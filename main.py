import logging
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import threading
import requests

# ТВОИ ДАННЫЕ (уже встроены)
BOT_TOKEN = "8165265174:AAGJBQ0OgI6UVSDRj8KvuGWrTRydJpESMUE"
NOTIFY_CHAT_ID = 2100683151  # Твой Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask-приложение
app = Flask(__name__)

# Telegram Bot — команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Старт обучения"],
        ["Курс + Чат (VIP Bonus)"],
        ["Поддержка"],
        ["О курсе"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать в GT COOL MASTER BOT!", reply_markup=reply_markup)

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оставьте своё сообщение здесь — мы свяжемся с вами в ближайшее время.")

# Обработка входа на / (Render health check)
@app.route('/')
def home():
    return 'GT COOL MASTER BOT работает.'

# Обработка уведомлений от CryptoCloud
@app.route('/payment', methods=['POST'])
def payment_notification():
    data = request.json
    if data:
        status = data.get('status')
        amount = data.get('amount')
        currency = data.get('currency')
        email = data.get('email', 'не указан')
        product = data.get('order_description', 'не указано')

        message = (
            f"✅ Новый платёж!\n"
            f"Сумма: {amount} {currency}\n"
            f"Продукт: {product}\n"
            f"Email: {email}\n"
            f"Статус: {status}"
        )

        # Отправка сообщения в Telegram
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": NOTIFY_CHAT_ID, "text": message}
        )
        return '', 200
    return '', 400

# Запуск Telegram-бота и Flask одновременно
if __name__ == '__main__':
    def run_bot():
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("support", support))
        application.run_polling()

    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=5000)