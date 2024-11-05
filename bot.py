import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler
from handlers import start, convert, handle_message, handle_document, user_help, fluence, feedback_dev, buttons_callback

nest_asyncio.apply()



async def main() -> None:
    application = ApplicationBuilder().token("7620312608:AAGlXyS_Zx7F6PjBlGQHn7LMRqHRhZo6mTc").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", user_help))
    application.add_handler(CallbackQueryHandler(buttons_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))


    await application.run_polling()

# Запускаем основной код
if __name__ == '__main__':
    asyncio.run(main())