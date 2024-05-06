#  Interpreter 3.7 -> 3.10
from PyQt5 import QtWidgets, QtCore, QtGui  # оставил 5-ую версию, потому что много наработок еще завязаны на нее
# todo ветка библиотек Qt - QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner, QtXml
# Руководство по установке см. https://packaging.python.org/tutorials/installing-packages/

# Пользовательская библиотека с классами
from moduleClassServerExchange import ServerExchange
# Задача создания пользовательских структур данных не расматривается -> Только функционал
# Компилируется и кладется в папку __pycache__
# Идея выноса каждого класса в этот отдельный файл, как на Java -> Удобство просмотра типов данных, не особо практично


SE = ServerExchange()


# fixme правильно писать конструктор
# todo Объявления внутри класса с конструктором и без
class AirLine(SE):
    def __init__(self):
        self.AirLine_ID = 1
        self.AirLineName = " "
        self.AirLineAlias = " "
        self.AirLineCodeIATA = " "
        self.AirLineCodeICAO = " "
        self.AirLineCallSighn = " "
        self.AirLineCity = " "
        self.AirLineCountry = " "
        self.AirLineStatus = 1
        self.CreationDate = '1920-01-01'
        self.AirLineDescription = " "
        self.Alliance = 4
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)
        self.cnxnAL = None  # подключение
        self.seekAL = None  # курсор

    def connectAL_DB(self, driver, servername, database):
        connection = SE.connectDB(driver=driver, servername=servername, database=database)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def connectAL_DSN(self, dsn):
        connection = SE.connectDSN(dsn=dsn)
        if connection[0]:
            self.cnxnAL = connection[1]
            self.seekAL = connection[2]
            return True
        else:
            return False

    def disconnectAL(self):
        SE.disconnect()
        pass

    def QueryAirLineByIATA(self, iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def QueryAirLineByPK(self, pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        return ResultSQL

    def InsertAirLineByIATAandICAO(self, iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekAL.execute(SQLQuery)
            if iata is None:
                print(" ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeICAO) VALUES ('" + str(icao) + "') "
            elif icao is None:
                print(" IATA=", str(iata))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA) VALUES ('" + str(iata) + "') "
            elif iata is None and icao is None:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES (NULL, NULL) "
                #print("raise Exception")
                #raise Exception
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES ('" + str(iata) + "', '" + str(icao) + "') "
            self.seekAL.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAL.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL


class AirCraft(ServerExchange):
    def __init__(self):
        self.AirCraftModel = 387  # Unknown Model
        self.BuildDate = '1990-01-01'
        self.RetireDate = '1990-01-01'
        self.SourceCSVFile = " "
        self.AirCraftDescription = " "
        self.AirCraftLineNumber_LN = " "
        self.AirCraftLineNumber_MSN = " "
        self.AirCraftSerialNumber_SN = " "
        self.AirCraftCNumber = " "
        self.EndDate = '1990-01-01'
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)

    # Подключения
    cnxnAC_XML = ' '
    cnxnAC = ' '
    cnxnFN = ' '
    # Курсоры
    seekAC_XML = ' '
    seekAC = ' '
    seekFN = ' '


class AirPort(ServerExchange):
    def __init__(self):
        self.HyperLinkToWikiPedia = " "
        self.HyperLinkToAirPortSite = " "
        self.HyperLinkToOperatorSite = " "
        self.HyperLinksToOtherSites = " "
        self.AirPortCodeIATA = " "
        self.AirPortCodeICAO = " "
        self.AirPortCodeFAA_LID = " "
        self.AirPortCodeWMO = " "
        self.AirPortName = " "
        self.AirPortCity = " "
        self.AirPortCounty = " "
        self.AirPortCountry = " "
        self.AirPortLatitude = 0
        self.AirPortLongitude = 0
        self.HeightAboveSeaLevel = 0
        self.SourceCSVFile = " "
        self.AirPortDescription = " "
        self.AirPortRunWays = " "
        self.AirPortFacilities = " "
        self.AirPortIncidents = " "

    cnxnRT = ' '  # подключение
    seekRT = ' '  # курсор


class ServerNames:
    # Имена серверов
    #ServerNameOriginal = "data-server-1.movistar.vrn.skylink.local"
    ServerNameOriginal = "localhost\mssqlserver15"  # указал имя NetBIOS и указал инстанс
    #ServerNameOriginal = "localhost\sqldeveloper"  # указал инстанс
    # fixme Забыл отменить обратно, надо проверить как самолеты и авиарейсы грузились без него причем в рабочую базу -> Все нормально, этот выбор работал, если грузить не через системный DSN
    ServerNameFlights = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
    ServerName = "localhost\mssqlserver15"  # указал инстанс
    #ServerName = "localhost\sqldeveloper"  # указал инстанс


class FileNames:
    # Имена читаемых и записываемых файлов
    InputFileCSV = ' '
    LogFileTXT = ' '
    ErrorFileTXT = 'LogReport_Errors.txt'


class Flags:
    # Флаги
    useAirFlightsDB = True
    useAirCraftsDSN = False
    useXQuery = False
    SetInputDate = False
    BeginDate = ' '


class States:
    # Состояния
    Connected_AL = False
    Connected_RT = False
    Connected_ACFN = False
    Connected_AC_XML = False


class Ui_DialogLoadAirFlightsWithAirCrafts(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogLoadAirFlightsWithAirCrafts, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(940, 375)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        #Dialog.setBaseSize(QtWidgets.QSize(0, 0))
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QtCore.QRect(50, 230, 81, 20))
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QtCore.QRect(530, 40, 181, 16))
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QtCore.QRect(150, 40, 251, 20))
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_DSN_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN_FN.setObjectName(u"comboBox_DSN_FN")
        self.comboBox_DSN_FN.setGeometry(QtCore.QRect(520, 100, 201, 22))
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QtCore.QRect(530, 80, 181, 16))
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QtCore.QRect(50, 260, 81, 20))
        self.comboBox_DB_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_FN.setObjectName(u"comboBox_DB_FN")
        self.comboBox_DB_FN.setGeometry(QtCore.QRect(520, 20, 201, 22))
        self.comboBox_Driver_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_FN.setObjectName(u"comboBox_Driver_FN")
        self.comboBox_Driver_FN.setGeometry(QtCore.QRect(520, 60, 201, 22))
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QtCore.QRect(530, 0, 181, 20))
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QtCore.QRect(50, 290, 81, 20))
        self.pushButton_GetStarted = QtWidgets.QPushButton(Dialog)
        self.pushButton_GetStarted.setObjectName(u"pushButton_GetStarted")
        self.pushButton_GetStarted.setGeometry(QtCore.QRect(490, 350, 101, 21))
        self.pushButton_ChooseTXTFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseTXTFile.setObjectName(u"pushButton_ChooseTXTFile")
        self.pushButton_ChooseTXTFile.setGeometry(QtCore.QRect(40, 350, 91, 23))
        self.lineEdit_TXTFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_TXTFile.setObjectName(u"lineEdit_TXTFile")
        self.lineEdit_TXTFile.setGeometry(QtCore.QRect(140, 350, 281, 20))
        self.lineEdit_TXTFile.setReadOnly(False)
        self.lineEdit_CSVFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CSVFile.setObjectName(u"lineEdit_CSVFile")
        self.lineEdit_CSVFile.setGeometry(QtCore.QRect(140, 320, 281, 20))
        self.lineEdit_CSVFile.setReadOnly(False)
        self.pushButton_ChooseCSVFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseCSVFile.setObjectName(u"pushButton_ChooseCSVFile")
        self.pushButton_ChooseCSVFile.setGeometry(QtCore.QRect(40, 320, 91, 23))
        self.comboBox_Driver_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_RT.setObjectName(u"comboBox_Driver_RT")
        self.comboBox_Driver_RT.setGeometry(QtCore.QRect(320, 140, 191, 22))
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QtCore.QRect(330, 80, 171, 20))
        self.comboBox_DB_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_RT.setObjectName(u"comboBox_DB_RT")
        self.comboBox_DB_RT.setGeometry(QtCore.QRect(320, 100, 191, 22))
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QtCore.QRect(330, 120, 111, 16))
        self.lineEdit_ODBCversion_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_RT.setObjectName(u"lineEdit_ODBCversion_RT")
        self.lineEdit_ODBCversion_RT.setGeometry(QtCore.QRect(320, 260, 191, 20))
        self.lineEdit_Driver_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_RT.setObjectName(u"lineEdit_Driver_RT")
        self.lineEdit_Driver_RT.setGeometry(QtCore.QRect(320, 230, 191, 20))
        self.lineEdit_Schema_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_RT.setObjectName(u"lineEdit_Schema_RT")
        self.lineEdit_Schema_RT.setGeometry(QtCore.QRect(320, 290, 191, 20))
        self.pushButton_Disconnect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_RT.setObjectName(u"pushButton_Disconnect_RT")
        self.pushButton_Disconnect_RT.setGeometry(QtCore.QRect(420, 200, 91, 23))
        self.pushButton_Connect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_RT.setObjectName(u"pushButton_Connect_RT")
        self.pushButton_Connect_RT.setGeometry(QtCore.QRect(420, 170, 91, 23))
        self.lineEdit_Schema_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_AL.setObjectName(u"lineEdit_Schema_AL")
        self.lineEdit_Schema_AL.setGeometry(QtCore.QRect(140, 290, 171, 20))
        self.lineEdit_Driver_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_AL.setObjectName(u"lineEdit_Driver_AL")
        self.lineEdit_Driver_AL.setGeometry(QtCore.QRect(140, 230, 171, 20))
        self.lineEdit_ODBCversion_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AL.setObjectName(u"lineEdit_ODBCversion_AL")
        self.lineEdit_ODBCversion_AL.setGeometry(QtCore.QRect(140, 260, 171, 20))
        self.comboBox_DB_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_AL.setObjectName(u"comboBox_DB_AL")
        self.comboBox_DB_AL.setGeometry(QtCore.QRect(140, 100, 171, 22))
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QtCore.QRect(150, 120, 111, 20))
        self.pushButton_Disconnect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_AL.setObjectName(u"pushButton_Disconnect_AL")
        self.pushButton_Disconnect_AL.setGeometry(QtCore.QRect(220, 200, 91, 23))
        self.comboBox_Driver_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_AL.setObjectName(u"comboBox_Driver_AL")
        self.comboBox_Driver_AL.setGeometry(QtCore.QRect(140, 140, 171, 22))
        self.pushButton_Connect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_AL.setObjectName(u"pushButton_Connect_AL")
        self.pushButton_Connect_AL.setGeometry(QtCore.QRect(220, 170, 91, 23))
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setObjectName(u"lineEdit_Server")
        self.lineEdit_Server.setGeometry(QtCore.QRect(140, 60, 371, 20))
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QtCore.QRect(150, 80, 141, 20))
        self.dateEdit_BeginDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_BeginDate.setObjectName(u"dateEdit_BeginDate")
        self.dateEdit_BeginDate.setGeometry(QtCore.QRect(730, 290, 110, 22))
        self.checkBox_SetInputDate = QtWidgets.QCheckBox(Dialog)
        self.checkBox_SetInputDate.setObjectName(u"checkBox_SetInputDate")
        self.checkBox_SetInputDate.setGeometry(QtCore.QRect(730, 320, 201, 18))
        self.label_Version = QtWidgets.QLabel(Dialog)
        self.label_Version.setObjectName(u"label_Version")
        self.label_Version.setGeometry(QtCore.QRect(10, 170, 201, 20))
        self.label_Version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_Disconnect_AC = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_AC.setObjectName(u"pushButton_Disconnect_AC")
        self.pushButton_Disconnect_AC.setGeometry(QtCore.QRect(630, 200, 91, 23))
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QtCore.QRect(530, 120, 181, 16))
        self.pushButton_Connect_AC = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_AC.setObjectName(u"pushButton_Connect_AC")
        self.pushButton_Connect_AC.setGeometry(QtCore.QRect(630, 170, 91, 23))
        self.comboBox_DSN_AC = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN_AC.setObjectName(u"comboBox_DSN_AC")
        self.comboBox_DSN_AC.setGeometry(QtCore.QRect(520, 140, 201, 22))
        self.lineEdit_DSN_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN_AC.setObjectName(u"lineEdit_DSN_AC")
        self.lineEdit_DSN_AC.setGeometry(QtCore.QRect(520, 320, 201, 20))
        self.lineEdit_Schema_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_AC.setObjectName(u"lineEdit_Schema_AC")
        self.lineEdit_Schema_AC.setGeometry(QtCore.QRect(520, 290, 201, 20))
        self.lineEdit_Driver_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_AC.setObjectName(u"lineEdit_Driver_AC")
        self.lineEdit_Driver_AC.setGeometry(QtCore.QRect(520, 230, 201, 20))
        self.lineEdit_ODBCversion_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AC.setObjectName(u"lineEdit_ODBCversion_AC")
        self.lineEdit_ODBCversion_AC.setGeometry(QtCore.QRect(520, 260, 201, 20))
        self.lineEdit_Server_remote = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server_remote.setObjectName(u"lineEdit_Server_remote")
        self.lineEdit_Server_remote.setGeometry(QtCore.QRect(140, 20, 371, 20))
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QtCore.QRect(150, 0, 261, 20))
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QtCore.QRect(730, 10, 201, 81))
        self.radioButton_DSN_AirFlights = QtWidgets.QRadioButton(self.groupBox)
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_DSN_AirFlights)
        self.radioButton_DSN_AirFlights.setObjectName(u"radioButton_DSN_AirFlights")
        self.radioButton_DSN_AirFlights.setGeometry(QtCore.QRect(10, 40, 151, 20))
        self.radioButton_DB_AirFlights = QtWidgets.QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.radioButton_DB_AirFlights)
        self.radioButton_DB_AirFlights.setObjectName(u"radioButton_DB_AirFlights")
        self.radioButton_DB_AirFlights.setGeometry(QtCore.QRect(10, 20, 181, 18))
        self.radioButton_DSN_AirCrafts = QtWidgets.QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.radioButton_DSN_AirCrafts)
        self.radioButton_DSN_AirCrafts.setObjectName(u"radioButton_DSN_AirCrafts")
        self.radioButton_DSN_AirCrafts.setGeometry(QtCore.QRect(10, 60, 151, 18))
        self.label_execute = QtWidgets.QLabel(Dialog)
        self.label_execute.setObjectName(u"label_execute")
        self.label_execute.setGeometry(QtCore.QRect(670, 350, 261, 20))
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QtCore.QRect(610, 350, 51, 20))
        self.label_31 = QtWidgets.QLabel(Dialog)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QtCore.QRect(10, 10, 128, 128))
        self.label_31.setPixmap(QtGui.QPixmap(u"../\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/research.ico"))
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QtCore.QRect(430, 320, 81, 20))
        self.label_BeginDate = QtWidgets.QLabel(Dialog)
        self.label_BeginDate.setObjectName(u"label_BeginDate")
        self.label_BeginDate.setGeometry(QtCore.QRect(730, 270, 201, 20))
        self.label_BeginDate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QtCore.QRect(730, 100, 131, 51))
        self.radioButton_DSN_AirCrafts_DOM = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_DSN_AirCrafts_DOM.setObjectName(u"radioButton_DSN_AirCrafts_DOM")
        self.radioButton_DSN_AirCrafts_DOM.setGeometry(QtCore.QRect(10, 20, 51, 20))
        self.radioButton_DSN_AirCrafts_SAX = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_DSN_AirCrafts_SAX.setObjectName(u"radioButton_DSN_AirCrafts_SAX")
        self.radioButton_DSN_AirCrafts_SAX.setGeometry(QtCore.QRect(70, 20, 51, 18))

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_12.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_16.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_11.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432", None))
        self.label_9.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439 DSN \u043f\u043e \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u0430\u043c", None))
        self.label_14.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f ODBC", None))
        self.label_8.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u043e\u0432", None))
        self.label_15.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430", None))
        self.pushButton_GetStarted.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0443", None))
        self.pushButton_ChooseTXTFile.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0436\u0443\u0440\u043d\u0430\u043b\u0430", None))
        self.pushButton_ChooseCSVFile.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_18.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0430\u044d\u0440\u043e\u043f\u043e\u0440\u0442\u043e\u0432", None))
        self.label_19.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_RT.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.pushButton_Connect_RT.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.label_20.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_AL.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.pushButton_Connect_AL.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.label_21.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0430\u0432\u0438\u0430\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0439", None))
        self.checkBox_SetInputDate.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u0435\u0440\u0435\u043d\u043e\u0441 \u0434\u0430\u0442\u044b \u0438\u0437 \u0444\u0430\u0439\u043b\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_Version.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_Disconnect_AC.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.label_13.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439 DSN \u043f\u043e \u0441\u0430\u043c\u043e\u043b\u0435\u0442\u0430\u043c", None))
        self.pushButton_Connect_AC.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f", None))
        self.label_17.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u043e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.groupBox.setTitle(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0430\u0442\u044c \u0432:", None))
        self.radioButton_DSN_AirFlights.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u043e\u0432 (DSN)", None))
        self.radioButton_DB_AirFlights.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u043e\u0432 (\u0434\u0440\u0430\u0439\u0432\u0435\u0440)", None))
        self.radioButton_DSN_AirCrafts.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0414 \u0441\u0430\u043c\u043e\u043b\u0435\u0442\u043e\u0432 (DSN)", None))
        self.label_execute.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 = ", None))
        self.label_22.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0430\u0442\u0443\u0441:", None))
        self.label_31.setText("")
        self.label_23.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439 DSN", None))
        self.label_BeginDate.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043f\u0435\u0440\u0438\u043e\u0434\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.groupBox_2.setTitle(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u0430\u0440\u0441\u0438\u0442\u044c \u0411\u0414 \u043a\u0430\u043a:", None))
        self.radioButton_DSN_AirCrafts_DOM.setText(QtCore.QCoreApplication.translate("Dialog", u"DOM", None))
        self.radioButton_DSN_AirCrafts_SAX.setText(QtCore.QCoreApplication.translate("Dialog", u"SAX", None))


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_CorrectDialogAirLinesInput.ui -o Qt_Designer_CorrectDialogAirLinesInput.py
class Ui_DialogInputIATAandICAO(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogInputIATAandICAO, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(240, 245)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(130, 30, 31, 16))
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QtCore.QRect(130, 60, 31, 16))
        self.lineEdit_CodeIATA = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CodeIATA.setObjectName(u"lineEdit_CodeIATA")
        self.lineEdit_CodeIATA.setGeometry(QtCore.QRect(10, 30, 113, 20))
        self.lineEdit_CodeICAO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CodeICAO.setObjectName(u"lineEdit_CodeICAO")
        self.lineEdit_CodeICAO.setGeometry(QtCore.QRect(10, 60, 113, 20))
        self.checkBox_Status_IATA = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status_IATA.setObjectName(u"checkBox_Status_IATA")
        self.checkBox_Status_IATA.setGeometry(QtCore.QRect(170, 30, 61, 18))
        self.pushButton_SearchInsert = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchInsert.setObjectName(u"pushButton_SearchInsert")
        self.pushButton_SearchInsert.setGeometry(QtCore.QRect(150, 90, 81, 23))
        self.checkBox_Status_ICAO = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status_ICAO.setObjectName(u"checkBox_Status_ICAO")
        self.checkBox_Status_ICAO.setGeometry(QtCore.QRect(170, 60, 61, 18))
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QtCore.QRect(10, 90, 131, 141))
        self.label_25.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/edit.ico"))

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QtCore.QCoreApplication.translate("Dialog", u"IATA", None))
        self.label_2.setText(QtCore.QCoreApplication.translate("Dialog", u"ICAO", None))
        self.checkBox_Status_IATA.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u0443\u0441\u0442\u043e", None))
        self.pushButton_SearchInsert.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0441\u0442\u0430\u0432\u043a\u0430", None))
        self.checkBox_Status_ICAO.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u0443\u0441\u0442\u043e", None))
        self.label_25.setText("")
    # retranslateUi


class Ui_DialogCorrectAirPortsWithMap(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirPortsWithMap, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(920, 780)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setObjectName(u"lineEdit_DSN")
        self.lineEdit_DSN.setGeometry(QtCore.QRect(110, 100, 201, 20))
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setObjectName(u"lineEdit_ODBCversion")
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(110, 70, 201, 20))
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QtCore.QRect(330, 50, 111, 16))
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QtCore.QRect(10, 100, 91, 16))
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.pushButton_ConnectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_ConnectDB.setObjectName(u"pushButton_ConnectDB")
        self.pushButton_ConnectDB.setGeometry(QtCore.QRect(320, 100, 121, 23))
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setObjectName(u"lineEdit_Driver")
        self.lineEdit_Driver.setGeometry(QtCore.QRect(110, 40, 201, 20))
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setObjectName(u"lineEdit_Schema")
        self.lineEdit_Schema.setGeometry(QtCore.QRect(110, 130, 201, 20))
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.comboBox_DB = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB.setObjectName(u"comboBox_DB")
        self.comboBox_DB.setGeometry(QtCore.QRect(320, 20, 251, 22))
        self.comboBox_Driver = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver.setObjectName(u"comboBox_Driver")
        self.comboBox_Driver.setGeometry(QtCore.QRect(320, 70, 251, 22))
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QtCore.QRect(330, 0, 111, 16))
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QtCore.QRect(10, 130, 91, 16))
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setObjectName(u"lineEdit_Server")
        self.lineEdit_Server.setGeometry(QtCore.QRect(110, 10, 201, 20))
        self.pushButton_DisconnectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_DisconnectDB.setObjectName(u"pushButton_DisconnectDB")
        self.pushButton_DisconnectDB.setGeometry(QtCore.QRect(450, 100, 121, 23))
        self.pushButton_UpdateDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_UpdateDB.setObjectName(u"pushButton_UpdateDB")
        self.pushButton_UpdateDB.setEnabled(True)
        self.pushButton_UpdateDB.setGeometry(QtCore.QRect(320, 130, 121, 23))
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QtCore.QRect(20, 730, 51, 21))
        self.lineEdit_HeightAboveSeaLevel = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_HeightAboveSeaLevel.setObjectName(u"lineEdit_HeightAboveSeaLevel")
        self.lineEdit_HeightAboveSeaLevel.setGeometry(QtCore.QRect(150, 750, 131, 20))
        self.lineEdit_AirPortLongitude = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortLongitude.setObjectName(u"lineEdit_AirPortLongitude")
        self.lineEdit_AirPortLongitude.setGeometry(QtCore.QRect(80, 750, 61, 20))
        self.textEdit_AirPortCity = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCity.setObjectName(u"textEdit_AirPortCity")
        self.textEdit_AirPortCity.setGeometry(QtCore.QRect(10, 560, 271, 51))
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QtCore.QRect(20, 670, 181, 16))
        self.textEdit_SourceCSVFile = QtWidgets.QTextEdit(Dialog)
        self.textEdit_SourceCSVFile.setObjectName(u"textEdit_SourceCSVFile")
        self.textEdit_SourceCSVFile.setGeometry(QtCore.QRect(10, 180, 271, 51))
        self.textEdit_AirPortName = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortName.setObjectName(u"textEdit_AirPortName")
        self.textEdit_AirPortName.setGeometry(QtCore.QRect(10, 490, 271, 51))
        self.pushButton_SearchByIATA = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByIATA.setObjectName(u"pushButton_SearchByIATA")
        self.pushButton_SearchByIATA.setGeometry(QtCore.QRect(190, 340, 71, 23))
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QtCore.QRect(20, 610, 251, 16))
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QtCore.QRect(20, 470, 61, 16))
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QtCore.QRect(20, 540, 241, 16))
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QtCore.QRect(130, 370, 41, 16))
        self.lineEdit_AirPortLatitude = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortLatitude.setObjectName(u"lineEdit_AirPortLatitude")
        self.lineEdit_AirPortLatitude.setGeometry(QtCore.QRect(10, 750, 61, 20))
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QtCore.QRect(90, 730, 51, 21))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(130, 340, 41, 16))
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QtCore.QRect(20, 160, 171, 21))
        self.textEdit_AirPortCounty = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCounty.setObjectName(u"textEdit_AirPortCounty")
        self.textEdit_AirPortCounty.setGeometry(QtCore.QRect(10, 630, 271, 41))
        self.textEdit_AirPortCountry = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCountry.setObjectName(u"textEdit_AirPortCountry")
        self.textEdit_AirPortCountry.setGeometry(QtCore.QRect(10, 690, 271, 41))
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QtCore.QRect(160, 730, 111, 21))
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QtCore.QRect(130, 400, 51, 16))
        self.lineEdit_AirPortCodeFAA_LID = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortCodeFAA_LID.setObjectName(u"lineEdit_AirPortCodeFAA_LID")
        self.lineEdit_AirPortCodeFAA_LID.setGeometry(QtCore.QRect(10, 400, 113, 20))
        self.pushButton_SearchByICAO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByICAO.setObjectName(u"pushButton_SearchByICAO")
        self.pushButton_SearchByICAO.setGeometry(QtCore.QRect(190, 370, 71, 23))
        self.pushButton_SearchAndInsertByIATAandICAO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchAndInsertByIATAandICAO.setObjectName(u"pushButton_SearchAndInsertByIATAandICAO")
        self.pushButton_SearchAndInsertByIATAandICAO.setGeometry(QtCore.QRect(90, 460, 191, 23))
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QtCore.QRect(580, 10, 131, 141))
        self.label_29.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/internal_drive_alt_13801.ico"))
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QtCore.QRect(290, 160, 621, 611))
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.textEdit_AirPortDescription = QtWidgets.QTextEdit(self.tab_1)
        self.textEdit_AirPortDescription.setObjectName(u"textEdit_AirPortDescription")
        self.textEdit_AirPortDescription.setGeometry(QtCore.QRect(10, 10, 591, 561))
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.textEdit_AirPortFacilities = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_AirPortFacilities.setObjectName(u"textEdit_AirPortFacilities")
        self.textEdit_AirPortFacilities.setGeometry(QtCore.QRect(10, 10, 591, 561))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.textEdit_Incidents = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_Incidents.setObjectName(u"textEdit_Incidents")
        self.textEdit_Incidents.setGeometry(QtCore.QRect(10, 10, 591, 561))
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_4)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 9, 591, 561))
        self.verticalLayout_Map = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_Map.setObjectName(u"verticalLayout_Map")
        self.verticalLayout_Map.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.textBrowser_HyperLinks = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_HyperLinks.setObjectName(u"textBrowser_HyperLinks")
        self.textBrowser_HyperLinks.setGeometry(QtCore.QRect(720, 20, 191, 101))
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QtCore.QRect(730, 0, 161, 21))
        self.pushButton_HyperLinkChange_Wikipedia = QtWidgets.QPushButton(Dialog)
        self.pushButton_HyperLinkChange_Wikipedia.setObjectName(u"pushButton_HyperLinkChange_Wikipedia")
        self.pushButton_HyperLinkChange_Wikipedia.setGeometry(QtCore.QRect(190, 250, 71, 21))
        self.pushButton_HyperLinkChange_AirPort = QtWidgets.QPushButton(Dialog)
        self.pushButton_HyperLinkChange_AirPort.setObjectName(u"pushButton_HyperLinkChange_AirPort")
        self.pushButton_HyperLinkChange_AirPort.setGeometry(QtCore.QRect(190, 270, 71, 21))
        self.pushButton_HyperLinkChange_Operator = QtWidgets.QPushButton(Dialog)
        self.pushButton_HyperLinkChange_Operator.setObjectName(u"pushButton_HyperLinkChange_Operator")
        self.pushButton_HyperLinkChange_Operator.setGeometry(QtCore.QRect(190, 290, 71, 21))
        self.label_hyperlink_to_WikiPedia = QtWidgets.QLabel(Dialog)
        self.label_hyperlink_to_WikiPedia.setObjectName(u"label_hyperlink_to_WikiPedia")
        self.label_hyperlink_to_WikiPedia.setGeometry(QtCore.QRect(10, 250, 171, 21))
        self.label_HyperLink_to_AirPort = QtWidgets.QLabel(Dialog)
        self.label_HyperLink_to_AirPort.setObjectName(u"label_HyperLink_to_AirPort")
        self.label_HyperLink_to_AirPort.setGeometry(QtCore.QRect(10, 270, 171, 21))
        self.label_HyperLink_to_Operator = QtWidgets.QLabel(Dialog)
        self.label_HyperLink_to_Operator.setObjectName(u"label_HyperLink_to_Operator")
        self.label_HyperLink_to_Operator.setGeometry(QtCore.QRect(10, 290, 171, 21))
        self.pushButton_HyperLinksChange = QtWidgets.QPushButton(Dialog)
        self.pushButton_HyperLinksChange.setObjectName(u"pushButton_HyperLinksChange")
        self.pushButton_HyperLinksChange.setGeometry(QtCore.QRect(840, 130, 71, 21))
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QtCore.QRect(20, 230, 161, 21))
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QtCore.QRect(130, 430, 51, 16))
        self.lineEdit_AirPortCodeWMO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortCodeWMO.setObjectName(u"lineEdit_AirPortCodeWMO")
        self.lineEdit_AirPortCodeWMO.setGeometry(QtCore.QRect(10, 430, 113, 20))
        self.pushButton_SearchByFAALID = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByFAALID.setObjectName(u"pushButton_SearchByFAALID")
        self.pushButton_SearchByFAALID.setGeometry(QtCore.QRect(190, 400, 71, 23))
        self.pushButton_SearchByWMO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByWMO.setObjectName(u"pushButton_SearchByWMO")
        self.pushButton_SearchByWMO.setGeometry(QtCore.QRect(190, 430, 71, 23))
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QtCore.QRect(20, 310, 41, 21))
        self.label_CodeIATA = QtWidgets.QLabel(Dialog)
        self.label_CodeIATA.setObjectName(u"label_CodeIATA")
        self.label_CodeIATA.setGeometry(QtCore.QRect(20, 340, 101, 20))
        self.label_CodeICAO = QtWidgets.QLabel(Dialog)
        self.label_CodeICAO.setObjectName(u"label_CodeICAO")
        self.label_CodeICAO.setGeometry(QtCore.QRect(20, 370, 101, 20))

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(3)


        QtCore.QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_12.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_16.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_13.setText(QtCore.QCoreApplication.translate("Dialog", u"DSN", None))
        self.label_11.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_ConnectDB.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.label_14.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f ODBC", None))
        self.label_8.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_15.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430", None))
        self.pushButton_DisconnectDB.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414", None))
        self.pushButton_UpdateDB.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f", None))
        self.label_17.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0428\u0438\u0440\u043e\u0442\u0430", None))
        self.label_7.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0440\u0430\u043d\u0430", None))
        self.pushButton_SearchByIATA.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.label_6.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0431\u043b\u0430\u0441\u0442\u044c, \u043e\u043a\u0440\u0443\u0433, \u043f\u0440\u043e\u0432\u0438\u043d\u0446\u0438\u044f, \u0448\u0442\u0430\u0442, \u043f\u0440\u0435\u0444\u0435\u043a\u0442\u0443\u0440\u0430", None))
        self.label_3.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.label_5.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u043b\u0438\u0436\u043d\u0438\u0435 \u043d\u0430\u0441\u0435\u043b\u0435\u043d\u043d\u044b\u0435 \u043f\u0443\u043d\u043a\u0442\u044b", None))
        self.label_2.setText(QtCore.QCoreApplication.translate("Dialog", u"ICAO", None))
        self.label_19.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u043e\u043b\u0433\u043e\u0442\u0430", None))
        self.label.setText(QtCore.QCoreApplication.translate("Dialog", u"IATA", None))
        self.label_21.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u0438", None))
        self.label_22.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0410\u0431\u0441. \u043e\u0442\u043c\u0435\u0442\u043a\u0430, \u043c", None))
        self.label_24.setText(QtCore.QCoreApplication.translate("Dialog", u"FAA LID", None))
        self.pushButton_SearchByICAO.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.pushButton_SearchAndInsertByIATAandICAO.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0438\u0441\u043a \u0438 \u0412\u0441\u0442\u0430\u0432\u043a\u0430 \u043f\u043e IATA \u0438 \u043f\u043e ICAO", None))
        self.label_29.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QtCore.QCoreApplication.translate("Dialog", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtCore.QCoreApplication.translate("Dialog", u"Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
        self.label_25.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0441\u044b\u043b\u043a\u0438 \u043d\u0430 \u0434\u0440\u0443\u0433\u0438\u0435 \u0441\u0430\u0439\u0442\u044b:", None))
        self.pushButton_HyperLinkChange_Wikipedia.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButton_HyperLinkChange_AirPort.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButton_HyperLinkChange_Operator.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.label_hyperlink_to_WikiPedia.setText(QtCore.QCoreApplication.translate("Dialog", u"WikiPedia", None))
        self.label_HyperLink_to_AirPort.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0430\u0439\u0442 \u0430\u044d\u0440\u043e\u043f\u043e\u0440\u0442\u0430 \u0438\u043b\u0438 \u0430\u044d\u0440\u043e\u0434\u0440\u043e\u043c\u0430", None))
        self.label_HyperLink_to_Operator.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0430\u0439\u0442 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430 \u0430\u044d\u0440\u043e\u043f\u043e\u0440\u0442\u0430", None))
        self.pushButton_HyperLinksChange.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.label_26.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0441\u044b\u043b\u043a\u0438 \u043d\u0430 \u0441\u0430\u0439\u0442\u044b:", None))
        self.label_27.setText(QtCore.QCoreApplication.translate("Dialog", u"WMO", None))
        self.pushButton_SearchByFAALID.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.pushButton_SearchByWMO.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.label_28.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041a\u043e\u0434\u044b:", None))
        self.label_CodeIATA.setText(QtCore.QCoreApplication.translate("Dialog", u"IATA", None))
        self.label_CodeICAO.setText(QtCore.QCoreApplication.translate("Dialog", u"ICAO", None))
    # retranslateUi

    # Окончание вставки тела конвертированного ресурсного файла

    # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# Вставка картинки https://stackoverflow.com/questions/28536306/inserting-an-image-in-gui-using-qt-designer
# > pyuic5 Qt_Designer_CorrectDialogAirLines.ui -o Qt_Designer_CorrectDialogAirLines.py
class Ui_DialogCorrectAirLine(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirLine, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(862, 830)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setGeometry(QtCore.QRect(120, 280, 181, 20))
        self.lineEdit_DSN.setObjectName("lineEdit_DSN")
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(120, 250, 181, 20))
        self.lineEdit_ODBCversion.setObjectName("lineEdit_ODBCversion")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 280, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_11.setObjectName("label_11")
        self.pushButton_SelectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_SelectDB.setGeometry(QtCore.QRect(400, 110, 181, 23))
        self.pushButton_SelectDB.setObjectName("pushButton_SelectDB")
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.lineEdit_Driver.setObjectName("lineEdit_Driver")
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setGeometry(QtCore.QRect(120, 310, 181, 20))
        self.lineEdit_Schema.setObjectName("lineEdit_Schema")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 250, 91, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(20, 310, 91, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setGeometry(QtCore.QRect(400, 140, 181, 23))
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.pushButton_Update = QtWidgets.QPushButton(Dialog)
        self.pushButton_Update.setEnabled(True)
        self.pushButton_Update.setGeometry(QtCore.QRect(460, 800, 91, 23))
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setGeometry(QtCore.QRect(30, 780, 111, 21))
        self.label_17.setObjectName("label_17")
        self.lineEdit_Position = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Position.setGeometry(QtCore.QRect(380, 800, 71, 21))
        self.lineEdit_Position.setObjectName("lineEdit_Position")
        self.pushButton_Begin = QtWidgets.QPushButton(Dialog)
        self.pushButton_Begin.setGeometry(QtCore.QRect(640, 20, 91, 23))
        self.pushButton_Begin.setObjectName("pushButton_Begin")
        self.lineEdit_AirLineCodeIATA = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeIATA.setGeometry(QtCore.QRect(20, 350, 113, 20))
        self.lineEdit_AirLineCodeIATA.setObjectName("lineEdit_AirLineCodeIATA")
        self.lineEdit_AirLineAlias = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineAlias.setGeometry(QtCore.QRect(140, 800, 231, 20))
        self.lineEdit_AirLineAlias.setObjectName("lineEdit_AirLineAlias")
        self.textEdit_AirLineCity = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineCity.setGeometry(QtCore.QRect(20, 560, 281, 51))
        self.textEdit_AirLineCity.setObjectName("textEdit_AirLineCity")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(30, 690, 101, 16))
        self.label_7.setObjectName("label_7")
        self.textEdit_AirLineName = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineName.setGeometry(QtCore.QRect(20, 480, 281, 51))
        self.textEdit_AirLineName.setObjectName("textEdit_AirLineName")
        self.pushButton_SearchByIATA = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByIATA.setGeometry(QtCore.QRect(200, 350, 101, 23))
        self.pushButton_SearchByIATA.setObjectName("pushButton_SearchByIATA")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 620, 181, 16))
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 460, 111, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 540, 151, 16))
        self.label_5.setObjectName("label_5")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(390, 780, 61, 20))
        self.label_18.setObjectName("label_18")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 380, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit_AirLineID = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineID.setGeometry(QtCore.QRect(20, 800, 113, 20))
        self.lineEdit_AirLineID.setObjectName("lineEdit_AirLineID")
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setGeometry(QtCore.QRect(150, 780, 111, 21))
        self.label_19.setObjectName("label_19")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 350, 51, 16))
        self.label.setObjectName("label")
        self.lineEdit_AirLineCodeICAO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeICAO.setGeometry(QtCore.QRect(20, 380, 113, 20))
        self.lineEdit_AirLineCodeICAO.setObjectName("lineEdit_AirLineCodeICAO")
        self.pushButton_Next = QtWidgets.QPushButton(Dialog)
        self.pushButton_Next.setGeometry(QtCore.QRect(640, 80, 91, 23))
        self.pushButton_Next.setObjectName("pushButton_Next")
        self.textEdit_AirLineCountry = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineCountry.setGeometry(QtCore.QRect(20, 710, 281, 31))
        self.textEdit_AirLineCountry.setObjectName("textEdit_AirLineCountry")
        self.pushButton_Previous = QtWidgets.QPushButton(Dialog)
        self.pushButton_Previous.setGeometry(QtCore.QRect(640, 50, 91, 23))
        self.pushButton_Previous.setObjectName("pushButton_Previous")
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setGeometry(QtCore.QRect(240, 410, 51, 20))
        self.label_24.setObjectName("label_24")
        self.lineEdit_CallSign = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CallSign.setGeometry(QtCore.QRect(20, 410, 211, 20))
        self.lineEdit_CallSign.setObjectName("lineEdit_CallSign")
        self.pushButton_SearchByICAO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByICAO.setGeometry(QtCore.QRect(200, 380, 101, 23))
        self.pushButton_SearchByICAO.setObjectName("pushButton_SearchByICAO")
        self.pushButton_Insert = QtWidgets.QPushButton(Dialog)
        self.pushButton_Insert.setGeometry(QtCore.QRect(100, 440, 201, 23))
        self.pushButton_Insert.setObjectName("pushButton_Insert")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(10, 20, 131, 141))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/folder.ico"))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setGeometry(QtCore.QRect(590, 20, 41, 41))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_25.ico"))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setGeometry(QtCore.QRect(590, 70, 41, 41))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_21.ico"))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(350, 120, 41, 41))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_22.ico"))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(150, 20, 131, 141))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("Значки (Иконки)/Device_Drive_Internal_alt_24444.ico"))
        self.label_29.setObjectName("label_29")
        self.checkBox_Status = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status.setGeometry(QtCore.QRect(20, 440, 71, 18))
        self.checkBox_Status.setObjectName("checkBox_Status")
        self.dateEdit_CreateDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_CreateDate.setGeometry(QtCore.QRect(20, 640, 110, 22))
        self.dateEdit_CreateDate.setObjectName("dateEdit_CreateDate")
        self.graphicsView_Logo = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView_Logo.setGeometry(QtCore.QRect(140, 620, 161, 81))
        self.graphicsView_Logo.setObjectName("graphicsView_Logo")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(30, 740, 211, 16))
        self.label_10.setObjectName("label_10")
        self.comboBox_Alliance = QtWidgets.QComboBox(Dialog)
        self.comboBox_Alliance.setGeometry(QtCore.QRect(20, 760, 251, 22))
        self.comboBox_Alliance.setObjectName("comboBox_Alliance")
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setGeometry(QtCore.QRect(30, 670, 101, 16))
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(340, 60, 111, 16))
        self.label_16.setObjectName("label_16")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(340, 10, 111, 16))
        self.label_8.setObjectName("label_8")
        self.comboBox_Driver = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver.setGeometry(QtCore.QRect(290, 80, 291, 22))
        self.comboBox_Driver.setObjectName("comboBox_Driver")
        self.comboBox_DB = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB.setGeometry(QtCore.QRect(290, 30, 291, 22))
        self.comboBox_DB.setObjectName("comboBox_DB")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(310, 170, 541, 611))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.textEdit_AirLineDescription = QtWidgets.QTextEdit(self.tab_1)
        self.textEdit_AirLineDescription.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.textEdit_AirLineDescription.setObjectName("textEdit_AirLineDescription")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2_tableWidget_1 = QtWidgets.QTableWidget(self.tab_2)
        self.tab_2_tableWidget_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_2_tableWidget_1.setObjectName("tab_2_tableWidget_1")
        self.tab_2_tableWidget_1.setColumnCount(0)
        self.tab_2_tableWidget_1.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tab_3_treeWidget_Hubs = QtWidgets.QTreeWidget(self.tab_3)
        self.tab_3_treeWidget_Hubs.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_3_treeWidget_Hubs.setObjectName("tab_3_treeWidget_Hubs")
        self.tab_3_treeWidget_Hubs.headerItem().setText(0, "1")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tab_4_listWidget_1 = QtWidgets.QListWidget(self.tab_4)
        self.tab_4_listWidget_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_4_listWidget_1.setObjectName("tab_4_listWidget_1")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tab_5_toolBox_1 = QtWidgets.QToolBox(self.tab_5)
        self.tab_5_toolBox_1.setGeometry(QtCore.QRect(20, 10, 57, 561))
        self.tab_5_toolBox_1.setObjectName("tab_5_toolBox_1")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_1.setObjectName("page_1")
        self.tab_5_toolBox_1.addItem(self.page_1, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page.setObjectName("page")
        self.tab_5_toolBox_1.addItem(self.page, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_3.setObjectName("page_3")
        self.tab_5_toolBox_1.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_4.setObjectName("page_4")
        self.tab_5_toolBox_1.addItem(self.page_4, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_2.setObjectName("page_2")
        self.tab_5_toolBox_1.addItem(self.page_2, "")
        self.tab_5_treeView_1 = QtWidgets.QTreeView(self.tab_5)
        self.tab_5_treeView_1.setGeometry(QtCore.QRect(85, 10, 441, 571))
        self.tab_5_treeView_1.setObjectName("tab_5_treeView_1")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tab_6_tableView_1 = QtWidgets.QTableView(self.tab_6)
        self.tab_6_tableView_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_6_tableView_1.setObjectName("tab_6_tableView_1")
        self.tabWidget.addTab(self.tab_6, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.tab_5_toolBox_1.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_13.setText(_translate("Dialog", "DSN"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.pushButton_SelectDB.setText(_translate("Dialog", "Подключиться к БД"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "Отключиться от БД"))
        self.pushButton_Update.setText(_translate("Dialog", "Записать"))
        self.label_17.setText(_translate("Dialog", "ID"))
        self.pushButton_Begin.setText(_translate("Dialog", "Начало"))
        self.label_7.setText(_translate("Dialog", "Страна"))
        self.pushButton_SearchByIATA.setText(_translate("Dialog", "Поиск"))
        self.label_6.setText(_translate("Dialog", "Дата основания"))
        self.label_3.setText(_translate("Dialog", "Наименование"))
        self.label_5.setText(_translate("Dialog", "Город (Штаб-квартира)"))
        self.label_18.setText(_translate("Dialog", "Позиция"))
        self.label_2.setText(_translate("Dialog", "ICAO"))
        self.label_19.setText(_translate("Dialog", "Псевдоним"))
        self.label.setText(_translate("Dialog", "IATA"))
        self.pushButton_Next.setText(_translate("Dialog", "Следующий"))
        self.pushButton_Previous.setText(_translate("Dialog", "Предыдущий"))
        self.label_24.setText(_translate("Dialog", "Позывной"))
        self.pushButton_SearchByICAO.setText(_translate("Dialog", "Поиск"))
        self.pushButton_Insert.setText(_translate("Dialog", "Поиск и Вставка по IATA и по ICAO"))
        self.checkBox_Status.setText(_translate("Dialog", "Статус"))
        self.label_10.setText(_translate("Dialog", "Альянс"))
        self.label_22.setText(_translate("Dialog", "Логотип"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_8.setText(_translate("Dialog", "База данных"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_1), _translate("Dialog", "Page 1"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_3), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_4), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_2), _translate("Dialog", "Page 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "Страница"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
