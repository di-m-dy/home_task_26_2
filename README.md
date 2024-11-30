# Домашнее задание 27_2

## !!!ВНИМАНИЕ!!! ##
### Инструкция перед запуском проекта (порядок выполнения имеет значение)
1. Перед запуском проекта переименуйте файл [env_template](env_template) в `.env` и поменяйте содержимое на свои переменные окруженния
2. Выполните миграцию `python manage.py migrate`
3. Создайте суперпользователя (имеет все права) `python manage.py create_custom_superuser`

    _Логин: admin@example.com Пароль: 0987_

4. Создайте модератора: `python manage.py create_moderator_user`

    _Логин: moderator@example.com Пароль: qweasd_

5. Создайте простого пользователя: `python manage.py create_simple_user`

    _Логин: test@example.com Пароль: 0987_

6. Заполните базу даных (курсы и уроки): `python manage.py fill_materials_data `
7. Заполните базу даных (платежи): `python manage.py fill_payment_data`

# Задание 1
1. Опишите Dockerfile для запуска контейнера с проектом.
2. Оберните в Docker Compose Django-проект с БД PostgreSQL.
3. Допишите в docker-compose.yaml работу с Redis.
4. Допишите в docker-compose.yaml работу с Celery.