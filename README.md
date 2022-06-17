#### Назначение

Некоторые сводные наработки по:
 - авиационному процессингу,
 - телеметрии,
 - телематике.

#### Описание

В объем данного проекта входит:
 - разработка баз данных (справочные, рабочие и оперативные данные) на внешнем сервере СУБД,
 - разработка прикладного программного обеспечения - утилит и графических оболочек (в части UX/UI) - для работы с ними,
 - администрирование серверов и баз данных на них,
 - первичная аналитика баз данных,
 - предоставление способа взаимодействия с другими проектами с помощью API-шек.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, вертодромы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные загружаются с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

Оперативные данные загружаются асинхронно на API-шках или по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования без учета хронологии.

Структура хранилища с базами данных - **Снежинка** (в центре - таблицы с рабочими и оперативными данными (далее по тексту **данными**),
с краев - таблицы со справочными данными (далее по тексту **словарями**).
Таблица летательных аппаратов гибридная и содержит:
 - поля, которые правятся только вручную,
 - поля, которые заполняются в процессе загрузки данных.

Модель восстановления баз данных - **Полная**, так как предусматривается одновременная работа множества клиентов и в хранимых процедурах используются помеченные транзакции.
Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия клиентов ставим на паузу до уведомления о возобновлении работы.

Инфраструктура:
 - сервер СУБД, 
 - файловый сервер,
 - терминальный сервер - работают по учеткам Windows без контроллера домена.

Права пользователей на доступ к базам данных соответсвуют их учеткам Windows на сервере СУБД.

Работа клиентов возможна в локальной подсети или из внешней сети через рабочий стол терминального сервера по RDP.

Прикладное программное обеспечение:
 - хранится на файловом сервере,
 - используется только в оригинале,
 - дорабатывается в процессе эксплуатации (в части CI/CD) без уведомления его пользователей.

Выпуск релизов и пакетов не предусматривается, так как программное обеспечение на распространяется. 

(первоначальное, август 2016-го года) `[Рисунок 1]`
![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")

Поправки:
 - С **tk**, **ttk** переделали на **pyQt**,
 - **Gtk** применялся в Linux-е (библиотека **pyGTK** на Windows сейчас не ставится),
 - Linux может использоваться на клиентах для правки справочников,
 - (*) Сайт на **WEB-сервере** разрабатывается отдельно и в объем данного проекта не входит.

###### Хранение информации в файлах различных типов и их использование `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)

Файлы, открываемые только в своем ПО, желательно не использовать.

###### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

#### История изменений и улучшений в проекте

Версия 3 (устарела):
 - были ошибки в загрузке данных (в объектах перепутали коды IATA и ICAO),
 - оставили как есть,
 - образец наработок,
 - источник первичных данных и для анализа.

Версии 4, 5 (теперь не актуальны, медленные, сильно загружает процессор сервера СУБД):
 - исправлены ошибки версии 3,
 - 5-ая версия предназначена для проверки правильности загрузки данных в 4-ой версии,
 - добавили обход взаимоблокировок на нарастающих временных задержках,
 - у летательных аппаратов регистрация и авиакомпании не указываются,
 - авиарейсы плюсуются без даты,
 
Версия 6 (текущая, теперь не актуальна):
 - авиарейсы вставляются по датам,
 - у летательных аппаратов обновляется регистрация и авиакомпания-оператор крайнего авиарейса,
 - удачно проиндексировали поля в таблицах (загрузка ускорилась в 25 ... 35 раз, простои на взаимоблокировках уменьшились),
 
Версия 7 (разработка пока на паузе, наработки переносятся в версию 8):
 - у летательных аппаратов по принципу _медленно меняющейся размерности_ сделана хронология регистраций
   (бизнес-ключ - сочетание заводских номеров, суррогатный ключ - регистрации по периодам использования соответственно),
 - а также сделана хронология авиакомпании-оператора, авиакомпании-владельца, авиакомпании-арендатора, авиакомпании-лизингодателя
   (бизнес-ключ - тот же, суррогатные ключи - авиакомпании по периодам использования соответственно) через промежуточные справочные таблицы, 

Версия 8 (в процессе разработки):
 - хронология регистраций и авиакомпаний пишется в XML-ных полях,
 - убрали отдельную базу данных по летательным аппаратам,
 - если в базе данных нет регистрации, использует функционал версии 7 для временного хранения недозагруженных данных (подробнее см. ниже по тексту), 
 - добавили отношения, индексы, XSD-схемы, каскадные правила на удаления и обновления,
 - для экспериментов используем не тестовую базу, а только тестовые таблицы
   (бэкап не раскатываем, а делаем трансфер двух таблиц в две тестовые таблицы,
   можно перенести отдельной файловой группой на отдельный HDD).

#### Справочники и данные

Летательный аппарат однозначно определяется сочетанием его заводских номеров LN, MSN, SN, CN в зависимости от фирмы-изготовителя.

Регистрационный номер летательного аппарата (англ. _Tail Number_, далее по тексту **регистрация**)
с течением времени может последовательно несколько раз переходить от одного летательного аппарата к другому.

В данных используется:
 - регистрация,
 - дата авиарейса,
 - строка авиарейса,
 - код IATA объекта вылета,
 - код IATA объекта прилета,
 - число ходок с этим авиарейсом
   и остальные данные в зависимости от источника.
 
Считаем, что любая авиакомпания (в том числе неизвестный частный владелец `IATA - пусто`, `ICAO - None`) может быть:
 - оператором,
 - владельцем (арендатором),
 - арендодателем,
 - лизингодателем.

Считаем, что авиарейс может выполнять:
 - собственно авиакомпания-владелец (нет оператора, нет аренды, нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-владельца (нет аренды и нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора (нет лизинга),
 - авиакомпания-оператор на летательном аппарате авиакомпании-арендатора, арендодатель которой взял его в лизинг.

Загрузка данных:
 - обновляет XML-ные поля авиакомпаний **XML(CONTENT dbo.XSD-схема)** в таблице летательных аппаратов,
   которые подаются на вход хранимой процедуры через XSD-схему и парсятся как **SAX**,
   используя комплектный функционал **XPath & XQuery** и спецификацию **SQL/XML**,
 - вставляет строки в таблице объектов,
 - вставляет строки в таблице маршрутов,
 - вставляет или обновляет строки в таблице авиарейсов

следующим образом:
 - парсим в таблице летательных аппаратов XML-ное поле регистрации (первичный XML-ный индекс),
 - выбираем строку, у которой временной диапазон с указанной регистрацией соответствует дате авиарейса,
 - если строки с подходящим временным периодом не найдено (это может случиться, если дата авиарейса новее, чем все временные диапазоны с указанной регистрацией),
   данные пишем во временную таблицу по образцу 7-й версии (см. "История изменений и улучшений в базах данных" в разделе "Версия 7"),
   формируем список соответствия регистраций и дат авиарейсов например в виде отдельной таблицы, которые надо восполнить в базе данных,
   после восполнения переносим данные из временной таблицы к остальным данным,
 - если в XML-ном поле авиакомпании нет,
   вставляем относительно корневого тэга новый тэг с указанным аттрибутом-идентификатором авиакомпании (как внешний ключ авиакомпании)
   и новый подтэг с датой авиарейса (как начало нового временного диапазона),
 - если в XML-ном поле авиакомпания есть,
   к существующим подтэгам в соответствии с хронологией добавляем новый подтэг с датой авиарейса,
 - подтэги дополнительно группируем по отдельному алгоритму (см. ниже "Группировка подтэгов ..."),
 - если регистрация в данных не указана, то в таблицу летательных аппаратов изменения не вносим,
 - если объекта, указанного в данных нет, вставляем новый объект,
 - если маршрута между объектами, указанными в данных, еще нет, вставляем новый маршрут,
 - если авиарейса с параметрами, указанными в данных нет, вставляем новый авиарейс,
 - если авиарейс с параметрами, указанными в данных уже есть, плюсуем количество этого авиарейса.

Группировка подтэгов с датами авиарейсов (пока в разработке):
 - пробуем вручную SQL-ные запросы со вставками на `XPath & XQuery`,
 - вызываем вручную из диалога открытия файла по фильтру `*.xq`,
 - вызываем программно по URL из файлов `*.xq`,
 - пробуем хранимые процедуры с вызовами из внешних файлов,
 - вставляем XML-ную базу по летательному аппарату в XML-ное поле **XML(CONTENT dbo.XSD-схема)** его строки,   
 - в остальных строках переставляем подтэги по хронологии и отбрасываем промежуточные подтэги **Saxon**-ом (библиотеки `libxml2`, `libxslt`),
 - определяемся в каких случаях по необходимости программно или вручную выполняем группировку.

Запросы на `XPath & XQuery` правим внутри `Management Studio` (без подсветки синтаксиса и автодополнения),
сохраняем файлами типа `*.xq` и вызываем внутри хранимых процедур и SQL-ных скриптов.

Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего.

###### Собираем **XML**-ные поля, определяемся с их структурой

![SSMS Делаем XML-ные поля](https://user-images.githubusercontent.com/104857185/173250391-229e37c8-c996-4d22-bf0f-7df07d0845b0.png)

В XML-ном поле регистрации может быть только один тэг с **аттрибутом-строкой**, обозначающим какую-то одну регистрацию.
Начало временного диапазона со следующей регистрацией считаем окончанием временного диапазона использования с предыдущей.
Заполняем только ручным вводом.

В каждом XML-ном поле авиакомпании может быть только один тэг с **аттрибутом-идентификатором**, указывающим на какую-то одну авиакомпанию.
Начало временного диапазона в следующей авиакомпании считаем окончанием временного диапазона использования в предыдущей.
Аттрибуты-идентификаторы в разных XML-ных полях могут указывать на одну и ту же авиакомпанию (см. выше 2 абзаца "Считаем, что ...").

###### Собираем **XSD-схему** (устарело, как пример) 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)

В начале XSD-схемы объявляются:
 - типовые и ссылочные схемы,
 - типовые, ссылочные и пользовательские пространства имен (см. https://www.w3.org/TR/xmlschema11-1/),
 - типовые, ссылочные и пользовательские типы данных XPath & XQuery.

Далее в XSD-схеме определяются элементы, каждый под своим именем (см. https://www.w3schools.com/xml/schema_simple.asp).

Элемент генерируется из XML-ного файла внутри `Management Studio` или с помощью XSLT-преобразования
(см. https://docs.microsoft.com/ru-ru/visualstudio/xml-tools/how-to-execute-an-xslt-transformation-from-the-xml-editor?view=vs-2022) 
и вставляется в соответствии с порядком просмотра XML-ных полей. В сложных случаях можно пользоваться **Schematron**-ом. 
Имя корневого тэга XML-ного поля соответствует имени элемента XSD-схемы.
Исходный текст XSD-схемы вставляется в SQL-ный скрипт ее привязки к базе данных
(надо найти способ не вставлять исходник схемы через буфер обмена, а выбирать ее в диалоге открытия файла или дать URL до нее `file:///P:/...`).
К базе данных можно привязать несколько XSD-схем.
К каждому XML-ному полю можно привязать свою XSD-схему.

###### Привязываем XSD-схему к базе данных

![SSMS Сборка XSD-схемы](https://user-images.githubusercontent.com/104857185/174197029-1815510f-f813-4244-8b73-d79f40e28064.png)
 
#### Поправки по терминологии:
 - **Коллекцию схем XML** в Management Studio точнее называть XSD-схемой.
 - **Созданием схемы** в SQL-ном скрипте правильнее называть привязкой XSD-схемы, потому что она уже собрана и сохранена файлом типа `*.xsd`.
 - **DTD-схемы** и **XDR-схемы** кратко упомянуты в `msdn.com`
   (см. https://docs.microsoft.com/ru-ru/visualstudio/xml-tools/how-to-create-an-xml-schema-from-an-xml-document?view=vs-2022),
   но уже не применяются.

XML-ные поля пропускаются через XSD-схему:
 - программно на входе хранимой процедуры,
 - программно при вставке или при обновлении строки,
 - при редактировании XML-ного файла с привязкой к XSD-схеме внутри Management Studio,
 - при ручном вводе XML-ного поля при вызове хранимой процедуры внутри Management Studio.

Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется
обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения,
так как сервер СУБД не дает обратные вызовы (вэб-хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты.
Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД.
Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами.
Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия.
Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных
(см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него).
Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года
и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %,
а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 25 ... 35 % благодаря удачно проиндексированным полям в таблицах.
Траффик по локальной подсети увеличивается из-за перезапросов. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC.
При вызове хранимой процедуры используются серверные курсоры.
Хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только средствами SQL сложно
(бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки).
Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Для обхода попадания на вложенную обработку исключений на клиентах:
 - установить или обновить **Драйвер ODBC для MS SQL** (дистрибутив версии 17 и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`),
 - поднять **Системный DSN** в источниках данных ODBC (см. `Подключение к БД через системный DSN` на сервере в папке проекта `..\SQL & XML (XPath & XQuery XSD XDR XSLT)`).

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

#### Объемы доработок

Найти способ не вставлять исходник XML-ного файла в строке ввода в диалоге хранимой процедуры внутри Management Studio через буфер обмена,
а выбирать его в диалоге открытия файла или дать URL до него `file:///P:/...`.

Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку на каждый в Wikipedia.

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней,
ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия).

Добавить на графической формочке свойств объектов поиск по названию объекта в выпадающем списке с автодополнением из уже имеющихся названий объектов в базе данных,
добавить виджеты на вкладке ВПП (широта, долгота, абсолютная отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.),
ссылку по объекту на статью в Wikipedia.

Для подписания и утверждения внесения изменений в справочные данные предусмотреть использование **сертификата (ЭЦП)** на USB-ом токене.
Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (пока уточняется). Требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме.

На сайте (см. (*) выше) показать маршруты в виде их профилей на топологии с привязкой к карте на https://www.google.com/maps , опираясь на аналитику баз данных.

Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
