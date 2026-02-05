import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = "8266204920:AAGmiHhMiwV88oYBGJgubnalGm4g1PFLOS8"
CORRECT_PASSWORD = "F6h0Ksu1Nm₽"

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Бот запущен!\n\n"
        "Введите пароль для доступа:"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == CORRECT_PASSWORD:
        await update.message.reply_text(
            "✅ Пароль верный! Доступ открыт.\n\n"
            "Команды:\n"
            "/start - начало\n"
            "/ping - проверка\n"
            "/status - статус"
        )
    else:
        await update.message.reply_text("❌ Неверный пароль")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Бот работает на Render 24/7!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Статус: ONLINE\n📍 Хостинг: Render.com")

# Основная функция
def main():
    logger.info("Запуск бота...")
    
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Настройки для Render
    PORT = int(os.environ.get('PORT', 10000))
    WEBHOOK_URL = "https://telegram-bot-24-7.onrender.com"  # БУДЕТ ВАШ URL
    
    logger.info(f"Порт: {PORT}")
    logger.info(f"Webhook URL: {WEBHOOK_URL}/{BOT_TOKEN}")
    
    # Запускаем через webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
