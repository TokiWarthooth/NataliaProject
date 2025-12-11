"""Главный файл запуска бота (точка входа)"""
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bot import main

if __name__ == '__main__':
    main()
