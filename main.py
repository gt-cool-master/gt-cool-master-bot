import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(f"Привет, админ! Твой ID: {2100683151}")
    else:
        await update.message.reply_text(f"Привет! Ты не админ. Твой ID: {2100683151}")