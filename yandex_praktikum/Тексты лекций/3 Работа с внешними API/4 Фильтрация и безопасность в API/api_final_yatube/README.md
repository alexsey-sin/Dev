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
> manage.py migrate
6. Создаем администратора:
> manage.py createsuperuser
7. Вводим логин, email, пароль администратора.
8. Запускаем сервер:
> manage.py runserver
9. Всё. Сервер запущен, api проекта доступено по адресу http://127.0.0.1:8000/

## API
    Документация по api из браузера: http://127.0.0.1:8000/redoc/
## Примеры
### Получаем токен
Отправляем **POST** -запрос на адрес *api/v1/token/* и передаем 2 поля в *data*.

1. username - указываем имя пользователя.
2. password - указываем пароль пользователя.

Примечание.

    Токен refresh нужен, чтобы обновить текущий токен.
    Токен access нужно сохранить и бережно хранить. Используется для аунтефикации пользователя.
    Жизнь токена 1 год, в настройках можно изменить.

### POST
#### Получить список всех публикаций
##### GET
###### query Parameters
    group (number) ID группы
> http://127.0.0.1:8000/api/v1/posts/
###### Responses
    200  
    Content type *application/json*  

#### Создать новую публикацию
##### POST
###### query Parameters  
    text *required* (string) текст поста
> http://127.0.0.1:8000/api/v1/posts/
###### Responses
    200  
    Content type *application/json*  

#### Получить публикацию по id  
##### GET
###### query Parameters  
    id *required* (number) ID публикации
> http://127.0.0.1:8000/api/v1/posts/{id}/
###### Responses  
    200  
    Content type *application/json*  

    400  
    Content type *application/json*  

#### Обновить публикацию по id  
##### PUT 
###### query Parameters  
    id *required* (number) ID публикации  
    text *required* (string) текст поста
> http://127.0.0.1:8000/api/v1/posts/{id}/
###### Responses
    200  
    Content type *application/json*  

    400  
    Content type *application/json*  

#### Частично обновить публикацию по id  
##### PATCH 
###### query Parameters
    id *required* (number) ID публикации  
    text *required* (string) текст поста
> http://127.0.0.1:8000/api/v1/posts/{id}/
###### Responses
    200  
    Content type *application/json*  

    400  
    Content type *application/json*  

#### Удалить публикацию по id
##### DELETE
###### query Parameters  
    id *required* (number) ID публикации  
> http://127.0.0.1:8000/api/v1/posts/{id}/
###### Responses
    204  

### COMMENTS
#### Получить список всех комментариев публикации  
##### GET
###### query Parameters  
    post_id *required* (number) ID публикации
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
###### Responses
    200  
    Content type *application/json*  

#### Создать новый комментарий для публикации
##### POST
###### query Parameters
    post_id *required* (number) ID публикации
	text *required* (string) текст поста
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
###### Responses
    200  
    Content type *application/json*  

#### Получить комментарий для публикации по id
##### GET
###### query Parameters
    post_id *required* (number) ID публикации
	comment *required*_id (number)ID комментария
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
###### Responses
    200  
    Content type *application/json*  

#### Обновить комментарий для публикации по id
##### PUT
###### query Parameters
    post_id *required* (number) ID публикации
	comment_id *required* (number)ID комментария
	text *required* (string) текст поста
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
###### Responses
    200  
    Content type *application/json*  

#### Частично обновить комментарий для публикации по id
##### PATCH
###### query Parameters
    post_id *required* (number) ID публикации
	comment_id *required* (number)ID комментария
	text *required* (string) текст поста
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
###### Responses
    200  
    Content type *application/json*  

#### Удалить комментарий для публикации по id
##### DELETE
###### query Parameters
    post_id *required* (number) ID публикации
	comment_id *required* (number)ID комментария
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{comment_id}/
###### Responses
    200  


### AUTH
#### Получить JWT-токен 
##### POST
###### query Parameters  
    username *required* (string)
    password *required* (string)
http://127.0.0.1:8000/api/v1/token/
###### Responses
    200  
    Content type *application/json*  

    400  
    Content type *application/json*  

### FOLLOW
#### Получить список всех подписчиков
##### GET
###### query Parameters  
    search (string) username тот кто подписан или на кого подписаны
http://127.0.0.1:8000/api/v1/follow/
###### Responses
    200  
    Content type *application/json*  

#### Создать подписку 
##### POST
###### query Parameters  
    user (string) Пользователь для фильтрации по подписчикам  
    following *required* (string)
http://127.0.0.1:8000/api/v1/follow/
###### Responses
    200  
    Content type *application/json*  

### GROUP
#### Получить список всех групп
##### GET
http://127.0.0.1:8000/api/v1/group/
###### Responses
    200  
    Content type *application/json*  

#### Создать новую группу
##### POST
###### query Parameters  
    title (string) Название группы  
http://127.0.0.1:8000/api/v1/group/
###### Responses
    200  
    Content type *application/json*  














