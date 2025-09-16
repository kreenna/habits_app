# DRF с Docker Compose

Этот проект использует Docker и docker-compose для запуска всех сервисов (Django, база данных, Redis, Celery и т.д.).

---

## Шаги для запуска проекта

### 1. Клонировать репозиторий
```
git clone https://github.com/your_username/your_project.git
cd your_project
```
---

### 2. Сборка Docker-образов
```
docker-compose build
```
---

### 3. Запуск проекта
```
docker-compose up -d
```
Флаг `-d` запускает контейнеры в фоне.

---

### 4. Применение миграций
```
docker-compose exec web python manage.py migrate
```
---

### 5. Создание суперпользователя (если нужно)
```
docker-compose exec web python manage.py createsuperuser
```
---

## Проверка работоспособности сервисов

### Django

Откройте в браузере:

http://localhost:8000/

Если видите главную страницу — Django работает.

---

### База данных (PostgreSQL)

Проверьте логи:
```
docker-compose logs db
```
Вы должны видеть сообщения о запуске и отсутствии ошибок.

---

### Redis

Проверьте, что контейнер запущен:
```
docker-compose ps
```

В списке должен быть сервис `redis` со статусом `Up`.

---

### Celery Worker

Проверьте логи:
```
docker-compose logs celery
```
Должны отображаться сообщения о старте рабочего процесса.

---

### Celery Beat (если используется)

Проверьте логи:
```
docker-compose logs celery-beat
```
Должна появиться информация о планировщике задач.

---

### Остановка проекта
```
docker-compose down
```
---

## Запуск тестов
```
docker-compose exec web python manage.py test
```