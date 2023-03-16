# yamdb_final
![yamdb_workflow](https://github.com/Ehite5/yamdb_final/workflows/yamdb_workflow.yml/badge.svg)
## Описание проекта
- Проект YaMDb собирает отзывы пользователей на произведения.
- Произведения делятся на категории: Музыка, Фильмы, Книги.
- Список категорий может быть расширен администратором.
<<<<<<< HEAD
- Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
- Пользователи могут ставить произведениям оценки что в дальнейшем повлияет на усреднённый рейтинг произведения.
=======
- Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может 
создавать только администратор.
- Пользователи могут ставить произведениям оценки что в дальнейшем повлияет на усреднённый 
рейтинг произведения.
>>>>>>> 3e66497 (Docker_yamdb)

## Для реализации проекта используются:
- Django 2.2.16
- Django REST Framework 3.12.4



## Документация к API
http://127.0.0.1:8000/redoc/



### Как запустить проект:

Все описанное ниже относится к ОС Linux.
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/Ehite5/yamdb_final
cd yamdb_final
cd api_yamdb
```

Ставим зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

Переходим в папку с файлом docker-compose.yaml:
```bash
cd infra
```

Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker-compose up -d --build
```

Выполняем миграции:
```bash
docker-compose exec web python manage.py makemigrations reviews
```
```bash
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

Останавливаем контейнеры:
```bash
docker-compose down -v
```

Документация к API:
```bash
http://127.0.0.1:8000/redoc/
```
