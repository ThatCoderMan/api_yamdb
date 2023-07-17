# API for YamDB

![workflow](https://github.com/ThatCoderMan/api_yamdb/actions/workflows/workflow.yml/badge.svg)
![workflow](https://github.com/ThatCoderMan/api_yamdb/actions/workflows/deploy.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.7
- Django 2.2
- Django REST Framework 
- Simplejwt
- Docker Compose 
- Gunicorn
- Nginx
- PostgresQL
- GitHub Actions

</details>


## Описание
API для проекта "YamDB" с возможностями регистрации пользователей; 
работой с постами; жанрами; категориями; публикациями; 
обзорами и комментариями к ним.

"YamDB" - сервис для бупликации постов и работы с ними.

### Инструкция по запуску:
Клонируйте репозиторий:
```commandline
git clone git@github.com:ThatCoderMan/foodgram-project-react.git
```
Установите и активируйте виртуальное окружение:

- *для MacOS:*
    ```commandline
    python3 -m venv venv
    ```
- *для Windows:*
    ```commandline
    python -m venv venv
    source venv/bin/activate
    source venv/Scripts/activate
    ```
Перейти в папку *api_yamdb/*:
```commandline
cd api_yamdb
```
Установите зависимости из файла requirements.txt:
```commandline
pip install -r requirements.txt
```
Примените миграции:
```commandline
python manage.py migrate
```
В папке с файлом manage.py выполните команду для запуска локально:
```commandline
python manage.py runserver
```
Документация к проекту доступна по адресу:
```
http://127.0.0.1/redoc/
```

### Сборка контейнера:
Перейти в папку *infra/*:
```commandline
cd infra/
```
Разверните контейнеры при помощи docker-compose:
```commandline
docker-compose up -d --build
```
Выполните миграции:
```commandline
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```commandline
docker-compose exec backend python manage.py createsuperuser
```
Заполните базу данных ингредиентами и тегами выполнив команду:
```commandline
docker-compose exec backend python manage.py from_csv_to_db --no-input
```
Остановка контейнеров:
```commandline
sudo docker-compose stop
```

### резервная копия базы данных
```commandline
docker-compose exec web python manage.py dumpdata > fixtures.json 
```

### Заполнение .env файла
В папке *infra/* необходимо создать .env файл и заполнить его данными:
```dotenv
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=YOUR_SECRET_KEY
```

### Права пользователей:

- _anonymous_ - можно просматривать описания работ, читать рецензии и комментарии.
- _authenticated user_ - может читать все, как Anonymous, может публиковать обзоры и оценивать работы (фильмы / книги / песни), может комментировать обзоры, редактировать и удалять свои обзоры и комментарии, редактировать свои собственные рейтинги работ;
- _moderator_ - те же права, что и у аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии;
- _administrator_ - может создавать и удалять произведения, категории и жанры, назначать роли пользователям;
- _superuser_ - права администратора, вы не можете изменить роль

#### Авторы проекта:

- [Артемий Березин](https://github.com/ThatCoderMan)
- [Вячеслав Шведов](https://github.com/Omen121)
- [Игорь Штенгелов](https://github.com/kontarkovi)