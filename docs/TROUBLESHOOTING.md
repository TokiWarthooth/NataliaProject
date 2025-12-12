# Решение проблем с деплоем

## Проблема: `sudo systemctl daemon-reload` не выполняется

### Шаг 1: Проверьте, что файл service скопирован правильно

```bash
# Проверьте, что файл существует
ls -la /etc/systemd/system/natalisbot.service

# Если файла нет, скопируйте его:
sudo cp /var/telegramBots/NatalisBot/deploy/natalisbot.service /etc/systemd/system/natalisbot.service

# Проверьте содержимое файла
sudo cat /etc/systemd/system/natalisbot.service
```

### Шаг 2: Проверьте права доступа

```bash
# Убедитесь, что у вас есть права sudo
sudo whoami
# Должно вывести: root

# Если нет прав, добавьте пользователя в sudoers:
# (выполните от root или другого пользователя с sudo)
sudo usermod -aG sudo your_username
```

### Шаг 3: Проверьте синтаксис файла service

```bash
# Проверьте синтаксис файла
sudo systemd-analyze verify /etc/systemd/system/natalisbot.service

# Если есть ошибки, они будут показаны
```

### Шаг 4: Выполните команды по отдельности

**Важно:** Выполняйте команды по одной, не слитно!

```bash
# 1. Перезагрузите systemd
sudo systemctl daemon-reload

# 2. Включите автозапуск
sudo systemctl enable natalisbot

# 3. Запустите сервис
sudo systemctl start natalisbot

# 4. Проверьте статус
sudo systemctl status natalisbot
```

### Шаг 5: Если команда все равно не работает

Проверьте, что systemd доступен:

```bash
# Проверьте версию systemd
systemctl --version

# Проверьте, что systemd запущен
systemctl status

# Попробуйте без sudo (если вы root)
systemctl daemon-reload
```

### Шаг 6: Альтернативный способ - создание файла вручную

Если копирование не работает, создайте файл вручную:

```bash
# Создайте файл
sudo nano /etc/systemd/system/natalisbot.service
```

Вставьте следующее содержимое:

```ini
[Unit]
Description=NatalisBot - Telegram Bot для юридических услуг
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/telegramBots/NatalisBot
Environment="PATH=/var/telegramBots/NatalisBot/venv/bin"
ExecStart=/var/telegramBots/NatalisBot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохраните (Ctrl+O, Enter, Ctrl+X) и выполните:

```bash
sudo systemctl daemon-reload
sudo systemctl enable natalisbot
sudo systemctl start natalisbot
```

## Другие частые проблемы

### Проблема: "Service not found"

```bash
# Убедитесь, что файл называется правильно
ls /etc/systemd/system/natalisbot.service

# Если файл называется по-другому, переименуйте:
# Если файл называется по-другому, переименуйте:
sudo mv /etc/systemd/system/old-name.service /etc/systemd/system/natalisbot.service
sudo systemctl daemon-reload
```

### Проблема: "Permission denied"

```bash
# Проверьте права на директорию бота
ls -la /var/telegramBots/NatalisBot

# Если нужно, измените владельца:
sudo chown -R root:root /var/telegramBots/NatalisBot
```

### Проблема: Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u natalisbot -n 50

# Проверьте, что .env файл существует и заполнен
cat /var/telegramBots/NatalisBot/.env

# Попробуйте запустить вручную
cd /var/telegramBots/NatalisBot
source venv/bin/activate
python bot.py
```

## Проверка работоспособности

После успешного запуска проверьте:

```bash
# Статус сервиса
sudo systemctl status natalisbot

# Логи в реальном времени
sudo journalctl -u natalisbot -f

# Проверка, что процесс запущен
ps aux | grep python
```

