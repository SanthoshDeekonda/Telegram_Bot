from bot import ChatBot
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # Log user information

    await update.message.reply_text("Hello! I'm your mental health support bot. How can I help you today?")