### Локальный запуск:

- Находясь в корневой папке проекта:
```
touch .env 
```
-заполнить .env по шаблону .env.example
```
cd backend
```
- выполнить команды:
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
```