![CI](https://github.com/AndreyEagle/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Foodgram - это сервис, позволяющий пользователям делиться своими рецептами.  Сервис позволяет: 
- добавлять понравившиеся рецепты в избранное; 
- подписываться на интересных авторов рецептов;
- скачивать список продуктов, необходимых для приготовления выбранного блюда.

***
### Проект доступен по ссылке:

http://foodgram.sytes.net/

### Стек технологий:
```
Python 3
Django
Django REST Framework
Djoser
Docker
```

## Запуск проекта:
1. Клонировать репозиторий:
```
git clone https://github.com/AndreyEagle/foodgram-project-react.git
```
2. Перед запуском проекта создать файл переменных окружения .env в папке /infra:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<ваш username>
POSTGRES_PASSWORD=<ваш password>
DB_HOST=db
DB_PORT=5432

DJANGO_DEBUG=''
SECRET_KEY=<ваш secret key>
```
3. Сборка и запуск проекта осуществляется из папки /infra:
```
docker-compose up -d --build
```
4. Выполнить миграции:
```
docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec backend python manage.py migrate
```
5. Создать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
6. Создать администратора:
```
docker-compose exec backend python manage.py createsuperuser
```
