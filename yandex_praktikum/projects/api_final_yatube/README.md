# api_final_yatube
## Описание
api_final_yatube - это проект в рамках курса обучения Python backend developer.
Это бэкенд социальной сети для публикации личных дневников на котором можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора.
Пользователи могут просматривать чужие страницы, подписываться на авторов и комментировать их записи. 
Аутентификация пользователей происходит по JWT-токену.

## Установка
### Как развернуть проект на локальной машине.
1. Необходимо клонировать репозитарий на свой локальный компьютер:
> git clone https://github.com/alexsey-sin/api_final_yatube.git
2. С терминала зайдите во вновь созданную папку **api_final_yatube**
3. Создайте виртуальное окружение:
> python -m venv venv
4. Установите зависимости проекта:
> pip install -r requirements.txt
5. Создание базы данных и миграция:
> 
