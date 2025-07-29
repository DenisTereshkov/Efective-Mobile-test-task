# Обменник товаров (Django)

**Минималистичная площадка для обмена вещами**  
[![Python 3.12+](https://img.shields.io/badge/python-3.8+-blue)](https://www.python.org/)
[![Django 5.2](https://img.shields.io/badge/django-5.2-green)](https://www.djangoproject.com/)



2. **Настройка окружения**:
Создайте в корне проекта файл .env
## ⚠️ Важно
Файл `.env` должен содержать:
```
SECRET_KEY=ваш_ключ_из_20_символов
DEBUG=True  # False для продакшена
```

1. **Переход в папку проекта**:
   ```bash
   cd backend
   ```
3. **Установка и миграции**:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Запуск**:
   ```bash
   python manage.py runserver
   ```
   → Откройте [http://localhost:8000](http://localhost:8000)

## 🛠 Технический минимум
- **База данных**: SQLite (готова сразу)
- **Шаблоны**: Django Templates
- **Аутентификация**: Стандартная Django-авторизация

## 📋 Основные команды
```bash
# Создать админа
python manage.py createsuperuser

# Запустить тесты
python manage.py test


