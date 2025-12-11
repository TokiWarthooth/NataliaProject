"""Сервис для работы с заявками"""
from telegram import Update
from telegram.ext import ContextTypes
from config import LAWYER_CHAT_ID, logger


class ApplicationService:
    """Сервис для обработки и отправки заявок"""
    
    def __init__(self, user_data: dict):
        """
        Инициализация сервиса
        
        Args:
            user_data: Словарь для хранения данных пользователей
        """
        self.user_data = user_data
        self.lawyer_chat_id = LAWYER_CHAT_ID
    
    def format_application_text(self, update: Update, user_id: int) -> str:
        """
        Форматирование текста заявки для юриста
        
        Args:
            update: Объект обновления Telegram
            user_id: ID пользователя
            
        Returns:
            Отформатированный текст заявки
        """
        data = self.user_data.get(user_id, {})
        username = update.effective_user.username if update.effective_user.username else 'username не указан'
        
        return f"""
📋 НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ

👤 Клиент: {update.effective_user.full_name}
🆔 ID: {user_id}
📞 Телефон: {data.get('phone', 'Не указан')}
📧 Email: {data.get('email', 'Не указан')}
🛎️ Услуга: {data.get('service', 'Не указана')}

📝 Описание проблемы:
{data.get('description', 'Не указано')}

---
Для связи с клиентом: @{username}
"""
    
    async def send_to_lawyer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
        """
        Отправка заявки юристу
        
        Args:
            update: Объект обновления Telegram
            context: Контекст бота
            user_id: ID пользователя
            
        Returns:
            True если заявка отправлена успешно, False в противном случае
        """
        if not self.lawyer_chat_id:
            logger.warning("LAWYER_CHAT_ID не установлен, заявка не отправлена")
            return False
        
        try:
            application_text = self.format_application_text(update, user_id)
            await context.bot.send_message(
                chat_id=self.lawyer_chat_id,
                text=application_text
            )
            logger.info(f"Заявка отправлена юристу от пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при отправке заявки: {e}")
            return False
    
    async def send_confirmation(self, update: Update, success: bool, keyboard_manager):
        """
        Отправка подтверждения пользователю
        
        Args:
            update: Объект обновления Telegram
            success: Успешно ли отправлена заявка
            keyboard_manager: Менеджер клавиатур
        """
        if success:
            await update.message.reply_text(
                "✅ Ваша заявка успешно отправлена!\n\n"
                "Наш юрист свяжется с вами в ближайшее время.\n\n"
                "Спасибо за обращение!",
                reply_markup=keyboard_manager.get_main_menu()
            )
        else:
            await update.message.reply_text(
                "❌ Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже.",
                reply_markup=keyboard_manager.get_main_menu()
            )
    
    def save_user_data(self, user_id: int, key: str, value: str):
        """
        Сохранение данных пользователя
        
        Args:
            user_id: ID пользователя
            key: Ключ данных
            value: Значение
        """
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id][key] = value
    
    def get_user_data(self, user_id: int) -> dict:
        """
        Получение данных пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Словарь с данными пользователя
        """
        return self.user_data.get(user_id, {})
    
    def clear_user_data(self, user_id: int):
        """
        Очистка данных пользователя
        
        Args:
            user_id: ID пользователя
        """
        if user_id in self.user_data:
            del self.user_data[user_id]

