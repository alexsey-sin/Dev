### Описание
Перед вами приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Найти проект можно по этому адресу/ Web address: http://178.154.220.190/recipes


### Технологии:
* Python 3.9
* Django 3.2.6
* Django rest framework 3.12.4
* Gunicorn 20.1.0
* Nginx 1.19.6
* Postgres 12.4

### Команды для работы с приложением:
-  Клонировать приложение к себе в репозиторий
```bash
git clone https://github.com/alexsey-sin/foodgram-project-react.git
```
- Необходимые переменные окружения, сохраненные в .env
    - DB_ENGINE
    - DB_NAME
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - DB_HOST
    - DB_PORT

- Запуск приложения
```bash
docker-compose up
```
- Сделать миграции
```bash
docker-compose exec foodgram python3 manage.py makemigrations

docker-compose exec foodgram python3 manage.py migrate --noinput
```
- Создание суперпользователя
```bash
docker-compose exec foodgram python3 manage.py createsuperuser
```
- Подготовка статики проекта
```bash
docker-compose exec foodgram python3 manage.py collectstatic --no-input
```
- Загрузка подготовленненных данных (ингредиенты)
```bash
docker-compose exec foodgram python3 manage.py loaddata data/igradients.json
```
### Автор
Алексей Синицин, студент факультета Бэкэнд Яндекс.Практикум (15 кагорта 2021 год)

