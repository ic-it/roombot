<h1 align="center"> RoomBot </h1>
<p align="center">Библиотека для интуитивно понятного взаимодействия с пользователем</p>
<a href="https://www.repostatus.org/#abandoned"><img src="https://www.repostatus.org/badges/latest/abandoned.svg" alt="Project Status: Abandoned – Initial development has started, but there has not yet been a stable, usable release; the project has been abandoned and the author(s) do not intend on continuing development." /></a>


## Основные концепции:
* Пользователь всегда находится в какой-то комнате.
* У пользователя есть права и он имеет доступ только к чётко выделенным областям программы.

Что такое комната?
Это условно список функций, объединённых одним именем, которые будут последовательно выполнятся при наличии у пользователя должных прав или соблюдения условий:

* подходящего типа сообщения
* положительный ответ функции "фильтра"

<h2 align="center"> Главные Компоненты </h2>

- ### RoomsManager
	- Главный класс, который используется для связи всех компонентов
- ### RoomsContainer
	- Класс, который хранит комнаты.

<h2 align="center">Интерфейсы и реализации по умолчанию</h2>

- ### IDatabase и IUsersTable
	- Компоненты, которые являются основными для взаимодействия с бд.
 	- Реализации по умолчанию:
 		- JsonDatabase, JsonUsersTable
		- Sqlite3Users, Sqlite3Database
- ### IMessageHandler и IMessageHandler
  * Компоненты для взаимодействия с сообщениями(middleware)
