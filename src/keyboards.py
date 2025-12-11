"""Клавиатуры для бота"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from .config import LEGAL_SERVICES


class KeyboardManager:
    """Менеджер клавиатур бота"""
    
    @staticmethod
    def get_main_menu() -> ReplyKeyboardMarkup:
        """Главное меню с кнопками"""
        keyboard = [
            [KeyboardButton("📋 Пользовательское соглашение")],
            [KeyboardButton("🛎️ Услуги")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_services_keyboard() -> InlineKeyboardMarkup:
        """Клавиатура с юридическими услугами"""
        keyboard = []
        services_list = list(LEGAL_SERVICES.items())
        
        # Размещаем по 2 кнопки в ряд
        for i in range(0, len(services_list), 2):
            row = []
            row.append(InlineKeyboardButton(services_list[i][1], callback_data=services_list[i][0]))
            if i + 1 < len(services_list):
                row.append(InlineKeyboardButton(services_list[i + 1][1], callback_data=services_list[i + 1][0]))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')])
        return InlineKeyboardMarkup(keyboard)

