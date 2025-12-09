import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы для состояний разговора
WAITING_DESCRIPTION, WAITING_PHONE, WAITING_EMAIL = range(3)

# Получаем токен и ID юриста из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
LAWYER_CHAT_ID = os.getenv('LAWYER_CHAT_ID')

# Хранение данных пользователя (в продакшене лучше использовать БД)
user_data = {}

# Текст пользовательского соглашения
USER_AGREEMENT = """
📋 ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ

1. Общие положения
Настоящее соглашение определяет условия использования бота для получения юридических консультаций.

2. Условия предоставления услуг
- Консультация предоставляется на платной основе
- Стоимость консультации: 1000 рублей
- Юрист свяжется с вами в течение 24 часов

3. Обработка персональных данных
Ваши персональные данные используются исключительно для связи с вами и предоставления консультации.

4. Контакты
По всем вопросам обращайтесь к администратору бота.
"""

# Список юридических услуг
LEGAL_SERVICES = {
    'family': '👨‍👩‍👧‍👦 Семейное право',
    'property': '🏠 Имущественное право',
    'divorce': '💔 Развод',
    'it_law': '💻 IT право',
    'labor': '💼 Трудовое право',
    'criminal': '⚖️ Уголовное право',
    'civil': '📜 Гражданское право',
    'business': '🏢 Бизнес право'
}


def get_main_menu():
    """Главное меню с кнопками"""
    keyboard = [
        [KeyboardButton("📋 Пользовательское соглашение")],
        [KeyboardButton("🛎️ Услуги")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_services_keyboard():
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
👋 Добро пожаловать в бот юридических услуг!

Я помогу вам получить профессиональную юридическую консультацию.

Выберите действие из меню ниже:
"""
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu()
    )


async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик описания проблемы"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['description'] = text
    await update.message.reply_text(
        "📞 Пожалуйста, укажите ваш номер телефона:"
    )
    return WAITING_PHONE


async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик номера телефона"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['phone'] = text
    await update.message.reply_text(
        "📧 Пожалуйста, укажите вашу электронную почту:"
    )
    return WAITING_EMAIL


async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик email и завершение заявки"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['email'] = text
    # Формируем и отправляем заявку
    await send_application(update, context)
    # Очищаем данные пользователя
    if user_id in user_data:
        del user_data[user_id]
    return ConversationHandler.END


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений (главное меню)"""
    text = update.message.text
    
    if text == "📋 Пользовательское соглашение":
        await update.message.reply_text(USER_AGREEMENT, reply_markup=get_main_menu())
    elif text == "🛎️ Услуги":
        await update.message.reply_text(
            "Выберите сферу юридической услуги:",
            reply_markup=get_services_keyboard()
        )


async def handle_service_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора услуги"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_to_menu':
        # Очищаем данные пользователя при возврате в меню
        user_id = query.from_user.id
        if user_id in user_data:
            del user_data[user_id]
        await query.edit_message_text(
            "Выберите действие из меню:",
            reply_markup=None
        )
        await query.message.reply_text(
            "Главное меню:",
            reply_markup=get_main_menu()
        )
        return ConversationHandler.END
    
    service_name = LEGAL_SERVICES.get(query.data, "Неизвестная услуга")
    
    # Сохраняем выбранную услугу
    user_id = query.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['service'] = service_name
    
    service_text = f"""
✅ Вы выбрали: {service_name}

💰 Стоимость консультации: 1000 рублей

📝 Пожалуйста, опишите вашу проблему:
"""
    await query.edit_message_text(service_text)
    
    return WAITING_DESCRIPTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /cancel для отмены заявки"""
    user_id = update.effective_user.id
    if user_id in user_data:
        del user_data[user_id]
    
    await update.message.reply_text(
        "❌ Заявка отменена.",
        reply_markup=get_main_menu()
    )
    return ConversationHandler.END


async def send_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка заявки юристу"""
    user_id = update.effective_user.id
    data = user_data.get(user_id, {})
    
    # Формируем сообщение для юриста
    application_text = f"""
📋 НОВАЯ ЗАЯВКА НА КОНСУЛЬТАЦИЮ

👤 Клиент: {update.effective_user.full_name}
🆔 ID: {user_id}
📞 Телефон: {data.get('phone', 'Не указан')}
📧 Email: {data.get('email', 'Не указан')}
🛎️ Услуга: {data.get('service', 'Не указана')}

📝 Описание проблемы:
{data.get('description', 'Не указано')}

---
Для связи с клиентом: @{update.effective_user.username if update.effective_user.username else 'username не указан'}
"""
    
    try:
        # Отправляем заявку юристу
        if LAWYER_CHAT_ID:
            await context.bot.send_message(
                chat_id=LAWYER_CHAT_ID,
                text=application_text
            )
            logger.info(f"Заявка отправлена юристу от пользователя {user_id}")
        else:
            logger.warning("LAWYER_CHAT_ID не установлен, заявка не отправлена")
        
        # Подтверждение пользователю
        await update.message.reply_text(
            "✅ Ваша заявка успешно отправлена!\n\n"
            "Наш юрист свяжется с вами в ближайшее время.\n\n"
            "Спасибо за обращение!",
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке заявки: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при отправке заявки. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_menu()
        )


def main():
    """Главная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен! Проверьте файл .env")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Создаем обработчик разговора для формы заявки
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handle_service_selection, pattern='^(family|property|divorce|it_law|labor|criminal|civil|business)$')
        ],
        states={
            WAITING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)],
            WAITING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
            WAITING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CallbackQueryHandler(handle_service_selection, pattern='^back_to_menu$')
        ],
    )
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_service_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

