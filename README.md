# DRF с Docker Compose

Этот проект использует Docker и docker-compose для запуска всех сервисов (Django, база данных, Redis, Celery и т.д.).

---

## Шаги для запуска проекта

### 0. Подготовка удаленного сервера
Подключитесь к серверу через SSH:
```
ssh your_user@your_server_ip
```
Обновите систему и установите необходимые пакеты:

```
sudo apt update && sudo apt upgrade -y
sudo apt install git docker docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
```
Добавьте пользователя в группу Docker (если необходимо):

```
sudo usermod -aG docker $USER
```
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