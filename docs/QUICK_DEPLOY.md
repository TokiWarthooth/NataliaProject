# 🚀 Быстрый деплой бота

## Вариант 1: Timeweb VPS (Рекомендуется) ⭐

### Где арендовать:
- **Timeweb** - https://timeweb.com/ (от 200₽/мес, российский провайдер)

### Быстрый деплой на Timeweb VPS:

```bash
# 1. Подключитесь к серверу Timeweb
ssh root@your-server-ip

# 2. Установите необходимое
apt update && apt install -y python3 python3-pip python3-venv git

# 3. Создайте директорию и клонируйте репозиторий
sudo mkdir -p /var/telegramBots
cd /var/telegramBots
sudo git clone https://github.com/your-username/your-repo.git NatalisBot
cd NatalisBot

# 4. Создайте .env файл
sudo nano .env
# Добавьте:
# BOT_TOKEN=ваш_токен
# LAWYER_CHAT_ID=ваш_chat_id

# 5. Установите и запустите
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Настройте автозапуск (скопируйте deploy/telegram-bot.service в /etc/systemd/system/)
sudo cp deploy/telegram-bot.service /etc/systemd/system/natalisbot.service
sudo systemctl daemon-reload
sudo systemctl enable natalisbot
sudo systemctl start natalisbot
```

### Настройка автоматического деплоя:

1. В GitHub: Settings → Secrets → Actions
2. Добавьте секреты:
   - `VPS_HOST` - IP сервера Timeweb
   - `VPS_USER` - пользователь (root или другой)
   - `VPS_SSH_KEY` - приватный SSH ключ
   - `VPS_DEPLOY_PATH` - путь к проекту: `/var/telegramBots/NatalisBot`

3. Теперь при каждом `git push` бот автоматически обновится!

---

## Вариант 2: Другие VPS провайдеры

### Альтернативы:
- **Hetzner** - от €4/мес - https://www.hetzner.com/
- **DigitalOcean** - от $6/мес - https://www.digitalocean.com/

Инструкция по деплою аналогична Timeweb.

---

## Вариант 3: Render (Бесплатно, для тестирования)

1. Зайдите на https://render.com/
2. New → Web Service
3. Подключите GitHub репозиторий
4. Настройки:
   - Build: `pip install -r requirements.txt`
   - Start: `python bot.py`
5. Добавьте переменные окружения
6. Deploy!

---

## Что выбрать?

- **Рекомендуется:** Timeweb VPS (от 200₽/мес, российский, надежный) ⭐
- **Альтернативы:** Hetzner (€4/мес) или DigitalOcean ($6/мес)
- **Для тестирования:** Render (бесплатно, но может "засыпать")

---

## После деплоя

Проверьте работу бота:
1. Найдите бота в Telegram
2. Отправьте `/start`
3. Проверьте все функции

**Логи:**
- Render: в веб-интерфейсе
- VPS (Timeweb и др.): `sudo journalctl -u natalisbot -f`

