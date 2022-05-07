![93936369_591194488270382_464298759405174784_n](https://user-images.githubusercontent.com/104857185/167257457-d5fc8393-4bdc-4391-a76d-9b2b73490016.jpg)
![1 001 001](https://user-images.githubusercontent.com/104857185/167037090-9cd548c0-9643-4903-adce-13e2a039226d.jpg)
# LoadWorkDataAirFlightsDBNew

Наработки по:
 - авиационному процессингу,
 - телематике,
 - телеметрии.

Справочные, рабочие и оперативные SQL-ные базы данных на MS SQL Server-е согласно имен входа и их прав доступа.

Справочные данные по:
  - объектам (аэропортам, аэродромам, авиабазам, взлетным полосам и хелипадам),
  - авиакомпаниям,
  - летательным аппаратам
 
----
Для обхода попадания на обработку вложенных исключений на клиентах:
 - настроить в источниках данных системный DSN (см. "Подключение к БД через системный DSN" в папке "Руководства в картинках"),
 - поставить двайвер ODBC для MSSQL версии 17.
 
Уход от взаимоблокировок при чтения/записи СУБД сделан с помощью обертывания цикла попыток с нарастающей задержкой в обработку исключения, потому что сервер СУБД на дает обратные вызовы (хуки или паузы до прерывания) клиентам на повторную попытку.

Поэтому при интенсивных запросах к СУБД на ожидании теряется 15 ... 20 % времени.

Начальное значение задержки по времени и шаг ее увеличения выбран экспериментально по результататм тестов и зависит от вычислительных характеристик сервера.

Модель восстановления баз данных - ПОЛНАЯ, так как в хранимых процедурах используются помеченные транзакции.

----
Доработать базу по летательным аппаратам таким образом, чтобы писать в нее:
 - арендодателей (необязательно),
 - арендаторов (владельцев),
 - операторов
в полях XML(CONTENT XSD-схема), парсить их как DOM по веткам и подветкам и при необходимости дописывать подветки по указанному аттрибуту с указанной датой например с помощью хранимой процедуры.
Недостаток хранимой процедуры - не возвращает в скрипты на Python-е результат своей работы (получилось, не получилось с указанием причины).
Недостаток XSD-схемы - тот же.
 
Дополнительно:
 - Надо применить комплектый с MS SQL функционал XPath & XQuery, чтобы нормально парсить XML-ные поля
 - Сделать графическую формочку для правки свойств альянсов (или делать это внутри Management Studio)
 - Сделать графическую формочку для правки свойств летательных аппаратов и доработать набор виджетов на ней
 - Добавить виджетов на вкладке свойств объекта, а также доработать вкладку ВПП со всеми свойствами (широта, долгота, абс. отметка, длина, ширина и т. д.)
 - Сделать удостоверение пользователей по сертификату (ЭЦП) на USB-ом токене

Пока работа клиентов предусматривается через терминальный сервер внутри инфраструктуры с СУБД по учеткам Windows Server-ов без контроллера домена и с заранее сделанной конфигой сервера СУБД
 - все пользователи работают с одной версией интерпретатора,
 - все пользователи работают с одним набором библиотек,
 - экономия ресурса серверов

Остальные замечания в исходниках см. по тэгам todo и fixme
