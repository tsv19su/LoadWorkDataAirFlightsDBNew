# LoadWorkDataAirFlightsDBNew

#### Общее описание
Некоторые сводные наработки по:
 - авиационному процессингу,
 - телематике,
 - телеметрии,
 - логистике.

Справочные, рабочие и оперативные данные в SQL-ных базах данных **MS SQL Server**-а.

Справочные данные:
  - объекты (аэропорты, аэродромы, авиабазы, взлетные полосы и хелипады),
  - авиакомпании,
  - летательные аппараты

использовались из источников:
 - http://apinfo.ru 
 - http://openflights.org
 - http://www1.ourairport.com/ (в России не открывается)
 - http://planelist.net
 - http://www.flightradar24.com
 - https://www.jetphotos.com/

Рабочие данные по авиаперелетам загружались с https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr

#### Архитектура ПО (первоначальная август 2016-го года) `[Рисунок 1]`

![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg "Решение по архитектуре")
Поправки:
 - С **tk** и с **ttk** переделали на **pyQt**,
 - **Gtk** применяется в Linux-е (библиотека **pyGTK** на Windows сейчас не ставится),
 - (*) Сайт на WEB-сервере разрабатывается отдельно и в объем данного проекта пока не входит

#### Хранение информации в файлах различных типов `[Рисунок 2]`

![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
_Файлы, открываемые только в своем ПО, желательно не использовать_

----
Предусматривается:
 - разработка баз данных и администрирование сервера СУБД в Management Studio,
 - работа клиентов на графических формах (в части UX/UI) в локальной подсети или по RDP из внешней сети по учеткам Windows Server-ов без контроллера домена, с заранее заданной конфигурацией сервера СУБД (имена входа, их права) и с ПО в оригинале с файлового сервера, которое дорабатывается в процессе работы (в части CI/CD) без уведомления клиентов

#### Отчеты по базам данных из Management Studio

![СУБД Полная - Простая - Сжатие - Полная 001 002](https://user-images.githubusercontent.com/37275122/168450352-48a1e7e1-eeb4-4227-b744-2d368fccac32.png)

![СУБД Полная - Простая - Сжатие - Полная 001 003](https://user-images.githubusercontent.com/37275122/168450358-630fa494-2c0f-4bad-afb1-42bdb44325ec.png)

![СУБД Полная - Простая - Сжатие - Полная 001 004](https://user-images.githubusercontent.com/37275122/168450362-8de3b141-e670-4067-a28e-544cd9cff239.png)

![СУБД Полная - Простая - Сжатие - Полная 001 005](https://user-images.githubusercontent.com/37275122/168890832-25179657-69dd-47e9-8bac-63e5ac56715e.png)

----
Для обхода попадания на вложенную обработку исключений на клиентах:
 - установить или обновить **двайвер ODBC для MS SQL** до версии 17 (дистрибутив и руководство см. на сервере в папке `Q:\M$_Windows\SQL_Server\Driver ODBC for SQL Server`).
 - в источниках данных ODBC настроить **Системный DSN** (см. "Подключение к БД через системный DSN" на сервере в папке проекта `..\Руководства в картинках`)
 
Уход от взаимоблокировок при загрузке рабочих и оперативных данных с нескольких внешних клиентов на сервер СУБД выполняется обертыванием тела цикла попыток с нарастающей задержкой по времени в обработку исключения, так как сервер СУБД не дает обратные вызовы (хуки или программные прерывания) клиентам на повторную попытку, если запрашиваемые данные пока заняты. Без обратных вызовов пока не получается эффективно задействовать внешний сервер СУБД. Транзакции сделаны короткими, но между ними все перезапрашивается снова, так как данные изменяются другими клиентами. Потери времени на задержках частично уменьшены путем уточнения уровня изоляции транзакции в зависимости от действия. Число перезапросов и их перенос по времени пишутся в журнал загрузки рабочих данных (см. `LogReport_DBNew6.txt` в папке проекта на сервере, `ErrorLog.txt` там же - ошибки дозаписи в него). Начальное значение задержки по времени и шаг ее приращения подобран экспериментально по результатам нагрузочных тестов осенью 2019-го года и зависит от вычислительных характеристик сервера СУБД. При 2-х кратном увеличении количества клиентов задержки увеличиваются на 15 ... 20 %, а нагрузка на сервер СУБД (процессор, HDD) уменьшается на 15 ... 20 % благодаря удачно проиндексированным полям в таблицах. Пропускная способность локальной подсети достаточная.

Каждый клиент использует непрерывное подключение с несколькими клиентскими статическими однопроходными непрокручиваемыми API-курсорами ODBC. При вызове хранимой процедуры используются серверные курсоры. Но хранимые процедуры применяются мало, потому что по мере усложнения прикладного функционала выполнить его только на SQL сложно (бедность типов данных и синтаксиса, сложность передачи и возврата составных типов данных, пока нет способа возврата результата и причины несработки). Уровни изоляции транзакции курсоров уточнены и проверены под нагрузкой на 4-х тестовых базах данных летом и осенью 2019-го года.

Контроль подключения и его восстановление при разрыве (например, при плохом контакте на коннекторах, через Wi-Fi или через мобильный Интернет) не предусматривается.

Модель восстановления баз данных - **ПОЛНАЯ**, так как в хранимых процедурах используются помеченные транзакции. Обслуживание баз данных (целостность, индексы, бэкапы) делается обычным способом - на время все действия завершаются до уведомления о возобновлении работы.

Загрузка рабочих и оперативных данных выполняется в отдельном потоке и не требует соответствия хронологии

----
#### Объемы доработок (вступительная часть):

Уточнить применение комплектного с **MS SQL** функционала **XPath & XQuery** и комплектной спецификации **SQL/XML**, чтобы парсить поля **XML(CONTENT dbo.XSD-схема)** как **DOM** в таблицах баз данных.

Доработать базу данных по летательным аппаратам таким образом, чтобы:
 - писать в нее арендодателей, лизингодателей, арендаторов (владельцев) и всех операторов по XML-ному полю на каждую авиакомпанию для каждого авиарейса в разных комбинациях, как внешний ключ, ссылающийся на соответствующую запись в таблице авиакомпаний,
 - при необходимости писать новую ветку и подветку или дописывать в существующую ветку новую подветку по указанному аттрибуту (авиакомпании) с указанием даты,
 - группировать подветки в соответствии с хронологией,
 - убирать предыдущие подветки, если они оказываются внутри временного диапазона в одной авиакомпании,
 - вынести запись или обновление каждого XML-ного поля в хранимую процедуру вместе с частью на XPath & XQuery для облегчения отладки. 

Таким образом, считаем, что:
 - в каждом поле ветка одной авиакомпании должна быть только одна,
 - в каждой ветке может быть несколько подветок с датами по количеству периодов использования в данной авиакомпании (начало периода),
 - начало периода использования в следующей авиакомпании совпадает с окончанием периода использования в предыдущей, так как в рабочих данных не указаны периоды бездействия.
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины). Недостаток XSD-схемы - тот же и тот, что она пропускает все или не пропускает ничего. Как обычно, просто фиксируем и записываем отказ этого действия в журнал для анализа. 

#### Делаем **XML**-ное поле

![Таблица с полем типа xml с привязкой к схеме xsd](https://user-images.githubusercontent.com/104857185/167261417-e0820f3d-965f-4124-9af6-e59994e09f46.png)

#### Делаем схему на все **XML**-ные поля и привязываем ее к ручному вводу данных в **XML** 

![SSMS - XML-код - Создать схему](https://user-images.githubusercontent.com/104857185/167261451-a42a0c66-2888-4042-88a2-679f1ef6549a.png)
_Поправка:
То, что в Management Studio называется коллекцией схем XML, точнее называть XSD-схемой. Генерируется из XML или добавляется скриптом - только *.xsd_
 
Дополнить структуру базы данных по авиакомпаниям (история, владельцы и остальное). Соответственно выбрать способ работы с ними для клиентов. Добавить ссылку на нее с Wikipedia

Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio). Добавить ссылку с Wikipedia

Сделать графическую формочку для правки свойств летательных аппаратов и уточнить набор виджетов на ней, в том числе их фото (выделить таблицы с мультимедийными полями в отдельную файловую группу, которую вынести на дисковую полку "холодного хранения") или ссылаться на их фото на https://www.jetphotos.com (присутствуют немодерирруемые несоответствия)

Добавить на графической формочке свойств объектов поиск объекта по названию в базе данных с выпадающим списком с автодополнением

Добавить на графической формочке для правки свойств объектов виджеты на вкладке ВПП (широта, долгота, абс. отметка, длина, ширина, покрытие полос, оснащение системой сближения и посадки и т. д.), ссылку по объекту на Wikipedia, поиск по наименованию в виде выпадающего списка (требуется интеграция с поиском Google-а)

Добавить возможность разрешения на внесение изменений в базы данных исполнителями через удостоверение пользователей **сертификатом (ЭЦП)** на USB-ом токене, а также подписание извещения на внесение изменений перед их внесением главным специалистом **сертификатом (ЭЦП)** на USB-ом токене. Предусмотреть возможность вывода истории внесения изменений с указанием подписантов (требуются **DDK** или **SDK** от фирмы-изготовителя USB-вых токенов для добавления диалога открытия содержимого токена и выбора на нем требуемого сертификата в пользовательском режиме)

Дополнить данные по маршрутам их профилями и топологиями с привязкой к картам Google, а также их изменениями с течением времени

Разработать асинхронную загрузку оперативных данных на API-шках по ВЭБ-хукам с http://www.flightradar24.com и с первичного оборудования

Выполнить визуализацию части данных на ВЭБ-сайте ВЭБ-сервера в этой же локальной подсети

Проанализировать базы данных с целью дальнейшего улучшения ее производительности с нескольких клиентов в локальной подсети.
 
----
Остальные замечания см. в исходниках по тэгам **todo** и **fixme**
