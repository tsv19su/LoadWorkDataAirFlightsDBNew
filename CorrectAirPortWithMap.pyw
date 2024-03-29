#  Interpreter 3.7 -> 3.10


# QtSQL медленнее, чем pyodbc
import pyodbc
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets  # pip install PyQtWebEngine -> поставил
import io
import folium
#from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine -> поставил

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes


# Делаем экземпляры
A = Classes.AirPort()
S = Classes.Servers()
# Добавляем аттрибуты
#S.ServerName = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
S.ServerName = "localhost\mssqlserver15"  # указал инстанс
#S.ServerName = "localhost\sqldeveloper"  # указал инстанс
S.Connected_RT = False


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    # fixme Сделать скрипт, который копирует данные таблицы по коду IATA строку за строкой из одной базы в другую
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    # fixme Правильно сделать экземпляр с композицией
    myDialog = Classes.Ui_DialogCorrectAirPortsWithMap()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(920, 780)
    myDialog.setWindowTitle('АэроПорты')
    myDialogInput = Classes.Ui_DialogCorrectAirLineInput()
    myDialogInput.setupUi(Dialog=myDialogInput)
    myDialogInput.setFixedSize(240, 245)
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.pushButton_ConnectDB.setToolTip("После подключения нажмите кнопку Поиск")
    myDialog.pushButton_UpdateDB.setToolTip("Запись внесенных изменений в БД \n Перед нажатием правильно заполнить и проверить введенные данные")
    myDialog.pushButton_UpdateDB.setEnabled(False)
    myDialog.pushButton_DisconnectDB.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_DisconnectDB.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_DSN.setEnabled(False)
    myDialog.lineEdit_Schema.setEnabled(False)
    # Добавляем базы данных в выпадающий список
    myDialog.comboBox_DB.addItem("AirPortsAndRoutesDBNew62")
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    myDialog.textEdit_SourceCSVFile.setEnabled(False)
    myDialog.label_hyperlink_to_WikiPedia.setEnabled(False)
    myDialog.label_HyperLink_to_AirPort.setEnabled(False)
    myDialog.label_HyperLink_to_Operator.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_Operator.setEnabled(False)
    myDialog.lineEdit_AirPortCodeIATA.setEnabled(False)
    myDialog.lineEdit_AirPortCodeICAO.setEnabled(False)
    myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(False)
    myDialog.lineEdit_AirPortCodeWMO.setEnabled(False)
    myDialog.pushButton_SearchByIATA.setToolTip("Поиск по коду IATA\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByIATA.setEnabled(False)
    myDialog.pushButton_SearchByICAO.setToolTip("Поиск по коду ICAO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByICAO.setEnabled(False)
    myDialog.pushButton_SearchByFAALID.setToolTip("Поиск по коду FAA LID\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByFAALID.setEnabled(False)
    myDialog.pushButton_SearchByWMO.setToolTip("Поиск по коду WMO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByWMO.setEnabled(False)
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setToolTip("Считаем, что аэропорт или аэродром однозначно определяются сочетанием кодов IATA и ICAO\nКоды FAA LID и WMO подисываются дополнительно\nЕсли код IATA пустой, то вероятно просто аэродром или взлетная полоса без инфраструктуры")
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(False)
    myDialog.textEdit_AirPortName.setEnabled(False)
    myDialog.textEdit_AirPortCity.setEnabled(False)
    myDialog.textEdit_AirPortCounty.setEnabled(False)
    myDialog.textEdit_AirPortCountry.setEnabled(False)
    myDialog.lineEdit_AirPortLatitude.setEnabled(False)
    myDialog.lineEdit_AirPortLongitude.setEnabled(False)
    myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setOpenExternalLinks(True)
    myDialog.textBrowser_HyperLinks.setReadOnly(True)
    myDialog.textBrowser_HyperLinks.setEnabled(False)
    myDialog.pushButton_HyperLinksChange.setToolTip("Изменение адресов ссылок")
    myDialog.pushButton_HyperLinksChange.setEnabled(False)
    myDialog.tabWidget.setTabText(0, "Описание")
    myDialog.tabWidget.setTabText(1, "Сооружения")
    myDialog.tabWidget.setTabText(2, "Случаи")
    myDialog.tabWidget.setTabText(3, "На карте")
    myDialog.tabWidget.setTabText(4, "Дополнительно")
    myDialog.tab_1.setToolTip("Общее описание аэропорта. История развития")
    myDialog.tab_2.setToolTip("Инфраструктура аэропорта, сооружения, хабы, арендаторы, склады, ангары")
    myDialog.tab_3.setToolTip("Случаи и инциденты")
    myDialog.tab_4.setToolTip("Расположение объекта на карте")
    myDialog.tab_5.setToolTip("Оснащение аппаратурой взаимодействия с самолетами (пока в разработке)")
    myDialog.textEdit_AirPortDescription.setEnabled(False)
    myDialog.textEdit_AirPortFacilities.setEnabled(False)
    myDialog.textEdit_Incidents.setEnabled(False)
    myDialog.verticalLayout_Map.setEnabled(False)
    myDialogInput.lineEdit_AirLineCodeIATA.setToolTip("Введите код IATA или поставьте галочку, если его нет")
    myDialogInput.lineEdit_AirLineCodeICAO.setToolTip("Введите код ICAO или поставьте галочку, если его нет")
    myDialogInput.checkBox_Status_IATA.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInput.checkBox_Status_ICAO.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInput.pushButton_SearchInsert.setToolTip("Внимательно проверить введенные данные. Исправления после вставки не предусматриваются")
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    myDialog.lineEditCodeFAA_LID = QtWidgets.QLineEdit()
    myDialog.lineEditCodeWMO = QtWidgets.QLineEdit()
    # Привязки обработчиков
    myDialog.pushButton_ConnectDB.clicked.connect(lambda: PushButtonConnectDB())
    myDialog.pushButton_UpdateDB.clicked.connect(lambda: PushButtonUpdateDB())
    myDialog.pushButton_DisconnectDB.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_HyperLinkChange_Wikipedia.clicked.connect(lambda: PushButtonChangeHyperLinkWikiPedia())
    myDialog.pushButton_HyperLinkChange_AirPort.clicked.connect(lambda: PushButtonChangeHyperLinkAirPort())
    myDialog.pushButton_HyperLinkChange_Operator.clicked.connect(lambda: PushButtonChangeHyperLinkOperator())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_SearchByFAALID.clicked.connect(lambda: PushButtonSearchByFAA_LID())
    myDialog.pushButton_SearchByWMO.clicked.connect(lambda: PushButtonSearchByWMO())
    myDialog.pushButton_SearchAndInsertByIATAandICAO.clicked.connect(lambda: PushButtonInsertByIATAandICAO())
    myDialog.pushButton_HyperLinksChange.clicked.connect(lambda: PushButtonChangeHyperLinks())
    myDialogInput.pushButton_SearchInsert.clicked.connect(lambda: PushButtonInsert())
    myDialogInput.checkBox_Status_IATA.clicked.connect(lambda: Check_IATA())
    myDialogInput.checkBox_Status_ICAO.clicked.connect(lambda: Check_ICAO())

    def CommonPart():
        DBAirPort = S.QueryAirPortByPK(A.Position)
        if DBAirPort is not None:
            A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
            A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
            A.AirPortName = DBAirPort.AirPortName
            A.AirPortCity = DBAirPort.AirPortCity
            A.AirPortCounty = DBAirPort.AirPortCounty
            A.AirPortCountry = DBAirPort.AirPortCountry
            A.AirPortLatitude = DBAirPort.AirPortLatitude
            A.AirPortLongitude = DBAirPort.AirPortLongitude
            A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
            A.SourceCSVFile = DBAirPort.SourceCSVFile
            A.AirPortDescription = DBAirPort.AirPortDescription
            A.AirPortFacilities = DBAirPort.AirPortFacilities
            A.AirPortIncidents = DBAirPort.AirPortIncidents
            SetFields()
            return True
        elif DBAirPort is None:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не найдена")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()
            return False
        else:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не прочиталась")
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.exec_()
            return False

    def SetFields():
        # Выводим записи
        myDialog.textEdit_SourceCSVFile.clear()
        myDialog.textEdit_SourceCSVFile.append(str(A.SourceCSVFile))
        myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(A.HyperLinkToWikiPedia) + ">Wikipedia</a>")
        myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(A.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
        myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(A.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
        myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)
        myDialog.lineEdit_AirPortCodeIATA.setText(str(A.AirPortCodeIATA))
        myDialog.lineEdit_AirPortCodeICAO.setText(str(A.AirPortCodeICAO))
        myDialog.lineEdit_AirPortCodeFAA_LID.setText(str(A.AirPortCodeFAA_LID))
        myDialog.lineEdit_AirPortCodeWMO.setText(str(A.AirPortCodeWMO))
        myDialog.textEdit_AirPortName.clear()
        myDialog.textEdit_AirPortName.append(str(A.AirPortName))
        myDialog.textEdit_AirPortCity.clear()
        myDialog.textEdit_AirPortCity.append(str(A.AirPortCity))
        myDialog.textEdit_AirPortCounty.clear()
        myDialog.textEdit_AirPortCounty.append(str(A.AirPortCounty))
        myDialog.textEdit_AirPortCountry.clear()
        myDialog.textEdit_AirPortCountry.append(str(A.AirPortCountry))
        myDialog.lineEdit_AirPortLatitude.setText(str(A.AirPortLatitude))
        myDialog.lineEdit_AirPortLongitude.setText(str(A.AirPortLongitude))
        myDialog.lineEdit_HeightAboveSeaLevel.setText(str(A.HeightAboveSeaLevel))
        myDialog.textBrowser_HyperLinks.clear()
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Wikipedia</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт аэропорта или аэродрома</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт оператора аэропорта</a>")
        myDialog.textEdit_AirPortDescription.clear()
        myDialog.textEdit_AirPortDescription.append(str(A.AirPortDescription))
        myDialog.textEdit_AirPortFacilities.clear()
        myDialog.textEdit_AirPortFacilities.append(A.AirPortFacilities)
        myDialog.textEdit_Incidents.clear()
        myDialog.textEdit_Incidents.append(A.AirPortIncidents)
        coordinates = (A.AirPortLatitude, A.AirPortLongitude)
        # Варианты карт: OpenStreetMap (подробная цветная), CartoDB Positron (серенькая), CartoDB Voyager (аскетичная, мало подписей и меток), NASAGIBS Blue Marble (пока не отрисовывается)
        m = folium.Map(tiles='OpenStreetMap',
                       zoom_start=13,
                       location=coordinates)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        webView = QtWebEngineWidgets.QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        # очищаем предыдущую отрисовку
        if myDialog.verticalLayout_Map is not None:
            while myDialog.verticalLayout_Map.count():
                child = myDialog.verticalLayout_Map.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    myDialog.verticalLayout_Map.clearLayout(child.layout())
        # новая отрисовка
        myDialog.verticalLayout_Map.addWidget(webView)

    def SwitchingGUI(Key):
        myDialog.comboBox_DB.setEnabled(not Key)
        myDialog.comboBox_Driver.setEnabled(not Key)
        myDialog.lineEdit_Server.setEnabled(Key)
        myDialog.lineEdit_Driver.setEnabled(Key)
        myDialog.lineEdit_ODBCversion.setEnabled(Key)
        myDialog.lineEdit_DSN.setEnabled(Key)
        myDialog.lineEdit_Schema.setEnabled(Key)
        myDialog.textEdit_SourceCSVFile.setEnabled(Key)
        myDialog.label_hyperlink_to_WikiPedia.setEnabled(Key)
        myDialog.label_HyperLink_to_AirPort.setEnabled(Key)
        myDialog.label_HyperLink_to_Operator.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Operator.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeIATA.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeICAO.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeWMO.setEnabled(Key)
        myDialog.pushButton_SearchByIATA.setEnabled(Key)
        myDialog.pushButton_SearchByICAO.setEnabled(Key)
        myDialog.pushButton_SearchByFAALID.setEnabled(Key)
        myDialog.pushButton_SearchByWMO.setEnabled(Key)
        myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(Key)
        myDialog.textEdit_AirPortName.setEnabled(Key)
        myDialog.textEdit_AirPortCity.setEnabled(Key)
        myDialog.textEdit_AirPortCounty.setEnabled(Key)
        myDialog.textEdit_AirPortCountry.setEnabled(Key)
        myDialog.lineEdit_AirPortLatitude.setEnabled(Key)
        myDialog.lineEdit_AirPortLongitude.setEnabled(Key)
        myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(Key)
        myDialog.textBrowser_HyperLinks.setEnabled(Key)
        myDialog.pushButton_HyperLinksChange.setEnabled(Key)
        myDialog.textEdit_AirPortDescription.setEnabled(Key)
        myDialog.textEdit_AirPortFacilities.setEnabled(Key)
        myDialog.textEdit_Incidents.setEnabled(Key)
        myDialog.verticalLayout_Map.setEnabled(Key)

    def PushButtonConnectDB():
        if not S.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_ConnectDB.setEnabled(False)
            # Подключаемся к базе данных по выбранному источнику
            ChoiceDB = myDialog.comboBox_DB.currentText()
            ChoiceDriver = myDialog.comboBox_Driver.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase = str(ChoiceDB)
            S.DriverODBC = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnRT = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                print("  База данных ", S.DataBase, " подключена")
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnRT.autocommit = False
                print("autocommit is disabled")
                # Ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
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
                S.seekRT = S.cnxnRT.cursor()
                print("seeks is on")
                S.Connected_RT = True
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnRT.getinfo(pyodbc.SQL_SERVER_NAME))
                # Драйвер
                myDialog.lineEdit_Driver.setText(S.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(S.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                # Источник данных
                myDialog.lineEdit_DSN.setText(S.cnxnRT.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(S.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                # Переводим в рабочее состояние (продолжение)
                SwitchingGUI(True)
                myDialog.pushButton_DisconnectDB.setEnabled(True)
                A.Position = 1
            except Exception:
                # Переводим в рабочее состояние
                myDialog.pushButton_ConnectDB.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect():
        # кнопка 'Отключиться от базы данных' нажата
        if S.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_DisconnectDB.setEnabled(False)
            # Снимаем курсоры
            S.seekRT.close()
            # Отключаемся от базы данных
            S.cnxnRT.close()
            # Снимаем флаги
            S.Connected_RT = False
            # Переводим в рабочее состояние (продолжение)
            SwitchingGUI(False)
            myDialog.pushButton_UpdateDB.setEnabled(False)  # возможно пока не тут
            myDialog.pushButton_ConnectDB.setEnabled(True)

    def PushButtonUpdateDB():
        # Кнопка "Записать"
        # todo вставить диалог выбора и проверки сертификата (ЭЦП) и условный переход с проверкой
        A.AirPortCodeICAO = myDialog.lineEdit_AirPortCodeICAO.text()
        A.AirPortName = myDialog.textEdit_AirPortName.toPlainText()
        A.AirPortCity = myDialog.textEdit_AirPortCity.toPlainText()
        A.AirPortCounty = myDialog.textEdit_AirPortCounty.toPlainText()
        A.AirPortCountry = myDialog.textEdit_AirPortCountry.toPlainText()
        A.AirPortLatitude = myDialog.lineEdit_AirPortLatitude.text()
        A.AirPortLongitude = myDialog.lineEdit_AirPortLongitude.text()
        A.HeightAboveSeaLevel = myDialog.lineEdit_HeightAboveSeaLevel.text()
        A.SourceCSVFile = myDialog.textEdit_SourceCSVFile.toPlainText()
        A.AirPortDescription = myDialog.textEdit_AirPortDescription.toPlainText()
        A.AirPortFacilities = myDialog.textEdit_AirPortFacilities.toPlainText()
        A.AirPortIncidents = myDialog.textEdit_Incidents.toPlainText()
        # Вносим изменение
        ResultUpdate = S.UpdateAirPort(A.AirPortCodeIATA,
                                       A.AirPortCodeICAO,
                                       A.AirPortName,
                                       A.AirPortCity,
                                       A.AirPortCounty,
                                       A.AirPortCountry,
                                       A.AirPortLatitude,
                                       A.AirPortLongitude,
                                       A.HeightAboveSeaLevel,
                                       A.SourceCSVFile,
                                       A.AirPortDescription,
                                       A.AirPortFacilities,
                                       A.AirPortIncidents)
        if not ResultUpdate:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не переписалась")
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.exec_()

    def PushButtonChangeHyperLinkWikiPedia():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            A.HyperLinkToWikiPedia = Link
            print(str(Link))
            myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(A.HyperLinkToWikiPedia) + ">Wikipedia</a>")
            myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkAirPort():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            A.HyperLinkToAirPortSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(A.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
            myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkOperator():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            A.HyperLinkToOperatorSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(A.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
            myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinks():
        pass

    def PushButtonSearchByIATA():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            DBAirPort = S.QueryAirPortByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirPort is not None:
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.HyperLinkToWikiPedia = DBAirPort.HyperLinkToWikiPedia
                A.HyperLinkToAirPortSite = DBAirPort.HyperLinkToAirPortSite
                A.HyperLinkToOperatorSite = DBAirPort.HyperLinkToOperatorSite
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortCodeFAA_LID = DBAirPort.AirPortCodeFAA_LID
                A.AirPortCodeWMO = DBAirPort.AirPortCodeWMO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            SetFields()
            myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByICAO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            DBAirPort = S.QueryAirPortByICAO(Code)
            if DBAirPort is not None:
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.HyperLinkToWikiPedia = DBAirPort.HyperLinkToWikiPedia
                A.HyperLinkToAirPortSite = DBAirPort.HyperLinkToAirPortSite
                A.HyperLinkToOperatorSite = DBAirPort.HyperLinkToOperatorSite
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortCodeFAA_LID = DBAirPort.AirPortCodeFAA_LID
                A.AirPortCodeWMO = DBAirPort.AirPortCodeWMO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            SetFields()
            myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByFAA_LID():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код FAA LID", "Введите код FAA LID")
        if ok:
            DBAirPort = S.QueryAirPortByFAA_LID(Code)
            if DBAirPort is not None:
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.HyperLinkToWikiPedia = DBAirPort.HyperLinkToWikiPedia
                A.HyperLinkToAirPortSite = DBAirPort.HyperLinkToAirPortSite
                A.HyperLinkToOperatorSite = DBAirPort.HyperLinkToOperatorSite
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortCodeFAA_LID = DBAirPort.AirPortCodeFAA_LID
                A.AirPortCodeWMO = DBAirPort.AirPortCodeWMO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            SetFields()
            myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByWMO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код WMO", "Введите код WMO")
        if ok:
            DBAirPort = S.QueryAirPortByWMO(Code)
            if DBAirPort is not None:
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.HyperLinkToWikiPedia = DBAirPort.HyperLinkToWikiPedia
                A.HyperLinkToAirPortSite = DBAirPort.HyperLinkToAirPortSite
                A.HyperLinkToOperatorSite = DBAirPort.HyperLinkToOperatorSite
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortCodeFAA_LID = DBAirPort.AirPortCodeFAA_LID
                A.AirPortCodeWMO = DBAirPort.AirPortCodeWMO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            SetFields()
            myDialog.pushButton_UpdateDB.setEnabled(True)

    def Check_IATA():
        if myDialogInput.checkBox_Status_IATA.isChecked():
            myDialogInput.lineEdit_AirLineCodeIATA.setEnabled(False)
        else:
            myDialogInput.lineEdit_AirLineCodeIATA.setEnabled(True)

    def Check_ICAO():
        if myDialogInput.checkBox_Status_ICAO.isChecked():
            myDialogInput.lineEdit_AirLineCodeICAO.setEnabled(False)
        else:
            myDialogInput.lineEdit_AirLineCodeICAO.setEnabled(True)

    def PushButtonInsert():
        if myDialogInput.checkBox_Status_IATA.isChecked():
            Code_IATA = None
        else:
            Code_IATA = myDialogInput.lineEdit_AirLineCodeIATA.text()
        if myDialogInput.checkBox_Status_ICAO.isChecked():
            Code_ICAO = None
        else:
            Code_ICAO = myDialogInput.lineEdit_AirLineCodeICAO.text()
        DBAirLine = S.QueryAirLineByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
        myDialogInput.close()

        def Transfer():
            A.Position = DBAirLine.AirLineUniqueNumber
            A.AirLine_ID = DBAirLine.AirLine_ID
            A.AirLineName = DBAirLine.AirLineName
            A.AirLineAlias = DBAirLine.AirLineAlias
            A.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
            A.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
            A.AirLineCallSighn = DBAirLine.AirLineCallSighn
            A.AirLineCity = DBAirLine.AirLineCity
            A.AirLineCountry = DBAirLine.AirLineCountry
            if DBAirLine.AirLineStatus is not None:
                A.AirLineStatus = DBAirLine.AirLineStatus
            else:
                A.AirLineStatus = False
            if DBAirLine.CreationDate:
                A.CreationDate = DBAirLine.CreationDate
            A.AirLineDescription = DBAirLine.AirLineDescription
            if DBAirLine.Alliance:
                A.Alliance = DBAirLine.Alliance
            else:
                A.Alliance = 4
            if A.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if A.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

        if DBAirLine is not None:
            # Переходим на найденную запись
            Transfer()
            message = QtWidgets.QMessageBox()
            message.setText("Такая запись есть")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()
        elif DBAirLine is None:
            # Вставка новой строки
            ResultInsert = S.InsertAirLineByIATAandICAO(Code_IATA, Code_ICAO)
            if ResultInsert:
                DBAirLine = S.QueryAirLineByIATAandICAO(Code_IATA, Code_ICAO)
                if DBAirLine is not None:
                    Transfer()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setText("Запись не прочиталась. Посмотрите ее через поиск")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не вставилась")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()

    def PushButtonInsertByIATAandICAO():
        # кнопка "Поиск и Вставка"
        # Отрисовка диалога ввода
        myDialogInput.setWindowTitle("Диалог ввода")
        myDialogInput.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogInput.show()

        """
        # кнопка 'Вставить новый' нажата
        LineCodeIATA, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите новый код IATA")
        if ok:
            myDialog.lineEditCodeIATA.setText(str(LineCodeIATA))
            Code = myDialog.lineEditCodeIATA.text()
            DBAirPort = S.QueryAirPortByIATA(Code)

            def Transfer():
                A.Position = DBAirPort.AirPortUniqueNumber
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
                SetFields()

            if DBAirPort is not None:
                # Переходим на найденную запись
                Transfer()
                message = QtWidgets.QMessageBox()
                message.setText("Такая запись есть. Вставляйте через поиск")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            elif DBAirPort is None:
                # Вставка новой строки
                ResultInsert = S.InsertAirPortByIATA(Code)
                if ResultInsert:
                    DBAirPort = S.QueryAirPortByIATA(Code)
                    if DBAirPort is not None:
                        Transfer()
                    else:
                        message = QtWidgets.QMessageBox()
                        message.setText("Запись не прочиталась. Посмотрите ее через поиск")
                        message.setIcon(QtWidgets.QMessageBox.Warning)
                        message.exec_()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setText("Запись не вставилась")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
        """

    # Отрисовка первого окна
    myDialog.show()
    # Правильное закрытие окна
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа,
# в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
