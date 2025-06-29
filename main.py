from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your chatbot. How can I assist you today?")




if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token=token).build()

    app.add_handler(CommandHandler("start", start_command))

    print("Bot is running...")
    print("polling...")
    app.run_polling()
    print("Bot has stopped.")