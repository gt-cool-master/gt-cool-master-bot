import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["Старт обучения"],
        ["Курс + Чат (VIP Bonus)"],
        ["Поддержка", "О курсе"]
    ],
    resize_keyboard=True
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            f"Привет, админ! Добро пожаловать в систему управления ботом.",
            reply_markup=main_menu
        )
    else:
        await update.message.reply_text(
            "Добро пожаловать!\n"
            "Этот бот — твой проводник в мир кондиционирования:\n"
            "от простых сплитов до сложных VRF-систем.\n\n"
            "Жми кнопку ниже, чтобы начать обучение.",
            reply_markup=main_menu
        )

# Команда /admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Ты в панели администратора. Добро пожаловать!")
    else:
        await update.message.reply_text("У тебя нет доступа к админке.")

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Старт обучения":
        await update.message.reply_text(
            "Чтобы начать обучение, необходимо оплатить доступ к курсу.\n"
            "Стоимость: 999₽ (доступ навсегда)\n\n"
            "[Здесь будет ссылка на оплату]"
        )

    elif text == "Курс + Чат (VIP Bonus)":
        await update.message.reply_text(
            "Поддержка нужна не на месяц — а когда начинается настоящая работа.\n\n"
            "Подписка — это твой прямой канал к профессионалам.\n"
            "Задавай вопросы, получай помощь, решай проблемы по ходу.\n\n"
            "**Стоимость: 599₽ в месяц.**\n"
            "Меньше, чем одна ошибка на объекте.\n\n"
            "**Хочешь остаться навсегда?** Есть разовая покупка — 2,999₽.\n"
            "Только если ты уверен, что пойдёшь до конца.\n\n"
            "[Тут будет кнопка или ссылка для оформления доступа]"
        )

    elif text == "Поддержка":
        await update.message.reply_text(
            "Оставьте своё сообщение здесь — мы свяжемся с вами в ближайшее время."
        )

    elif text == "О курсе":
        await update.message.reply_text(
            "Курс включает обучение от простых до сложных систем (включая VRF),\n"
            "практику, расчёты по чертежам, составление смет и работу с клиентами.\n"
            "Материалы в тексте и таблицах. Доступ — навсегда."
        )
    else:
        await update.message.reply_text("Пожалуйста, используйте меню ниже.")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()