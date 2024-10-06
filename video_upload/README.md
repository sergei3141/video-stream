# Запуск на Windows

## Создать вирутальное окружение

```
python -m venv .venv
.venv/Scripts/activate
```

## Загрузить библиотеки

```
python -m pip install -r requirements.txt
```

## Выполнить миграции

```
python manage.py makemigraions
python manage.py migrate
```

## Запустить сервер

```
python manage.py runserver
```

# Запуск на MacOS/Linux

## Создать вирутальное окружение

```
python3 -m pip install virtualenv
python3 -m virtualenv .venv
source ./.venv/bin/activate
```

## Загрузить библиотеки

```
python3 -m pip install -r requirements.txt
```

## Выполнить миграции

```
python3 manage.py makemigraions
python3 manage.py migrate
```

## Запустить сервер

```
python3 manage.py runserver
```
