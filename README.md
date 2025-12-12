# NatalisBot - Telegram Bot для юридических услуг

Бот для приема заявок на юридические консультации.

## Функционал

- ✅ Приветствие при запуске
- ✅ Пользовательское соглашение
- ✅ Выбор сферы юридической услуги (семейное право, имущественное, развод, IT право и др.)
- ✅ Форма заявки (описание проблемы, телефон, email)
- ✅ Автоматическая отправка заявки юристу в Telegram
- ✅ Подтверждение пользователю об успешной отправке

## Локальная развертка

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка .env файла

Создайте файл `.env` в корне проекта:

```
BOT_TOKEN=ваш_токен_бота
LAWYER_CHAT_ID=ваш_chat_id_юриста
```

**Как получить LAWYER_CHAT_ID:**
- Напишите боту @userinfobot в Telegram
- Он покажет ваш Chat ID (число)
- Вставьте это число в `.env`

### 3. Запуск

```bash
python bot.py
```

### 4. Отладка

В Cursor/VS Code:
1. Откройте `bot.py`
2. Установите breakpoint (клик слева от номера строки)
3. Нажмите **F5**

## Развертка на сервере (Timeweb VPS)

### 1. Подготовка сервера

```bash
# Подключитесь к серверу
ssh root@your-server-ip

# Установите необходимое
apt update && apt install -y python3 python3-pip python3-venv git
```

### 2. Клонирование и настройка

```bash
# Создайте директорию
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

# Создайте .env файл
sudo nano .env
# Добавьте BOT_TOKEN и LAWYER_CHAT_ID
```

### 3. Настройка автозапуска

```bash
# Скопируйте service файл
sudo cp deploy/natalisbot.service /etc/systemd/system/natalisbot.service

# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable natalisbot

# Запустите бота
sudo systemctl start natalisbot

# Проверьте статус
sudo systemctl status natalisbot
```

### 4. Просмотр логов

```bash
sudo journalctl -u natalisbot -f
```

## Автоматический деплой

### Настройка GitHub Actions

1. В GitHub: **Settings → Secrets → Actions**
2. Добавьте секреты:
   - `VPS_HOST` - IP адрес сервера
   - `VPS_USER` - пользователь (root)
   - `VPS_SSH_KEY` - приватный SSH ключ
   - `VPS_DEPLOY_PATH` - `/var/telegramBots/NatalisBot`

3. При каждом `git push` в ветку `main` бот автоматически обновится!

## Структура проекта

```
NataliaProject/
├── src/                      # Исходный код бота
│   ├── bot.py               # Главный файл бота
│   ├── config.py            # Конфигурация
│   ├── handlers.py          # Обработчики команд
│   ├── keyboards.py         # Клавиатуры
│   └── application_service.py  # Сервис заявок
├── deploy/                  # Файлы для развертывания
│   ├── deploy.sh
│   └── natalisbot.service
├── configs/                 # Конфигурационные файлы
├── bot.py                   # Точка входа
└── requirements.txt         # Зависимости
```

## Управление сервисом

```bash
# Статус
sudo systemctl status natalisbot

# Перезапуск
sudo systemctl restart natalisbot

# Остановка
sudo systemctl stop natalisbot

# Логи
sudo journalctl -u natalisbot -f
```
