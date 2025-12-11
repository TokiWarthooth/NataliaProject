#!/bin/bash

# Скрипт для ручного деплоя на VPS

set -e

echo "🚀 Начинаем деплой бота..."

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Файл .env не найден!${NC}"
    echo "Создайте файл .env с переменными BOT_TOKEN и LAWYER_CHAT_ID"
    exit 1
fi

# Обновление кода
echo -e "${GREEN}📥 Обновление кода из Git...${NC}"
git pull origin main || git pull origin master

# Активация виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${GREEN}📦 Создание виртуального окружения...${NC}"
    python3 -m venv venv
fi

echo -e "${GREEN}🔧 Активация виртуального окружения...${NC}"
source venv/bin/activate

# Установка зависимостей
echo -e "${GREEN}📚 Установка зависимостей...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Перезапуск сервиса (если используется systemd)
if systemctl is-active --quiet natalisbot; then
    echo -e "${GREEN}🔄 Перезапуск сервиса NatalisBot...${NC}"
    sudo systemctl restart natalisbot
    echo -e "${GREEN}✅ Бот перезапущен!${NC}"
    echo -e "${GREEN}📋 Статус:${NC}"
    sudo systemctl status natalisbot --no-pager -l
else
    echo -e "${YELLOW}⚠️  Сервис natalisbot не найден. Запускаем бота вручную...${NC}"
    echo -e "${GREEN}✅ Деплой завершен! Запустите бота командой: python bot.py${NC}"
    echo -e "${GREEN}   Или: python -m src.bot${NC}"
fi

echo -e "${GREEN}🎉 Деплой завершен успешно!${NC}"

