# Инструкция по развертыванию бота

## Варианты хостинга

### 1. VPS (Рекомендуется) - от $5/мес

**Популярные провайдеры:**
- **DigitalOcean** - https://www.digitalocean.com/ (от $6/мес)
- **Hetzner** - https://www.hetzner.com/ (от €4/мес, очень дешево)
- **Timeweb** - https://timeweb.com/ (от 200₽/мес, российский)
- **Selectel** - https://selectel.ru/ (от 300₽/мес, российский)

**Преимущества:**
- Полный контроль
- Надежность
- Можно разместить несколько проектов

### 2. Бесплатные платформы

#### Railway (Рекомендуется для начала)
- **Сайт:** https://railway.app/
- **Бесплатно:** $5 кредитов в месяц
- **Простота:** Очень легко развернуть

#### Render
- **Сайт:** https://render.com/
- **Бесплатно:** Есть бесплатный тариф
- **Ограничения:** Может "засыпать" при неактивности

#### Fly.io
- **Сайт:** https://fly.io/
- **Бесплатно:** Есть бесплатный тариф
- **Особенности:** Хорошо для небольших проектов

### 3. Облачные функции (Serverless)

- **Yandex Cloud Functions** - https://cloud.yandex.ru/
- **AWS Lambda** - https://aws.amazon.com/lambda/
- Требуют больше настройки, но очень дешево

---

## Развертывание на VPS (Linux)

### Шаг 1: Подготовка сервера

```bash
# Подключитесь к серверу по SSH
ssh root@your-server-ip

# Обновите систему
apt update && apt upgrade -y

# Установите Python и Git
apt install -y python3 python3-pip python3-venv git

# Создайте пользователя для бота (опционально, но рекомендуется)
adduser telegrambot
usermod -aG sudo telegrambot
su - telegrambot
```

### Шаг 2: Клонирование и настройка

```bash
# Клонируйте репозиторий
cd /home/telegrambot
git clone https://github.com/your-username/your-repo.git telegram-bot
cd telegram-bot

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
nano .env
# Добавьте:
# BOT_TOKEN=ваш_токен
# LAWYER_CHAT_ID=ваш_chat_id
```

### Шаг 3: Настройка systemd для автозапуска

```bash
# Создайте service файл
sudo nano /etc/systemd/system/telegram-bot.service
```

Вставьте содержимое из файла `telegram-bot.service` (см. ниже)

```bash
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable telegram-bot

# Запустите бота
sudo systemctl start telegram-bot

# Проверьте статус
sudo systemctl status telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

### Шаг 4: Настройка автоматического деплоя через GitHub Actions

1. В репозитории GitHub перейдите в **Settings → Secrets and variables → Actions**
2. Добавьте следующие секреты:
   - `VPS_HOST` - IP адрес вашего сервера
   - `VPS_USER` - имя пользователя (например, `telegrambot` или `root`)
   - `VPS_SSH_KEY` - приватный SSH ключ для доступа к серверу
   - `VPS_DEPLOY_PATH` - путь к проекту на сервере (например, `/home/telegrambot/telegram-bot`)

3. Создайте SSH ключ на вашем компьютере (если еще нет):
```bash
ssh-keygen -t ed25519 -C "github-actions"
# Скопируйте приватный ключ (~/.ssh/id_ed25519) в GitHub Secrets как VPS_SSH_KEY
# Добавьте публичный ключ на сервер:
ssh-copy-id user@your-server-ip
```

4. При каждом push в ветку `main` бот автоматически обновится на сервере!

---

## Развертывание на Railway

### Шаг 1: Создайте аккаунт
1. Зайдите на https://railway.app/
2. Войдите через GitHub

### Шаг 2: Создайте новый проект
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий

### Шаг 3: Настройте переменные окружения
1. В проекте перейдите в "Variables"
2. Добавьте:
   - `BOT_TOKEN` = ваш токен бота
   - `LAWYER_CHAT_ID` = ваш chat ID

### Шаг 4: Настройте команду запуска
Railway автоматически определит Python проект, но убедитесь что:
- В корне есть `requirements.txt`
- Команда запуска: `python bot.py`

### Готово! Бот автоматически развернется.

---

## Развертывание на Render

### Шаг 1: Создайте аккаунт
1. Зайдите на https://render.com/
2. Войдите через GitHub

### Шаг 2: Создайте Web Service
1. Нажмите "New +" → "Web Service"
2. Подключите ваш GitHub репозиторий
3. Настройки:
   - **Name:** telegram-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

### Шаг 3: Добавьте переменные окружения
В разделе "Environment":
- `BOT_TOKEN` = ваш токен
- `LAWYER_CHAT_ID` = ваш chat ID

### Шаг 4: Деплой
Нажмите "Create Web Service" - бот развернется автоматически!

---

## Обновление бота

### Ручное обновление (VPS):
```bash
cd /home/telegrambot/telegram-bot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
```

### Автоматическое обновление:
Просто сделайте `git push` в ветку `main` - GitHub Actions автоматически обновит бота на сервере!

---

## Мониторинг и логи

### VPS (systemd):
```bash
# Просмотр логов
sudo journalctl -u telegram-bot -f

# Статус сервиса
sudo systemctl status telegram-bot

# Перезапуск
sudo systemctl restart telegram-bot
```

### Railway/Render:
Логи доступны прямо в веб-интерфейсе платформы.

---

## Рекомендации

1. **Для начала:** Используйте Railway (бесплатно, просто)
2. **Для продакшна:** Арендуйте VPS (надежнее, больше контроля)
3. **Бюджет:** Hetzner или Timeweb (самые дешевые VPS)

## Безопасность

- Никогда не коммитьте файл `.env` в Git
- Используйте SSH ключи вместо паролей
- Регулярно обновляйте зависимости
- Используйте firewall на VPS

