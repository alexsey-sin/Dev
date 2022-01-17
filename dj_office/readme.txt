# Для проекта создаем папку, например, dj_project
# Из командной строки переходим в папку
$ cd dj_project

# Создаем виртуальное окружение (Python разумеется уже установлен в системе)
$ python -m venv venv

# Активируем виртуальное окружение
$ venv\Scripts\activate

# Обновим pip
(venv)$ python -m pip install --upgrade pip

# Установим Django
(venv)$ pip install Django

# Создадим проект
(venv)$ django-admin startproject dj_project

# Создадим первое приложение
(venv)$ python manage.py startapp bond

# Создадим базу данных
(venv)$ python manage.py migrate

# Создадим суперпользователя
(venv)$ python manage.py createsuperuser














