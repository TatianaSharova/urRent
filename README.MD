# **_UrRent_**
Сервис для бронирования помещений.  

Стек: Python, FastAPI, SQLalchemy, aiosqlite, Pydantic  

**Как запустить проект:**
-----------
Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/TatianaSharova/urRent.git
```

Создать и активировать виртуальное окружение:
```bash
poetry install
poetry env activate
source .venv/Scripts/activate
```

**Аутентификация:**  
-----------
Для аутентификации в проекте используются JWT-токены. Для обеспечения безопасности и работы с JWT-токенами в проекте используются RSA-ключи. Приватный ключ будет использоваться для подписи JWT-токенов, а публичный — для их верификации. Для их генерации выполните следующие шаги:

1. В директории src/auth/ создайте папку certs/:
```bash
mkdir src/auth/certs
```
2. Сгенерируйте RSA-ключи с помощью openssl.
```bash
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048

# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

**Работа с бд:** 
-----------
alembic
urRent/src
```bash
alembic revision --autogenerate -m "create ... table"
```
применить миграцию
```bash
alembic upgrade head
```

**Документация:**  
-----------
Документацию к API после запуска проекта можно посмотреть по адресам:
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Pre-commit
Этот проект использует [pre-commit](https://pre-commit.com/) для автоматического запуска линтеров перед коммитом.

### Настройка pre-commit
Установи хуки:

```bash
poetry run pre-commit install
```

### Ручной запуск

Проверить все файлы вручную:
```bash
pre-commit run --all-files
```
Проверить конкретный файл:
```bash
pre-commit run --files path/to/file.py
```

### Автор
[Татьяна Шарова](https://github.com/TatianaSharova)
