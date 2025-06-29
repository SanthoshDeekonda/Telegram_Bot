from bot import Bot
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os


bot = Bot()
bot.load_data('training_data.json')
bot.train()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    start_response = """
        Hello! I'm Sunny, your personal therapeutic AI assistant. 🌼

        I'm here to listen, support, and guide you through your thoughts and feelings — or even help you with basic first-aid advice if needed.

        You can say things like:
        - "I'm feeling anxious"
        - "How do I treat a cut?"
        - "Hi Sunny"
        - "I feel tired"
        - "Tell me a joke"

        So, how are you feeling today?

        """

    await update.message.reply_text(start_response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    response = bot.get_response(user_input)
    await update.message.reply_text(response)




if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token=token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    print("polling...")
    app.run_polling()
    print("Bot has stopped.")