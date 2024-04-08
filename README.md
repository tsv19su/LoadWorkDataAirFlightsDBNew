Некоторые сводные наработки (базы данных на внешнем MS SQL Server-е и набор клиентских утилит) по:
 - авиационному процессингу,
 - авиационной диспетчеризации,
 - авиационной телеметрии,
 - авиационной телематике.
 ----

#### Описание

В объем данного проекта входит:
 - разработка баз данных (справочные, рабочие и оперативные данные) на внешнем сервере СУБД,
 - администрирование сервера СУБД,
 - разработка прикладного программного обеспечения - утилит и графических оболочек (в части `UX/UI`) - для работы с ними,
 - загрузка рабочих и оперативных данных с помощью утилит (графических диалоговых формочек и в командной строке),
 - правка справочных данных с помощью графических оболочек (графических диалоговых формочек),
 - первичная аналитика баз данных,
 - предоставление способа взаимодействия другим проектам с помощью API-шек.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, вертодромы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

![формочка Аэропорты](https://github.com/tsv19su254052/LoadWorkData-GUIs-and-Utilities/assets/104857185/96656c8b-25bd-4810-ae42-006a4f959ede)

использовались из источников:
 - [apinfo.ru](http://apinfo.ru )
 - [openflights.org](http://openflights.org)
 - [ourairport.com](http://www1.ourairport.com) (переезжает на другое место, в России не открывается)
 - [planelist.net](http://planelist.net)
 - [flightradar24.com](http://www.flightradar24.com)
 - [jetphotos.com](https://www.jetphotos.com)

Рабочие данные загружаются с [BTS](https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)

Оперативные данные загружаются асинхронно:
 - с [flightradar24.com](http://www.flightradar24.com) на API-шках и по ВЭБ-хукам (надо покупать и оплачивать токен),
 - с первичного оборудования.

Рабочие и оперативные данные загружаются без учета хронологии.

Инфраструктура:
 - сервер СУБД, 
 - файловый сервер,
 - терминальный сервер - работают по учеткам `Windows` без контроллера домена.

Работа клиентов возможна в локальной подсети или из внешней сети через рабочий стол терминального сервера по `RDP`. Разрабатывать отдельную прикладную серверную компоненту на сервере СУБД пока не требуется.

Прикладное программное обеспечение:
 - хранится на файловом сервере,
 - используется только в оригинале,
 - дорабатывается в процессе эксплуатации (в части `CI/CD`) без уведомления пользователей.

Выпуск релизов и пакетов не предусматривается.
Программное обеспечение на распространяется, хранится на инфраструктуре серверов.

(первоначальное, август 2016-го года) `[Рисунок 1]`
![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

Поправки:
 - С **tk**, **ttk** переделали на **pyQt**,
 - **Gtk** применялась в `Linux`-е (библиотека **pyGTK** на `Windows` сейчас пока не ставится),
 - `Linux` может использоваться на клиентах для правки справочников (выходит из употребления на клиентах из-за запаздывания в написании и функционале драйверов),
 - (*) Сайт на **WEB-сервере** разрабатывается отдельно и в объем данного проекта не входит.

Файлы, открываемые только в своем ПО, желательно не использовать.

#### История изменений и улучшений в проекте

Версия 3 (устарела):
 - были ошибки в загрузке данных (в объектах перепутали коды `IATA` и `ICAO`) - исправили, но база данных с ошибкой, оставили как есть,
 - образец наработок,
 - источник первичных данных и для анализа.

Версии 4, 5 (теперь не актуальны, медленные, сильно загружает процессор сервера СУБД):
 - исправлены ошибки версии 3,
 - версия 5 предназначена для проверки правильности транзакций загрузки данных в версии 4 - результаты сошлись, все правильно,
 - добавили обход взаимоблокировок с помощью обработки исключения и нарастающей временной задержке,
 - у летательных аппаратов регистрация и авиакомпании не указываются,
 - авиарейсы плюсуются без даты.
 
Версия 6 (текущая, теперь не актуальна):
 - авиарейсы вставляются по датам,
 - у летательных аппаратов обновляется регистрация и авиакомпания-оператор крайнего авиарейса,
 - удачно проиндексировали поля в таблицах (загрузка ускорилась в 25 ... 35 раз, простои на взаимоблокировках уменьшились).
 
Версия 7 (разработка пока на паузе, наработки переносятся в версию 8):
 - у летательных аппаратов по принципу _медленно меняющейся размерности_ сделана хронология регистраций
   (бизнес-ключ - сочетание заводских номеров, суррогатный ключ - регистрации по периодам использования соответственно),
 - а также сделана хронология авиакомпании-оператора, авиакомпании-владельца, авиакомпании-арендатора, авиакомпании-лизингодателя
   (бизнес-ключ - тот же, суррогатные ключи - авиакомпании по периодам использования соответственно) через промежуточные справочные таблицы.

Версия 8 (в процессе разработки):
 - у летательных аппаратов хронология регистраций и авиакомпаний пишется в XML-ных полях
   (если в базе данных у летательных аппаратов нет регистрации, используем функционал версии 7 для временного хранения недозагруженных данных,
   подробнее см. "Загрузка данных" ниже по тексту), 
 - у авиакомпаний список аэропортов-хабов сделан XML-ным полем,
 - у объекта описание сделано XML-ным полем (структура разделов и подразделов),
 - убрали отдельную базу данных по летательным аппаратам,
 - добавили отношения, индексы, XSD-схемы, каскадные правила на удаления и обновления,
 - подняли очередь и службу [**Service Broker**](https://docs.microsoft.com/ru-ru/sql/database-engine/configure-windows/sql-server-service-broker?view=sql-server-ver15), см. [статью](https://docs.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/monitor-database-deadlocks),
   чтобы не пользоваться временными задержками для ухода от взаимоблокировок, но функционала SQL-ных скриптов внутри хранимых процедур не хватает,
   ищем решение как разнести сложность, пробуем разные серверные курсоры внутри хранимых процедур см. [статью](https://docs.microsoft.com/ru-ru/sql/relational-databases/native-client-odbc-cursors/implementation/odbc-cursor-library?view=sql-server-ver15), а также [статью](https://docs.microsoft.com/ru-ru/sql/t-sql/language-elements/declare-cursor-transact-sql?view=sql-server-ver15),
 - для экспериментов используем не тестовую базу, а только тестовые таблицы
   (делаем трансфер двух таблиц соответственно в две тестовые таблицы, можно перенести отдельной файловой группой на отдельный HDD).

Справочники и данные

Считаем, что авиакомпания однозначно определяется сочетанием кодов `IATA` и `ICAO` и что любая авиакомпания (в том числе неизвестный частный владелец `IATA - пусто`, `ICAO - пусто`) может быть:
 - оператором,
 - владельцем (арендатором),
 - арендодателем,
 - лизингодателем.

Считаем, что:
 - самолет однозначно определяется сочетанием его заводских номеров `LN`, `MSN`, `SN`, `CN` в зависимости от фирмы-изготовителя,
 - регистрационный номер самолета (англ. _Tail Number_, далее по тексту **регистрация**) с течением времени может последовательно несколько раз переходить от одного самолета к другому,
 - самолет за время эксплуатации может несколько раз изменить свой регистрационный номер. 

В данных используется:
 - регистрация самолета,
 - дата авиарейса,
 - обозначение авиарейса,
 - код `IATA` объекта вылета,
 - код `IATA` объекта прилета,
 - число ходок
   и остальные данные в зависимости от источника.
 
Например, авиакомпания может:
 - владеть одними самолетами,
 - быть оператором для других самолетов,
 - давать в лизинг третьи самолеты,
 - арендовать четвертое множество самолетов.

Например самолет может быть:
 - в лизинге у одной компании,
 - работать на авиарейсах другой.

И ситуация у авиакомпаний и по самолетоам время от времени меняется.

Считаем, что авиарейс может выполнять:
 - собственно авиакомпания-владелец (нет оператора, нет аренды, нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-владельца (нет аренды и нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора (нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора, арендодатель которой взял его в лизинг.

В исходных данных для гражданских дается регистрация, для служебных дается заводской серийный номер.
Источники информации - переписки на форумах. Ссылки не даю, так как через время при переходе по ним выбирает **404**. 

Загрузка данных:
 - обновляет XML-ные поля авиакомпаний **XML(CONTENT dbo.XSD-схема)** в таблице летательных аппаратов,
   которые подаются на вход хранимой процедуры через XSD-схему и парсятся как **SAX**,
   используя комплектный функционал [**XPath & XQuery**](http://xmlhack.ru/texts/03/xquery/what.is.xquery.html) и спецификацию **SQL/XML**,
 - вставляет строки в таблице аэропортов,
 - вставляет строки в таблице маршрутов,
 - вставляет или обновляет строки в таблице авиарейсов

следующим образом:
 - парсим в таблице летательных аппаратов XML-ное поле регистрации (первичный XML-ный индекс),
 - выбираем строку, у которой временной диапазон с указанной регистрацией соответствует дате авиарейса,
 - если строки с подходящим временным периодом не найдено (это может случиться, если дата авиарейса новее, чем все временные диапазоны с указанной регистрацией),
   данные пишем во временную таблицу по образцу 7-й версии (см. [История изменений и улучшений в базах данных](https://github.com/tsv19su254052/LoadWorkData-GUIs-and-Utilities#%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D0%B8%D0%B7%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B8-%D1%83%D0%BB%D1%83%D1%87%D1%88%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5)),
 - формируем список соответствия регистраций и дат авиарейсов например в виде отдельной таблицы, которые надо восполнить в базе данных,
 - после восполнения переносим данные из временной таблицы к остальным данным,
 - если в XML-ном поле авиакомпании нет,
   вставляем относительно корневого тэга новый тэг с указанным аттрибутом-идентификатором авиакомпании (как внешний ключ авиакомпании)
   и новый подтэг с датой авиарейса (как начало нового временного диапазона),
 - если в XML-ном поле авиакомпания есть, к существующим подтэгам в соответствии с хронологией добавляем новый подтэг с датой авиарейса,
 - подтэги дополнительно группируем по отдельному алгоритму (см. ниже "Группировка подтэгов ..."),
 - если регистрация в данных не указана, то в таблицу летательных аппаратов изменения не вносим,
 - если объекта, указанного в данных нет, вставляем новый объект,
 - если маршрута между объектами, указанными в данных, еще нет, вставляем новый маршрут,
 - если авиарейса с параметрами, указанными в данных нет, вставляем новый авиарейс,
 - если авиарейс с параметрами, указанными в данных уже есть, плюсуем количество этого авиарейса.

Группировка подтэгов с датами авиарейсов (пока в разработке):
 - группируем подтэги программно при изменении,
 - API-шки пишем те же и еще пишем такие же на [**SQLAlchemy**](https://docs.sqlalchemy.org/en/14/dialects/mssql.html) под MS SQL Server,
 - во всех его строках переставляем подтэги по хронологии и отбрасываем промежуточные подтэги,
 - пробуем вручную SQL-ные запросы со вставками на `XPath & XQuery`,
 - сохраняем вставки на `XPath & XQuery` файлами запросов `*.xq`,
 - вызываем вставки в запросах программно по URL,
 - вызываем вручную из диалога открытия файла,
 - пробуем хранимые процедуры с программными вызовами вставки,
 - вставляем старую XML-ную базу летательного аппарата (не более 2 Гбайт на каждую согласно документации `msdn.com`)
   в XML-ное поле **XML(CONTENT dbo.XSD-схема)** его строки и парсим его как [**DOM**](https://stackoverflow.com/questions/192907/xml-parsing-elementtree-vs-sax-and-dom) , см. [статью](https://stackoverflow.com/questions/1890923/xpath-to-fetch-sql-xml-value) , а также [статью](https://stackoverflow.com/questions/43848456/t-sql-xquery-value-of-attribute-y-where-attribute-x-is-known) внутри скрипта на Python-е [**Saxon**](https://www.saxonica.com/technology/xslt-and-xquery.xml)-ом библиотеки `libxml2` (есть `libxml2dom`, `libxml-python`, `libxml-python3`), `libxslt` (пока нету).

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC.
При вызове хранимой процедуры используются серверные курсоры.
Хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно
(бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки).
Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Для обхода попадания на вложенную обработку исключений на клиентах:
 - установить или обновить **Драйвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`, версия 18 не работает с СУБД версии 11),
 - поднять **Системный DSN** в источниках данных ODBC (см. `Подключение к БД через системный DSN` на сервере в папке проекта `..\SQL & XML (XPath & XQuery XSD XDR XSLT)`).

#### Объемы доработок на клиентах

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней,
ссылаться на их фото на сайте [jetphotos.com](https://www.jetphotos.com) (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойтсв авиакомпаний виджеты и ссылки просмотра финансовой и юридической информации из надежной онлайн базы.

Добавить на графической формочке свойств объектов:
 - поиск по названию объекта в выпадающем списке с автодополнением из уже имеющихся названий объектов в базе данных,
 - добавить виджеты на вкладке ВПП (широта, долгота, абсолютная отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.),
 - виждеты выбора страны, области (графства, штата, региона), города, района города из надежной онлайн базы на ее API-шках в формате XML
   (см. [простой пример](https://htmlweb.ru/geo/api_get_data.php) ),
   надо зарегистрироваться, купить и оплачивать API-ключ согласно [тарифа](https://htmlweb.ru/user/tariffs.php) для каждого клиента,
   а также см. [здесь](https://www.maxmind.com/en/worldcities) , а также [здесь](http://www.geonames.org) , [здесь](http://netload.biz/2011/01/24/geoip3) и [здесь](https://pear.php.net/manual/en/package.webservices.services-geonames.examples.php) ,
   значение подтэга `wiki` вынести отдельно гиперссылкой, чтобы открывать статью из `WikiPedia.org`,
 - виджеты и ссылки для просмотра свойств вышеперечисленных географических объектов.

На сайте (см. (*) [выше](https://github.com/tsv19su254052/LoadWorkData-GUIs-and-Utilities/blob/Developing_v7/README.md#%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%BE%D0%B5-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE%D0%B5-%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5)) показать маршруты в виде их профилей на топологии с привязкой к [карте Google](https://www.google.com/maps) , опираясь на аналитику баз данных.

Остальные указания и замечания см.:
 - в исходниках по тэгам **todo** и **fixme**,
 - в [обсуждениях](https://github.com/tsv19su254052/LoadWorkDataAirFlightsDBNew/issues) ,
 - комментарии в исходниках.
