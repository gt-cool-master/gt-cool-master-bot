import os
import json
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
VIP_USERS = set()  # временно, позже подключим базу
COURSE_USERS = set()

app = Flask(__name__)

keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Старт обучения")],
        [KeyboardButton("Курс + Чат (VIP Bonus)")],
        [KeyboardButton("Поддержка"), KeyboardButton("О курсе")]
    ],
    resize_keyboard=True
)

# ==== ОБРАБОТЧИКИ КНОПОК И КОМАНД ====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(f"Привет, админ! Твой ID: {user_id}", reply_markup=keyboard)
    else:
        await update.message.reply_text("Добро пожаловать! Выберите действие с помощью кнопок ниже.", reply_markup=keyboard)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "Старт обучения":
        if user_id in COURSE_USERS:
            await update.message.reply_text("Добро пожаловать на обучение! Вот ваш первый модуль: [ссылка]")
        else:
            await update.message.reply_text("Чтобы начать обучение, необходимо оплатить доступ. Стоимость курса: 999₽\n[Тут будет ссылка на оплату]")

    elif text == "Курс + Чат (VIP Bonus)":
        await update.message.reply_text(
            "Дополнительная опция: VIP-доступ с чатом поддержки.\n"
            "— Месячная подписка: 599₽/мес\n"
            "— Навсегда: 2,999₽\n\n"
            "Ты получаешь:\n"
            "— Общение с профи\n"
            "— Помощь в работе с клиентами\n"
            "— Поддержку и обратную связь\n\n"
            "Хочешь оформить доступ? [Тут будет кнопка/ссылка на оплату]"
        )

    elif text == "Поддержка":
        await update.message.reply_text("Оставьте своё сообщение здесь — мы свяжемся с вами в ближайшее время.")

    elif text == "О курсе":
        await update.message.reply_text(
            "Курс охватывает:\n"
            "— Установку кондиционеров от простых до VRF-систем\n"
            "— Чтение чертежей и расчёт смет\n"
            "— Продажи, общение с клиентами и закрытие сделок\n"
            "— Полная схема запуска с нуля\n\n"
            "Обучение проходит поэтапно с сопровождением."
        )

# ==== API ПЛАТЕЖЕЙ (CryptoCloud) ====

@app.route("/payment-notify", methods=["POST"])
def crypto_payment_notify():
    data = request.json
    if data and data.get("status") == "paid":
        order_id = data.get("order_id")
        telegram_id = int(order_id)  # мы передаём telegram_id как order_id

        # В зависимости от товара открываем доступ
        product = data.get("product", "").lower()
        if "vip" in product:
            VIP_USERS.add(telegram_id)
        else:
            COURSE_USERS.add(telegram_id)

        print(f"Доступ открыт пользователю {telegram_id} для: {product}")
    return "", 200

# ==== ЗАПУСК ====

if __name__ == "__main__":
    import threading

    async def telegram_bot():
        tg_app = ApplicationBuilder().token(BOT_TOKEN).build()
        tg_app.add_handler(CommandHandler("start", start))
        tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        await tg_app.run_polling()

    threading.Thread(target=lambda: app.run(port=5000)).start()

    import asyncio
    asyncio.run(telegram_bot())