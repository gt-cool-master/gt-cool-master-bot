import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import os

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Получаем токен и данные от окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # для логов
app = Flask(__name__)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Добро пожаловать в GT COOL MASTER. Готов учиться?")

# Обработчик для уведомлений от CryptoCloud
@app.route("/payment", methods=["POST"])
def payment_notification():
    data = request.json
    if data:
        user_id = data.get("order_id")
        amount = data.get("amount_crypto")
        currency = data.get("currency")
        payment_type = data.get("description")

        # Отправка уведомления админу
        app.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Поступил платёж!\nID: {user_id}\nСумма: {amount} {currency}\nТип: {payment_type}"
        )
    return "OK", 200

# Основной запуск
if __name__ == "__main__":
    from telegram.ext import Application

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    app.bot = application.bot

    application.add_handler(CommandHandler("start", start))

    import threading
    threading.Thread(target=application.run_polling, name="BotThread").start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)