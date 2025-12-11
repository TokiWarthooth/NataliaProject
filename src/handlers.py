"""Обработчики команд и сообщений бота"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from .config import (
    WAITING_DESCRIPTION, 
    WAITING_PHONE, 
    WAITING_EMAIL, 
    LEGAL_SERVICES, 
    USER_AGREEMENT,
    CONSULTATION_PRICE,
    logger
)
from .keyboards import KeyboardManager
from .application_service import ApplicationService


class BotHandlers:
    """Класс обработчиков бота"""
    
    def __init__(self, user_data: dict):
        """
        Инициализация обработчиков
        
        Args:
            user_data: Словарь для хранения данных пользователей
        """
        self.keyboard_manager = KeyboardManager()
        self.application_service = ApplicationService(user_data)
        self.user_data = user_data
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
👋 Добро пожаловать в бот юридических услуг!

Я помогу вам получить профессиональную юридическую консультацию.

Выберите действие из меню ниже:
"""
        await update.message.reply_text(
            welcome_text,
            reply_markup=self.keyboard_manager.get_main_menu()
        )
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /cancel для отмены заявки"""
        user_id = update.effective_user.id
        self.application_service.clear_user_data(user_id)
        
        await update.message.reply_text(
            "❌ Заявка отменена.",
            reply_markup=self.keyboard_manager.get_main_menu()
        )
        return ConversationHandler.END
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений (главное меню)"""
        text = update.message.text
        
        if text == "📋 Пользовательское соглашение":
            await update.message.reply_text(
                USER_AGREEMENT, 
                reply_markup=self.keyboard_manager.get_main_menu()
            )
        elif text == "🛎️ Услуги":
            await update.message.reply_text(
                "Выберите сферу юридической услуги:",
                reply_markup=self.keyboard_manager.get_services_keyboard()
            )
    
    async def handle_service_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора услуги"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'back_to_menu':
            # Очищаем данные пользователя при возврате в меню
            user_id = query.from_user.id
            self.application_service.clear_user_data(user_id)
            await query.edit_message_text(
                "Выберите действие из меню:",
                reply_markup=None
            )
            await query.message.reply_text(
                "Главное меню:",
                reply_markup=self.keyboard_manager.get_main_menu()
            )
            return ConversationHandler.END
        
        service_name = LEGAL_SERVICES.get(query.data, "Неизвестная услуга")
        
        # Сохраняем выбранную услугу
        user_id = query.from_user.id
        self.application_service.save_user_data(user_id, 'service', service_name)
        
        service_text = f"""
✅ Вы выбрали: {service_name}

💰 Стоимость консультации: {CONSULTATION_PRICE} рублей

📝 Пожалуйста, опишите вашу проблему:
"""
        await query.edit_message_text(service_text)
        
        return WAITING_DESCRIPTION
    
    async def handle_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик описания проблемы"""
        text = update.message.text
        user_id = update.effective_user.id
        
        self.application_service.save_user_data(user_id, 'description', text)
        await update.message.reply_text(
            "📞 Пожалуйста, укажите ваш номер телефона:"
        )
        return WAITING_PHONE
    
    async def handle_phone(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик номера телефона"""
        text = update.message.text
        user_id = update.effective_user.id
        
        self.application_service.save_user_data(user_id, 'phone', text)
        await update.message.reply_text(
            "📧 Пожалуйста, укажите вашу электронную почту:"
        )
        return WAITING_EMAIL
    
    async def handle_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик email и завершение заявки"""
        text = update.message.text
        user_id = update.effective_user.id
        
        self.application_service.save_user_data(user_id, 'email', text)
        
        # Отправляем заявку
        success = await self.application_service.send_to_lawyer(update, context, user_id)
        await self.application_service.send_confirmation(update, success, self.keyboard_manager)
        
        # Очищаем данные пользователя
        self.application_service.clear_user_data(user_id)
        return ConversationHandler.END

