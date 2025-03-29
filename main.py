import os
from flask import Flask, request
import requests
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Инициализация Flask-сервера
app = Flask(__name__)

# Данные из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Сюда будем сохранять доступы
user_access = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        text = f"Привет, админ! Твой ID: {user_id}"
    else:
        text = (
            "Привет! Добро пожаловать в GT COOL MASTER BOT.\n"
            "Выберите действие с помощью кнопок ниже."
        )
    keyboard = [["Старт обучения"], ["Курс + Чат (VIP Bonus)"], ["Поддержка", "О курсе"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "Старт обучения":
        if user_access.get(user_id, {}).get("course"):
            await update.message.reply_text("Обучение уже доступно. Добро пожаловать!")
        else:
            await update.message.reply_text(
                "Чтобы начать обучение, необходимо оплатить доступ. Стоимость курса: 999₽\n"
                "[Тут будет ссылка на оплату]"
            )
    elif text == "Курс + Чат (VIP Bonus)":
        if user_access.get(user_id, {}).get("vip"):
            await update.message.reply_text("У тебя уже есть VIP доступ. Заходи в чат!")
        else:
            await update.message.reply_text(
                "Дополнительная опция: VIP-доступ с чатом поддержки.\n"
                "— Месячная подписка: 599₽/мес\n"
                "— Пожизненный доступ: 2,999₽\n\n"
                "Хочешь оформить доступ? [Тут будет кнопка или ссылка]"
            )
    elif text == "Поддержка":
        await update.message.reply_text(
            "Оставьте своё сообщение здесь — мы свяжемся с вами в ближайшее время."
        )
    elif text == "О курсе":
        await update.message.reply_text(
            "GT COOL MASTER — обучающий курс по установке кондиционеров всех типов:\n"
            "— Базовые, сплит-системы, VRF\n"
            "— Расчёт по чертежам, сметы, техника общения с клиентами\n\n"
            "Всё на практике, с поддержкой и гарантией результата."
        )
    else:
        await update.message.reply_text("Выберите действие с помощью кнопок ниже.")

# Webhook для приёма уведомлений от CryptoCloud
@app.route("/payment_webhook", methods=["POST"])
def payment_webhook():
    data = request.json
    if data.get("status") == "success":
        custom = data.get("custom_fields", {})
        user_id = int(custom.get("telegram_id", 0))
        product = custom.get("product", "")

        if user_id:
            if user_id not in user_access:
                user_access[user_id] = {}
            if "vip" in product.lower():
                user_access[user_id]["vip"] = True
            else:
                user_access[user_id]["course"] = True

            asyncio.run(send_telegram_message(user_id, "Спасибо за оплату! Доступ открыт."))
    return "ok", 200

# Отправка сообщений пользователям
async def send_telegram_message(user_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": user_id, "text": text})

# Запуск бота и Flask одновременно
def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)