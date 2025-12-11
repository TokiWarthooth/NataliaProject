"""Главный файл запуска бота"""
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters
from telegram import Update
from config import BOT_TOKEN, WAITING_DESCRIPTION, WAITING_PHONE, WAITING_EMAIL, logger
from handlers import BotHandlers

# Хранение данных пользователя (в продакшене лучше использовать БД)
user_data = {}


def main():
    """Главная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен! Проверьте файл .env")
        return
    
    # Инициализируем обработчики
    handlers = BotHandlers(user_data)
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Создаем обработчик разговора для формы заявки
    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                handlers.handle_service_selection, 
                pattern='^(family|property|divorce|it_law|labor|criminal|civil|business)$'
            )
        ],
        states={
            WAITING_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_description)
            ],
            WAITING_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_phone)
            ],
            WAITING_EMAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_email)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", handlers.cancel),
            CallbackQueryHandler(handlers.handle_service_selection, pattern='^back_to_menu$')
        ],
    )
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("cancel", handlers.cancel))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handlers.handle_service_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
