# Инструкция по развертыванию бота

## Варианты хостинга

### 1. VPS (Рекомендуется) - от $5/мес

**Популярные провайдеры:**
- **Timeweb** - https://timeweb.com/ (от 200₽/мес, российский, рекомендуется) ⭐
- **Hetzner** - https://www.hetzner.com/ (от €4/мес, очень дешево)
- **DigitalOcean** - https://www.digitalocean.com/ (от $6/мес)
- **Selectel** - https://selectel.ru/ (от 300₽/мес, российский)

**Преимущества:**
- Полный контроль
- Надежность
- Можно разместить несколько проектов

### 2. Облачные функции (Serverless)

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
# Создайте директорию для ботов (если еще не создана)
sudo mkdir -p /var/telegramBots
cd /var/telegramBots

# Клонируйте репозиторий
sudo git clone https://github.com/your-username/your-repo.git NatalisBot
cd NatalisBot

# Создайте виртуальное окружение
sudo python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
sudo nano .env
# Добавьте:
# BOT_TOKEN=ваш_токен
# LAWYER_CHAT_ID=ваш_chat_id
```

### Шаг 3: Настройка systemd для автозапуска

```bash
# Скопируйте service файл
sudo cp deploy/telegram-bot.service /etc/systemd/system/natalisbot.service

# Или создайте вручную
sudo nano /etc/systemd/system/natalisbot.service
```

Вставьте содержимое из файла `deploy/telegram-bot.service` (пути уже настроены на `/var/telegramBots/NatalisBot`)

```bash
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable natalisbot

# Запустите бота
sudo systemctl start natalisbot

# Проверьте статус
sudo systemctl status natalisbot

# Просмотр логов
sudo journalctl -u natalisbot -f
```

### Шаг 4: Настройка автоматического деплоя через GitHub Actions

1. В репозитории GitHub перейдите в **Settings → Secrets and variables → Actions**
2. Добавьте следующие секреты:
   - `VPS_HOST` - IP адрес вашего сервера
   - `VPS_USER` - имя пользователя (например, `telegrambot` или `root`)
   - `VPS_SSH_KEY` - приватный SSH ключ для доступа к серверу
   - `VPS_DEPLOY_PATH` - путь к проекту на сервере: `/var/telegramBots/NatalisBot`

3. Создайте SSH ключ на вашем компьютере (если еще нет):
```bash
ssh-keygen -t ed25519 -C "github-actions"
# Скопируйте приватный ключ (~/.ssh/id_ed25519) в GitHub Secrets как VPS_SSH_KEY
# Добавьте публичный ключ на сервер:
ssh-copy-id user@your-server-ip
```

4. При каждом push в ветку `main` бот автоматически обновится на сервере!

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
cd /var/telegramBots/NatalisBot
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart natalisbot
```

### Автоматическое обновление:
Просто сделайте `git push` в ветку `main` - GitHub Actions автоматически обновит бота на сервере!

---

## Мониторинг и логи

### VPS (systemd):
```bash
# Просмотр логов
sudo journalctl -u natalisbot -f

# Статус сервиса
sudo systemctl status natalisbot

# Перезапуск
sudo systemctl restart natalisbot
```

### Render:
Логи доступны прямо в веб-интерфейсе платформы.

---

## Рекомендации

1. **Рекомендуется:** Timeweb VPS (от 200₽/мес, российский провайдер, надежный)
2. **Альтернативы:** Hetzner (€4/мес) или DigitalOcean ($6/мес)
3. **Для продакшна:** VPS дает полный контроль и надежность

## Безопасность

- Никогда не коммитьте файл `.env` в Git
- Используйте SSH ключи вместо паролей
- Регулярно обновляйте зависимости
- Используйте firewall на VPS

