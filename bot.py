import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
BOT_TOKEN = "8266204920:AAGmiHhMiwV88oYBGJgubnalGm4g1PFLOS8"
CORRECT_PASSWORD = "F6h0Ksu1Nm₽"  # Пароль для доступа

# Словарь для хранения авторизованных пользователей
authorized_users = {}

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    if user_id in authorized_users:
        await update.message.reply_text(
            f"✅ Вы уже авторизованы, {username}!\n"
            "Доступ ко всем функциям открыт.\n\n"
            "Доступные команды:\n"
            "/help - справка\n"
            "/info - информация"
        )
    else:
        await update.message.reply_text(
            "🔐 Для доступа к боту требуется авторизация.\n\n"
            "Введите пароль ниже:"
        )

# Обработка ввода пароля
async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    # Если пользователь уже авторизован
    if user_id in authorized_users:
        return
    
    # Проверка пароля
    if text == CORRECT_PASSWORD:
        authorized_users[user_id] = {
            'username': update.effective_user.username,
            'first_name': update.effective_user.first_name,
            'access_time': update.message.date
        }
        
        await update.message.reply_text(
            "✅ Пароль верный! Полный доступ открыт.\n\n"
            "Теперь вы можете использовать все функции бота.\n"
            "Введите /help для просмотра доступных команд."
        )
        logging.info(f"Пользователь {user_id} успешно авторизовался")
    else:
        await update.message.reply_text("❌ Неверный пароль. Попробуйте еще раз.")
        logging.warning(f"Неудачная попытка входа от пользователя {user_id}")

# Пример команды для авторизованных пользователей
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in authorized_users:
        await update.message.reply_text("⚠️ Сначала введите правильный пароль!")
        return
    
    await update.message.reply_text(
        "📋 Доступные команды:\n\n"
        "/info - информация о боте\n"
        "/status - ваш статус\n"
        "/logout - выйти из системы"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in authorized_users:
        await update.message.reply_text("⚠️ Сначала введите правильный пароль!")
        return
    
    await update.message.reply_text(
        "🤖 Это защищенный бот\n\n"
        "• Только авторизованные пользователи\n"
        "• Защита паролем\n"
        "• Безопасное соединение"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in authorized_users:
        await update.message.reply_text("⚠️ Сначала введите правильный пароль!")
        return
    
    user_data = authorized_users[user_id]
    await update.message.reply_text(
        f"📊 Ваш статус:\n\n"
        f"ID: {user_id}\n"
        f"Имя: {user_data['first_name']}\n"
        f"Юзернейм: @{user_data.get('username', 'не указан')}\n"
        f"Авторизован: {user_data['access_time'].strftime('%d.%m.%Y %H:%M')}"
    )

async def logout_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in authorized_users:
        del authorized_users[user_id]
        await update.message.reply_text("👋 Вы вышли из системы. Для доступа снова введите /start")
    else:
        await update.message.reply_text("Вы не авторизованы.")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("logout", logout_command))
    
    # Обработчик текстовых сообщений (для пароля)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()