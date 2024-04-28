#  Interpreter 3.7 -> 3.10


import pyodbc  # pymssql работает тяжелее, пробуем также SQLAlchemy
import pandas
import itertools
import datetime
import time
import os
import sys
import socket
import threading
# оставили 5-ую версию, потому что много наработок еще завязаны на нее
# QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner - запускаем в командной строке, QtXml (устарел) -> замена QXmlStreamReader, QXmlStreamWriter
from PyQt5 import QtWidgets
import pathlib
#import stringcolor  # fixme в IDLE и в pyCharm раскраска не работает, в командной строке сразу слетает
import colorama
import termcolor
#import tqdm  # fixme tqdm нужен свой цикл -> сюда не подходит

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes
# todo  - Сделать пользовательскую наработку (не библиотеку и не пакет) отдельным репозиторием
#       - Импортировать ее как подмодуль для повторного применения синхронно (mutualy connected) или асинхронно (independent) -> Импортировал асинхронно, обновление только вручную на командах git, для синхронного нет функционала
#       - Результат импорта -> на github-е - синяя неактивная ссылка, по которой никуда не перейдешь, внутри pyCharm-а - дубликат репозитория подмодуля в локальную ветку
# fixme Есть проблемка при импорте пользовательских библиотек из внешних файлов по другим путям из других папок
# fixme pyCharm как графическая оболочка пока не работает с подмодулями в графическом режиме [@Aleks10](https://qna.habr.com/q/196071), а пока только командами 'git submodules'


# Версия обработки с цветным выводом
__myOwnDevelopingVersion__ = 8.42
# todo Версия задается тут. Пакеты на GitHub-е *.tar.gz (под Linux или под BSD) не нужны. Выпуск релизов пока не имеет практической пользы, как указано в ReadME.md

colorama.init(autoreset=False)  # используем Colorama, чтобы сделать работу Termcolor на Windows, оставляем цветовое оформление до следующего явного указания
print(termcolor.colored("Обработка v" + str(__myOwnDevelopingVersion__) + " загрузки рабочих данных в БД SQL Server-а", 'blue', 'on_yellow'))
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
#print("Разработал " + stringcolor.bold("Тарасов Сергей").cs("red", "gold") + " tsv19su@yandex.ru")
print(termcolor.colored("Пользователь = " + str(os.getlogin()), 'green', 'on_yellow'))

# fixme Вывести в файл requirements.txt список пакетов с версиями - пока не требуется
# pip freeze > requirements.txt

# fixme Установить пакеты с определенными версиями - пока не требуется
# pip install -r requirements.txt

# fixme Установить пакет из папки, как пример
# pip install SomePackage-1.0-py2.py3-none-any.whl

# Делаем экземпляр
S = Classes.Servers()

# Имена серверов
#S.ServerNameOriginal = "data-server-1.movistar.vrn.skylink.local"
S.ServerNameOriginal = "localhost\mssqlserver15"  # указал имя NetBIOS и указал инстанс
#S.ServerNameOriginal = "localhost\sqldeveloper"  # указал инстанс
# fixme Забыл отменить обратно, надо проверить как самолеты и авиарейсы грузились без него причем в рабочую базу -> Все нормально, этот выбор работал, если грузить не через системный DSN
S.ServerNameFlights = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
S.ServerName = "localhost\mssqlserver15"  # указал инстанс
#S.ServerName = "localhost\sqldeveloper"  # указал инстанс

# Имена читаемых и записываемых файлов
S.InputFileCSV = ' '
S.LogFileTXT = ' '
S.ErrorFileTXT = 'LogReport_Errors.txt'

# Флаги
S.useAirFlightsDB = True
S.useAirCraftsDSN = False
S.SetInputDate = False

# Состояния
S.Connected_AL = False
#S.Connected_AC = False
S.Connected_RT = False
S.Connected_ACFN = False
S.Connected_AC_XML = False


def myApplication():
    # Одно прикладное приложение
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    myDialog = Classes.Ui_DialogLoadAirFlightsWithAirCrafts()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(940, 375)
    myDialog.setWindowTitle('Загрузка рабочих данных')
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.label_Version.setText("Версия обработки " + str(__myOwnDevelopingVersion__))
    # Получаем список DSN-ов
    # Добавляем атрибут DSNs по ходу действия
    S.DSNs = pyodbc.dataSources()  # добавленные системные DSN-ы
    if S.DSNs:
        for DSN in S.DSNs:
            if not DSN:
                break
            myDialog.comboBox_DSN_FN.addItem(str(DSN))
            myDialog.comboBox_DSN_AC.addItem(str(DSN))
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver_AL.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_RT.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_FN.addItem(str(DriverODBC))
    # Добавляем базы данных в выпадающие списки
    myDialog.comboBox_DB_AL.addItem("AirLinesDBNew62")
    myDialog.comboBox_DB_RT.addItem("AirPortsAndRoutesDBNew62")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew42")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew52")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew62WorkBase")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew72WorkBase")
    myDialog.radioButton_DB_AirFlights.setToolTip("Использовать имя базы данных и драйвер СУБД")
    myDialog.radioButton_DSN_AirFlights.setToolTip("Использовать системный DSN")
    myDialog.radioButton_DSN_AirCrafts.setToolTip("Использовать системный DSN")  # дошел до сюда
    myDialog.dateEdit_BeginDate.setToolTip("Дата начала периода загрузки рабочих данных")
    myDialog.checkBox_SetInputDate.setToolTip("Перенос даты авиарейса из входных данных")
    myDialog.pushButton_GetStarted.setToolTip("Запуск загрузки исходных данных по авиаперелетам \nВнимательно проверьте параметры загрузки")

    def UpdateAirLinesSourcesChoiceByStatesAndFlags():
        if S.Connected_AL:
            # Переключаем в рабочее состояние
            myDialog.comboBox_DB_AL.setEnabled(False)
            myDialog.comboBox_Driver_AL.setEnabled(False)
            if S.Connected_RT and (S.Connected_ACFN or S.Connected_AC_XML):
                PrepareForInputData(True)
        else:
            # Переключаем в исходное состояние
            # параметры соединения с сервером
            if not S.Connected_RT:
                myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_AL.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
            myDialog.lineEdit_Schema_AL.setEnabled(False)
            myDialog.comboBox_DB_AL.setEnabled(True)
            myDialog.comboBox_Driver_AL.setEnabled(True)
            PrepareForInputData(False)

    def UpdateAirPortsSourcesChoiceByStatesAndFlags():
        pass

    def UpdateFlightsSourcesChoiceByStatesAndFlags():
        # Состояния + Флаги -> Графическая оболочка
        if S.Connected_AC_XML or S.Connected_ACFN:
            myDialog.groupBox.setEnabled(False)
            myDialog.comboBox_DB_FN.setEnabled(False)
            myDialog.comboBox_Driver_FN.setEnabled(False)
            myDialog.comboBox_DSN_FN.setEnabled(False)
            myDialog.comboBox_DSN_AC.setEnabled(False)
            if S.Connected_AL and S.Connected_RT:
                PrepareForInputData(True)
        else:
            myDialog.groupBox.setEnabled(True)
            if S.useAirCraftsDSN:
                myDialog.comboBox_DB_FN.setEnabled(False)
                myDialog.comboBox_Driver_FN.setEnabled(False)
                myDialog.comboBox_DSN_FN.setEnabled(False)
                myDialog.comboBox_DSN_AC.setEnabled(True)
            else:
                myDialog.comboBox_DSN_AC.setEnabled(False)
                if S.useAirFlightsDB:
                    myDialog.comboBox_DB_FN.setEnabled(True)
                    myDialog.comboBox_Driver_FN.setEnabled(True)
                    myDialog.comboBox_DSN_FN.setEnabled(False)
                else:
                    myDialog.comboBox_DB_FN.setEnabled(False)
                    myDialog.comboBox_Driver_FN.setEnabled(False)
                    myDialog.comboBox_DSN_FN.setEnabled(True)
            # Переключаем в исходное состояние
            PrepareForInputData(False)
            # параметры соединения с сервером
            myDialog.lineEdit_Server_remote.setEnabled(False)
            myDialog.lineEdit_Driver_AC.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AC.setEnabled(False)
            myDialog.lineEdit_Schema_AC.setEnabled(False)
            myDialog.lineEdit_DSN_AC.setEnabled(False)

    UpdateFlightsSourcesChoiceByStatesAndFlags()
    #UpdateFlightsSourcesChoiceByStatesAndFlags()
    myDialog.pushButton_Disconnect_AL.setEnabled(False)
    myDialog.pushButton_Disconnect_RT.setEnabled(False)
    myDialog.pushButton_Disconnect_AC.setEnabled(False)
    myDialog.dateEdit_BeginDate.setEnabled(False)
    myDialog.checkBox_SetInputDate.setChecked(False)
    myDialog.checkBox_SetInputDate.setEnabled(False)
    myDialog.pushButton_ChooseCSVFile.setEnabled(False)
    myDialog.lineEdit_CSVFile.setEnabled(False)
    myDialog.pushButton_ChooseTXTFile.setEnabled(False)
    myDialog.lineEdit_TXTFile.setEnabled(False)
    #myDialog.progressBar_completion.setEnabled(False)
    #myDialog.progressBar_completion.setToolTip("Выполнение загрузки рабочих данных, проценты")
    myDialog.pushButton_GetStarted.setEnabled(False)
    # параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Server_remote.setEnabled(False)
    myDialog.lineEdit_Driver_AL.setEnabled(False)
    myDialog.lineEdit_Driver_RT.setEnabled(False)
    myDialog.lineEdit_Driver_AC.setEnabled(False)
    myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
    myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
    myDialog.lineEdit_ODBCversion_AC.setEnabled(False)
    myDialog.lineEdit_Schema_AL.setEnabled(False)
    myDialog.lineEdit_Schema_RT.setEnabled(False)
    myDialog.lineEdit_Schema_AC.setEnabled(False)
    myDialog.lineEdit_DSN_AC.setEnabled(False)
    myDialog.label_execute.setEnabled(False)
    # Привязки обработчиков todo без lambda не работает
    myDialog.pushButton_Connect_AL.clicked.connect(lambda: PushButtonConnect_AL())  # Подключиться к базе данных
    myDialog.pushButton_Disconnect_AL.clicked.connect(lambda: PushButtonDisconnect_AL())  # Отключиться от базы данных
    myDialog.pushButton_Connect_RT.clicked.connect(lambda: PushButtonConnect_RT())
    myDialog.pushButton_Disconnect_RT.clicked.connect(lambda: PushButtonDisconnect_RT())
    myDialog.pushButton_Connect_AC.clicked.connect(lambda: PushButtonConnect_ACFN())
    myDialog.pushButton_Disconnect_AC.clicked.connect(lambda: PushButtonDisconnect_AC())
    # todo Объединить обе radioButton в одно, как на tkBuilder, и переделать на triggered -> СДЕЛАЛ
    myDialog.radioButton_DB_AirFlights.toggled.connect(lambda: RadioButtonsToggled())
    myDialog.radioButton_DSN_AirFlights.toggled.connect(lambda: RadioButtonsToggled())
    myDialog.radioButton_DSN_AirCrafts.toggled.connect(lambda: RadioButtonsToggled())
    #myDialog.groupBox.toggled.connect(lambda: RadioButtonsToggled())  # fixme не реагирует
    myDialog.pushButton_ChooseCSVFile.clicked.connect(lambda: PushButtonChooseCSVFile())  # Выбрать файл данных
    myDialog.pushButton_ChooseTXTFile.clicked.connect(lambda: PushButtonChooseLOGFile())  # Выбрать файл журнала
    myDialog.pushButton_GetStarted.clicked.connect(lambda: PushButtonGetStarted())  # Начать загрузку

    def RadioButtonsToggled():
        # Переключатели -> Флаги
        if myDialog.radioButton_DSN_AirCrafts.isChecked():
            S.useAirCraftsDSN = True
        else:
            S.useAirCraftsDSN = False
            if myDialog.radioButton_DB_AirFlights.isChecked():
                S.useAirFlightsDB = True
            if myDialog.radioButton_DSN_AirFlights.isChecked():
                S.useAirFlightsDB = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()

    def PrepareForInputData(Key):
        myDialog.pushButton_ChooseCSVFile.setEnabled(Key)
        myDialog.lineEdit_CSVFile.setEnabled(Key)
        myDialog.pushButton_ChooseTXTFile.setEnabled(Key)
        myDialog.lineEdit_TXTFile.setEnabled(Key)
        myDialog.dateEdit_BeginDate.setEnabled(Key)
        if Key:
            myDialog.dateEdit_BeginDate.setCalendarPopup(True)
        myDialog.checkBox_SetInputDate.setEnabled(Key)
        myDialog.pushButton_GetStarted.setEnabled(Key)

    def PushButtonConnect_AL():
        myDialog.pushButton_Connect_AL.setEnabled(False)
        if not S.Connected_AL:
            # Подключаемся к базе данных авиакомпаний
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            # https://docs.microsoft.com/ru-ru/previous-versions/dotnet/framework/data/adonet/sql/ownership-and-user-schema-separation-in-sql-server
            ChoiceDB = myDialog.comboBox_DB_AL.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_AL.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_AL = str(ChoiceDB)
            S.DriverODBC_AL = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                # todo Сделать сообщение с зелеными галочками по пунктам подключения
                S.cnxnAL = pyodbc.connect(driver=S.DriverODBC_AL, server=S.ServerNameOriginal, database=S.DataBase_AL)
                print("  БД = ", S.DataBase_AL, "подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnAL.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
                # API-курсоры ODBC по SQLSetStmtAttr:
                #  - тип SQL_ATTR_CURSOR_TYPE:
                #    - однопроходный (последовательный доступ),
                #    - статический (копия в tempdb),
                #    - управляемый набор ключей,
                #    - динамический,
                #    - смешанный
                #  - режим работы в стиле ISO:
                #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                # Клиентские однопроходные , статические API-курсоры ODBC.
                # Добавляем атрибуты seek...
                S.seekAL = S.cnxnAL.cursor()
                print("seeks is on")
                S.Connected_AL = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setEnabled(True)
                myDialog.lineEdit_Server.setText(S.cnxnAL.getinfo(pyodbc.SQL_SERVER_NAME))
                # Драйвер
                myDialog.lineEdit_Driver_AL.setEnabled(True)
                myDialog.lineEdit_Driver_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_DRIVER_NAME))
                # версия ODBC
                myDialog.lineEdit_ODBCversion_AL.setEnabled(True)
                myDialog.lineEdit_ODBCversion_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_ODBC_VER))
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_AL.setEnabled(True)
                myDialog.lineEdit_Schema_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_USER_NAME))
                UpdateAirLinesSourcesChoiceByStatesAndFlags()
                myDialog.pushButton_Disconnect_AL.setEnabled(True)
            except Exception:
                myDialog.pushButton_Connect_AL.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_AL():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        if S.Connected_AL:
            # Снимаем курсор
            S.seekAL.close()
            # Отключаемся от базы данных
            S.cnxnAL.close()
            S.Connected_AL = False
        # Переключаем в исходное состояние
        UpdateAirLinesSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AL.setEnabled(True)

    def PushButtonConnect_RT():
        myDialog.pushButton_Connect_RT.setEnabled(False)
        if not S.Connected_RT:
            # Подключаемся к базе данных аэропортов и маршрутов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB = myDialog.comboBox_DB_RT.currentText()
            ChoiceDriver = myDialog.comboBox_Driver_RT.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_RT = str(ChoiceDB)
            S.DriverODBC_RT = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnRT = pyodbc.connect(driver=S.DriverODBC_RT, server=S.ServerNameOriginal, database=S.DataBase_RT)
                print("  БД = ", S.DataBase_RT, "подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnRT.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-шные курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-шные курсоры (выборка кэшируется на клиенте)
                #
                # API-шные курсоры ODBC по SQLSetStmtAttr:
                #  - тип SQL_ATTR_CURSOR_TYPE:
                #    - однопроходный (последовательный доступ),
                #    - статический (копия в tempdb),
                #    - управляемый набор ключей,
                #    - динамический,
                #    - смешанный
                #  - режим работы в стиле ISO:
                #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                # Клиентские однопроходные, статические API-курсоры ODBC.
                # Добавляем атрибуты seek...
                S.seekRT = S.cnxnRT.cursor()
                print("seeks is on")
                S.Connected_RT = True
                # Переключаем в рабочее состояние
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnRT.getinfo(pyodbc.SQL_SERVER_NAME))
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver_RT.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion_RT.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema_RT.setEnabled(True)
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB_RT.setEnabled(False)
                myDialog.comboBox_Driver_RT.setEnabled(False)
                if S.Connected_AL and (S.Connected_ACFN or S.Connected_AC_XML):
                    PrepareForInputData(True)
                myDialog.pushButton_Disconnect_RT.setEnabled(True)
            except Exception:
                # Переводим в неактивное состояние
                myDialog.pushButton_Connect_RT.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов и маршрутов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_RT():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        if S.Connected_RT:
            # Снимаем курсор
            S.seekRT.close()
            # Отключаемся от базы данных
            S.cnxnRT.close()
            S.Connected_RT = False
        # Переключаем в исходное состояние
        myDialog.comboBox_DB_RT.setEnabled(True)
        myDialog.comboBox_Driver_RT.setEnabled(True)
        PrepareForInputData(False)
        # параметры соединения с сервером
        if not S.Connected_AL:
            myDialog.lineEdit_Server.setEnabled(False)
        myDialog.lineEdit_Driver_RT.setEnabled(False)
        myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
        myDialog.lineEdit_Schema_RT.setEnabled(False)
        myDialog.pushButton_Connect_RT.setEnabled(True)

    def PushButtonConnect_ACFN():
        if S.useAirCraftsDSN:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not S.Connected_AC_XML:
                # Подключаемся к базе данных самолетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDSN_AC_XML = myDialog.comboBox_DSN_AC.currentText()
                # Добавляем атрибут myDSN
                S.myDSN_AC_XML = str(ChoiceDSN_AC_XML)
                try:
                    # Добавляем атрибут cnxn
                    # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                    S.cnxnAC_XML = pyodbc.connect("DSN=" + S.myDSN_AC_XML)
                    # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                    S.cnxnAC_XML.autocommit = False
                    # Делаем свой экземпляр и ставим набор курсоров
                    # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                    #
                    # Способы реализации курсоров:
                    #  - SQL, Transact-SQL,
                    #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                    #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                    #
                    # API-курсоры ODBC по SQLSetStmtAttr:
                    #  - тип SQL_ATTR_CURSOR_TYPE:
                    #    - однопроходный (последовательный доступ),
                    #    - статический (копия в tempdb),
                    #    - управляемый набор ключей,
                    #    - динамический,
                    #    - смешанный
                    #  - режим работы в стиле ISO:
                    #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                    #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                    # Клиентские однопроходные , статические API-курсоры ODBC.
                    # Добавляем атрибуты seek...
                    S.seekAC_XML = S.cnxnAC_XML.cursor()
                    S.Connected_AC_XML = True
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(S.cnxnAC_XML.getinfo(pyodbc.SQL_SERVER_NAME))
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(S.cnxnAC_XML.getinfo(pyodbc.SQL_DRIVER_NAME))
                    # версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(S.cnxnAC_XML.getinfo(pyodbc.SQL_ODBC_VER))
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(S.cnxnAC_XML.getinfo(pyodbc.SQL_USER_NAME))
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(S.cnxnAC_XML.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                except Exception:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД самолетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    pass
                finally:
                    pass
        else:
            myDialog.pushButton_Connect_AC.setEnabled(False)
            if not S.Connected_ACFN:
                # Подключаемся к базе данных авиаперелетов
                # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
                ChoiceDB_ACFN = myDialog.comboBox_DB_FN.currentText()
                ChoiceDriver_ACFN = myDialog.comboBox_Driver_FN.currentText()
                # Добавляем атрибуты DataBase, DriverODBC
                S.DataBase_ACFN = str(ChoiceDB_ACFN)
                S.DriverODBC_ACFN = str(ChoiceDriver_ACFN)
                ChoiceDSN_ACFN = myDialog.comboBox_DSN_FN.currentText()
                # Добавляем атрибут myDSN
                S.myDSN_ACFN = str(ChoiceDSN_ACFN)
                try:
                    # Добавляем атрибут cnxn
                    if S.useAirFlightsDB:
                        # через драйвер СУБД + клиентский API-курсор
                        S.cnxnAC = pyodbc.connect(driver=S.DriverODBC_ACFN, server=S.ServerNameFlights, database=S.DataBase_ACFN)
                        S.cnxnFN = pyodbc.connect(driver=S.DriverODBC_ACFN, server=S.ServerNameFlights, database=S.DataBase_ACFN)
                    else:
                        # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                        S.cnxnAC = pyodbc.connect("DSN=" + S.myDSN_ACFN)
                        S.cnxnFN = pyodbc.connect("DSN=" + S.myDSN_ACFN)
                    # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                    S.cnxnAC.autocommit = False
                    S.cnxnFN.autocommit = False
                    # Делаем свой экземпляр и ставим набор курсоров
                    # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                    #
                    # Способы реализации курсоров:
                    #  - SQL, Transact-SQL,
                    #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                    #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                    #
                    # API-курсоры ODBC по SQLSetStmtAttr:
                    #  - тип SQL_ATTR_CURSOR_TYPE:
                    #    - однопроходный (последовательный доступ),
                    #    - статический (копия в tempdb),
                    #    - управляемый набор ключей,
                    #    - динамический,
                    #    - смешанный
                    #  - режим работы в стиле ISO:
                    #    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
                    #    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY

                    # Клиентские однопроходные , статические API-курсоры ODBC.
                    # Добавляем атрибуты seek...
                    S.seekAC = S.cnxnAC.cursor()
                    S.seekFN = S.cnxnFN.cursor()
                    S.Connected_ACFN = True
                    # Переключаем в рабочее состояние
                    # SQL Server
                    myDialog.lineEdit_Server_remote.setEnabled(True)
                    myDialog.lineEdit_Server_remote.setText(S.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME))
                    # Драйвер
                    myDialog.lineEdit_Driver_AC.setEnabled(True)
                    myDialog.lineEdit_Driver_AC.setText(S.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME))
                    # Версия ODBC
                    myDialog.lineEdit_ODBCversion_AC.setEnabled(True)
                    myDialog.lineEdit_ODBCversion_AC.setText(S.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER))
                    # Схема (если из-под другой учетки, то выводит имя учетки)
                    myDialog.lineEdit_Schema_AC.setEnabled(True)
                    myDialog.lineEdit_Schema_AC.setText(S.cnxnFN.getinfo(pyodbc.SQL_USER_NAME))
                    # Источник данных
                    myDialog.lineEdit_DSN_AC.setEnabled(True)
                    myDialog.lineEdit_DSN_AC.setText(S.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                    # Переводим в рабочее состояние (продолжение)
                    UpdateFlightsSourcesChoiceByStatesAndFlags()
                    if S.Connected_AL and S.Connected_RT:
                        PrepareForInputData(True)
                    myDialog.pushButton_Disconnect_AC.setEnabled(True)
                except Exception:
                    myDialog.pushButton_Connect_AC.setEnabled(True)
                    message = QtWidgets.QMessageBox()
                    message.setText("Нет подключения к БД авиаперелетов")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    pass
                finally:
                    pass

    def PushButtonDisconnect_AC():
        # Обработчик кнопки 'Отключиться от базы данных'
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        if S.Connected_AC_XML:
            # Снимаем курсор
            S.seekAC_XML.close()
            # Отключаемся от базы данных
            S.cnxnAC_XML.close()
            S.Connected_AC_XML = False
        if S.Connected_ACFN:
            # Снимаем курсор
            S.seekAC.close()
            # Отключаемся от базы данных
            S.cnxnAC.close()
            S.Connected_AC = False
            # Снимаем курсор
            S.seekFN.close()
            # Отключаемся от базы данных
            S.cnxnFN.close()
            S.Connected_ACFN = False
        UpdateFlightsSourcesChoiceByStatesAndFlags()
        myDialog.pushButton_Connect_AC.setEnabled(True)


    def PushButtonChooseCSVFile():
        filter = "Data files (*.csv)"
        S.InputFileCSV = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть рабочие данные", ' ', filter=filter)[0]
        S.urnCSV = S.InputFileCSV.rstrip(os.sep)  # не сработало
        S.filenameCSV = pathlib.Path(S.InputFileCSV).name  # сработало
        myDialog.lineEdit_CSVFile.setText(S.filenameCSV)

    def PushButtonChooseLOGFile():
        filter = "Log Files (*.txt *.text)"
        S.LogFileTXT = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть журнал", ' ', filter=filter)[0]
        S.filenameTXT = pathlib.Path(S.LogFileTXT).name
        myDialog.lineEdit_TXTFile.setText(S.filenameTXT)

    def LoadThread(Csv, Log):
        """
        Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
        Источник BTSgov (убал из файла все косые, запятые и кавычки)
        https://www.transtats.bts.gov/DL_SelectFields.asp - не работает
        https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr - работает
        """
        myDialog.label_execute.setText("Чтение и перепаковка исходных данных")
        myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: yellow")
        print("  Чтение и перепаковка исходных данных")
        print("  ожидайте ...", end=' ')
        # todo Если оперативной памяти не достаточно, то тут остановится
        DataFrameFromCSV = pandas.read_csv(Csv, sep=",")
        # В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем с ними
        ListAirLineCodeIATA = DataFrameFromCSV['OP_UNIQUE_CARRIER'].tolist()
        ListAirCraft = DataFrameFromCSV['TAIL_NUM'].tolist()
        ListAirPortDeparture = DataFrameFromCSV['ORIGIN'].tolist()
        ListAirPortArrival = DataFrameFromCSV['DEST'].tolist()
        ListFlightNumber = DataFrameFromCSV['OP_CARRIER_FL_NUM'].tolist()
        # fixme Переделать эту часть (формат даты и времени в файле исходных данных поменялся с 2018-09-23 на 9/1/2023 12:00:00 AM)
        ListFlightDate = DataFrameFromCSV['FL_DATE'].tolist()
        # todo Собрать новый список с датами соединением из 3-х списков с целыми числами поэлементно через минусы и использовать теперь его -> СОБРАЛ
        # todo Проверить на соответствие результат перед записью в базу -> ПРОВЕРИЛ
        ListYear = DataFrameFromCSV['YEAR'].tolist()
        ListMonth = DataFrameFromCSV['MONTH'].tolist()
        ListDay = DataFrameFromCSV['DAY_OF_MONTH'].tolist()
        ListFlightDateConcatenated = []
        for attemptNumber in range(len(ListYear)):
            ListFlightDateConcatenated.append(str(ListYear[attemptNumber]) + "-" + str(ListMonth[attemptNumber]) + "-" + str(ListDay[attemptNumber]))
        #myDialog.label_execute.setText("Исходные данные перепакованы")  # оболочка зависает и слетает
        if S.SetInputDate:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")
        else:
            myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: blue")
        print("Исходные данные перепакованы")
        # Списки
        ListAirLinesAdded = []
        ListAirLinesFailed = []
        ListAirCraftsAdded = []
        ListAirCraftsUpdated = []
        ListAirCraftsFailed = []
        ListAirPortsNotFounded = []
        # Счетчики
        CountRoutesAdded = 0
        CountRoutesFailed = 0
        CountFlightsAdded = 0
        CountFlightsPadded = 0
        CountFlightsFailed = 0
        CountProgressBarFailed = 0
        # Распределение плотности перезапросов сервера
        DistributionDensityAirLines = []
        DistributionDensityAirCrafts = []
        DistributionDensityAirRoutes = []
        DistributionDensityAirFlights = []
        Density = 2  # раз в секунду
        # attemptRetryCount = 750 * Density
        attemptRetryCount = 750
        for Index in range(attemptRetryCount):
            DistributionDensityAirLines.append(0)
            DistributionDensityAirCrafts.append(0)
            DistributionDensityAirRoutes.append(0)
            DistributionDensityAirFlights.append(0)
        # Дата и время сейчас
        Now = time.time()
        DateTime = time.ctime(Now)
        # Отметка времени начала загрузки
        __StartTime__ = datetime.datetime.now()
        #myDialog.label_execute.setText("Загрузка начата")  # оболочка зависает и слетает
        print(termcolor.colored("Загрузка начата", "red", "on_yellow"))
        # Сигнал на обновление полоски выполнения
        # _signalUpdateProgressBar = QtCore.pyqtSignal(float)
        completion = 0  # Выполнение загрузки
        ExecutePrevious = 0
        # pbar = tqdm.tqdm(len(ListAirLineCodeIATA))
        # Один внешний цикл и три вложенных цикла
        for AL, AC, Dep, Arr, FN, FD in zip(ListAirLineCodeIATA, ListAirCraft, ListAirPortDeparture, ListAirPortArrival, ListFlightNumber, ListFlightDateConcatenated):
            print(colorama.Fore.BLUE + "Авикомпания", str(AL), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = S.QueryAirLineByIATA(AL)
                if DBAirLine is None:
                    if S.InsertAirLineByIATAandICAO(AL, None):
                        ListAirLinesAdded.append(AL)
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "добавилась ", end=" ")
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirLine is not None:
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                ListAirLinesFailed.append(AL)
            print(" ")
            DistributionDensityAirLines[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Самолет", str(AC), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirCraft = S.QueryAirCraftByRegistration(AC)
                if DBAirCraft is None:
                    DBAirLine = S.QueryAirLineByIATA(AL)
                    if DBAirLine is None:
                        # Вставляем самолет с пустым внешним ключем
                        if S.InsertAirCraftByRegistration(Registration=AC, ALPK=None):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "добавился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirLine is not None:
                        # Вставляем самолет (на предыдущем цикле вставили авиакомпанию)
                        if S.InsertAirCraftByRegistration(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber):
                            ListAirCraftsAdded.append(AC)
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "добавился", end=" ")
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirCraft is not None:
                    # todo Когда сделаю базу данных по самолетам, эту часть переделать
                    DBAirLinePK = S.QueryAirLineByPK(DBAirCraft.AirCraftAirLine)
                    if DBAirLinePK is None or DBAirLinePK.AirLineCodeIATA != AL:
                        # fixme пустая ячейка в таблице SQL-ной БД - NULL <-> в Python-е - (None,) -> в условиях None и (None,) - не False и не True
                        # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация UNKNOWN не имеет внешнего ключа авиакомпании
                        # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация nan каждый раз переписывается на другую компанию-оператора
                        DBAirLine = S.QueryAirLineByIATA(AL)
                        if DBAirLine is None:
                            break
                        elif DBAirLine is not None:
                            if S.UpdateAirCraft(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber):
                                ListAirCraftsUpdated.append(AC)
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTCYAN_EX + "переписали на", str(AL), end=" ")
                                break
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "*", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirLinePK.AirLineCodeIATA == AL:
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                ListAirCraftsFailed.append(AC)
            print(" ")
            DistributionDensityAirCrafts[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Маршрут", str(Dep), "-", str(Arr), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirPortDep = S.QueryAirPortByIATA(Dep)
                if DBAirPortDep is not None:
                    DBAirPortArr = S.QueryAirPortByIATA(Arr)
                    if DBAirPortArr is not None:
                        DBAirRoute = S.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is None:
                            # Если есть оба аэропорта и нет маршрута
                            if S.InsertAirRoute(DBAirPortDep.AirPortUniqueNumber, DBAirPortArr.AirPortUniqueNumber):
                                CountRoutesAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "добавился", end=" ")
                                break
                            else:
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                        elif DBAirRoute is not None:
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirPortArr is None:
                        ListAirPortsNotFounded.append(Arr)
                        # Вставляем аэропорт только с кодом IATA
                        if S.InsertAirPortByIATA(Arr):
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                            print(colorama.Fore.GREEN + "добавили аэропорт", str(Arr), end=" ")
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirPortDep is None:
                    ListAirPortsNotFounded.append(Dep)
                    # Вставляем аэропорт только с кодом IATA
                    if S.InsertAirPortByIATA(Dep):
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                        print(colorama.Fore.GREEN + "добавили аэропорт", str(Dep), end=" ")
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                CountRoutesFailed += 1
            print(" ")
            DistributionDensityAirRoutes[deadlockCount] += 1
            print(colorama.Fore.BLUE + " Авиарейс", str(AL) + str(FN), end=" ")
            deadlockCount = 0  # Счетчик попыток -> Обнуляем
            if not S.SetInputDate:
                FD = S.BeginDate
            # Цикл попыток
            for attemptNumber in range(attemptRetryCount):
                deadlockCount = attemptNumber
                DBAirLine = S.QueryAirLineByIATA(AL)
                if DBAirLine is not None:
                    DBAirCraft = S.QueryAirCraftByRegistration(AC)
                    if DBAirCraft is not None:
                        DBAirRoute = S.QueryAirRoute(Dep, Arr)
                        if DBAirRoute is not None:
                            # todo между транзакциями маршрут и самолет еще раз перезапросить внутри вызываемой функции - СДЕЛАЛ
                            ResultModify = S.ModifyAirFlight(AC, AL, FN, Dep, Arr, FD, S.BeginDate)
                            if ResultModify == 0:
                                # fixme оболочка зависает и слетает
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                                time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
                            if ResultModify == 1:
                                CountFlightsAdded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "вставился", end=" ")
                                break
                            if ResultModify == 2:
                                CountFlightsPadded += 1
                                #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: green")  # оболочка зависает и слетает
                                print(colorama.Fore.GREEN + "сплюсовался", end=" ")
                                break
                        elif DBAirRoute is None:
                            CountFlightsFailed += 1
                            break
                        else:
                            #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(attemptNumber / Density)
                    elif DBAirCraft is None:
                        CountFlightsFailed += 1
                        break
                    else:
                        #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(attemptNumber / Density)
                elif DBAirLine is None:
                    CountFlightsFailed += 1
                    break
                else:
                    #myDialog.label_execute.setStyleSheet("border: 3px solid; border-color: red")  # оболочка зависает и слетает
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(attemptNumber / Density)  # пытаемся уйти от взаимоблокировки
            else:
                CountFlightsFailed += 1
            print(" ")
            DistributionDensityAirFlights[deadlockCount] += 1
            completion += 1
            Execute = round(100 * completion / len(ListFlightNumber), 2)  # вычисляем и округляем процент выполнения до 2 цифр после запятой
            # fixme При слишком частом обновлении виджета графическая оболочка подвисает, зависает или слетает (обработка исключения не помогает) -> Исправил
            if Execute > ExecutePrevious:
                stringExecute = "Выполнение = " + str(Execute) + " %"
                myDialog.label_execute.setText(stringExecute)
                ExecutePrevious = Execute
            # todo Сделать полосу выполнения все время внизу со всеми параметрами например с помощью tqdm - Не работает в цикле
            print(colorama.Fore.CYAN + "Выполнение =", str(Execute), "%")
            # pbar.update()
            # myDialog.progressBar_completion.setValue(int(Execute))  # fixme выдает ошибку про рекурсивную отрисовку (см. снимок экрана)
        # pbar.close()
        # Отметка времени окончания загрузки
        __EndTime__ = datetime.datetime.now()
        # Убираем с конца столбцы с нулями
        for Index in reversed(range(attemptRetryCount)):
            if DistributionDensityAirLines[Index] == 0 and DistributionDensityAirCrafts[Index] == 0 and DistributionDensityAirRoutes[Index] == 0 and DistributionDensityAirFlights[Index] == 0:
                DistributionDensityAirLines.pop(Index)
                DistributionDensityAirCrafts.pop(Index)
                DistributionDensityAirRoutes.pop(Index)
                DistributionDensityAirFlights.pop(Index)
            else:
                break
        # Собираем списки в DataFrame
        DataFrameDistributionDensity = pandas.DataFrame([DistributionDensityAirLines,
                                                         DistributionDensityAirCrafts,
                                                         DistributionDensityAirRoutes,
                                                         DistributionDensityAirFlights],
                                                        index=[" - авиакомпании", " - самолеты", " - маршруты", " - авиарейсы"])
        DataFrameDistributionDensity.index.name = "Базы данных:"
        OutputString = " \n \n"
        OutputString += "Загрузка рабочих данных (версия обработки - " + str(__myOwnDevelopingVersion__) + ") начата " + str(DateTime) + " \n"
        OutputString += " Загрузка проведена с " + str(socket.gethostname()) + " \n"
        OutputString += " Версия интерпретатора = " + str(sys.version) + " \n"
        OutputString += " Источник входных данных = " + str(S.filenameCSV) + " \n"
        OutputString += " Входные данные внесены за " + str(S.BeginDate) + " \n"
        if S.SetInputDate:
            OutputString += " Дата авиарейса проставлена из входного файла\n"
        else:
            OutputString += " Дата авиарейса проставлена как 1-ое число указанного месяца \n"
        OutputString += " Сервер СУБД = " + str(S.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME)) + " \n"
        OutputString += " Драйвер = " + str(S.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME)) + " \n"
        OutputString += " Версия ODBC = " + str(S.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER)) + " \n"
        OutputString += " DSN = " + str(S.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)) + " \n"
        OutputString += " Схема = " + str(S.cnxnFN.getinfo(pyodbc.SQL_USER_NAME)) + " \n"
        OutputString += " Длительность загрузки = " + str(__EndTime__ - __StartTime__) + " \n"
        OutputString += " Пользователь = " + str(os.getlogin()) + " \n"
        OutputString += " Итоги: \n"
        # Формируем итоги
        # todo Сделать итоги в виде XML и писать его полем XML.Document в базу данных
        if ListAirLinesAdded:
            OutputString += " - добавлены авиакомпании: \n  "
            OutputString += str(set(ListAirLinesAdded))  # fixme с регистрациями NaN надолго зависает, не убирает повторы и не группирует
            OutputString += " \n"
        if ListAirLinesFailed:
            OutputString += " - не добавлены данные по авиакомпаниям: \n  "
            OutputString += str(set(ListAirLinesFailed))
            OutputString += " \n"
        if ListAirCraftsAdded:
            OutputString += " - добавлены самолеты: \n  "
            OutputString += str(set(ListAirCraftsAdded))
            OutputString += " \n"
        if ListAirCraftsUpdated:
            OutputString += " - добавлены данные по самолетам: \n  "
            OutputString += str(set(ListAirCraftsUpdated))
            # Убираем только повторы, идущие подряд, но с сохранением исходного порядка fixme не работает
            OutPutNew = [el for el, _ in itertools.groupby(ListAirCraftsUpdated)]
            OutputString += " \n"
        if ListAirCraftsFailed:
            OutputString += " - не добавлены данные по самолетам: \n  "
            OutputString += str(set(ListAirCraftsFailed))
            OutputString += " \n"
        if CountRoutesAdded:
            OutputString += " - добавлено " + str(CountRoutesAdded) + " маршрутов \n"
        if CountRoutesFailed:
            OutputString += " - не добавлено " + str(CountRoutesFailed) + " маршрутов \n"
            OutputString += " \n"
        if ListAirPortsNotFounded:
            OutputString += " - не найдены аэропорты: \n  "
            OutputString += str(set(ListAirPortsNotFounded))
            OutputString += " \n"
        if CountFlightsAdded:
            OutputString += " - добавлено " + str(CountFlightsAdded) + " авиарейсов \n"
        if CountFlightsFailed:
            OutputString += " - не добавлено " + str(CountFlightsFailed) + " авиарейсов \n"
        if CountFlightsPadded:
            OutputString += " - сплюсовано " + str(CountFlightsPadded) + " авиарейсов \n"
        if CountProgressBarFailed:
            OutputString += " - отказов полосы выполнения =" + str(CountProgressBarFailed) + " \n"
        OutputString += " - перезапросы сервера: \n" + str(DataFrameDistributionDensity) + " \n"
        # Дописываем в журнал (обычным способом)
        # fixme Большая строка не дописывается, скрипт долго висит
        try:
            # fixme При больших объемах дозаписи и одновременном доступе к журналу нескольких обработок не все результаты дописываются в него
            LogFile = open(Log, 'a')
            LogFile.write(OutputString)
            # LogFile.write('Вывод обычным способом\n')
        except IOError:
            try:
                LogError = open(S.ErrorFileTXT, 'a')
                LogError.write("Ошибка дозаписи результатов по " + str(S.filenameCSV) + " в " + str(S.filenameTXT) + " \n")
            except IOError:
                print("Ошибка дозаписи в файл журнала")
            finally:
                LogError.close()
            print(colorama.Fore.LIGHTYELLOW_EX + "Ошибка дозаписи в " + str(S.filenameTXT))
        finally:
            LogFile.close()
        # Дописываем в журнал (с помощью менеджера контекста)
        # with open(Log, 'a') as LogFile:
        #     LogFile.write(OutputString)
        #     LogFile.write('Вывод с помощью менеджера контекста\n')
        # fixme Тут графическая оболочка слетела
        time.sleep(2)  # задержка, чтобы исправить этот момент
        myDialog.label_execute.setText("Загрузка окончена")
        myDialog.label_execute.setStyleSheet("border: 5px solid; border-color: pink")
        print(termcolor.colored("Загрузка окончена", "red", "on_yellow"))
        # Снимаем курсоры
        S.seekAL.close()
        S.seekAC.close()
        S.seekRT.close()
        S.seekFN.close()
        S.seekAC_XML.close()
        # Отключаемся от баз данных
        S.cnxnAL.close()
        S.cnxnAC.close()
        S.cnxnRT.close()
        S.cnxnFN.close()
        S.cnxnAC_XML.close()

    def PushButtonGetStarted():
        myDialog.pushButton_GetStarted.setEnabled(False)
        S.BeginDate = myDialog.dateEdit_BeginDate.date().toString('yyyy-MM-dd')
        if myDialog.checkBox_SetInputDate.isChecked():
            S.SetInputDate = True
        else:
            S.SetInputDate = False
        myDialog.pushButton_ChooseCSVFile.setEnabled(False)
        myDialog.pushButton_ChooseTXTFile.setEnabled(False)
        myDialog.dateEdit_BeginDate.setEnabled(False)
        myDialog.checkBox_SetInputDate.setEnabled(False)
        myDialog.pushButton_Disconnect_AL.setEnabled(False)
        myDialog.pushButton_Disconnect_RT.setEnabled(False)
        myDialog.pushButton_Disconnect_FN.setEnabled(False)
        myDialog.pushButton_Disconnect_AC.setEnabled(False)
        myDialog.label_execute.setEnabled(True)
        # todo Заброс на возможность запуска нескольких загрузок с доработкой графической оболочки без ее закрытия на запуске загрузки
        threadLoad = threading.Thread(target=LoadThread, daemon=False, args=(S.InputFileCSV, S.LogFileTXT, ))  # поток не сам по себе
        threadLoad.start()
        # fixme с ... .join() кнопки не гаснут, графическая оболочка зависает -> убрал ... .join()
        #threadLoad.join(1)  # ждем поток в основном потоке (графическая оболочка зависает), секунд
        #myDialog.close()  # закрываем графическую оболочку, текстовая остается

    # Отрисовка диалога
    myDialog.show()
    # Правильное закрытие диалога
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__,
# только если файл запускается как основная программа, в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
