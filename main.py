import dataHandler
import responseHandler
import mediaHandler
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler


DATA = dataHandler.load_data("user_data/data.csv")
PATTERNS, RESPONSES = responseHandler.set_respond_data("Bot_data/intents.json")


def get_user_data(update: Update) -> list:
    user = update.effective_user
    user_data =  [user.id, user.first_name, user.last_name, user.username]

    return user_data


async def start_command(update:Update, contex: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hey")
    user_data = get_user_data(update)
    if user_data[0] not in DATA["User_id"].values:
        dataHandler.add_data(user_data, DATA)
        dataHandler.save_data("user_data/data.csv", DATA)


async def vid_to_audio(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send the Video file of less then or equal to 5min long")
    await update.message.reply_text("this feature may not work properly")


async def img_to_pdf(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me the Image you want to convert to pdf")
    await update.message.reply_text("this feature may not work properly")


async def message_handler(update:Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = responseHandler.get_response(user_message.lower(), PATTERNS, RESPONSES)
    await update.message.reply_text(response)


async def receive_photo(update:Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = update.message.photo[-1]
    file_id = photo_file.file_id
    img = await context.bot.get_file(file_id)
    await img.download_to_drive(f"user_data/media/photos/{update.effective_user.id}.png")

    keyboard = [
        [InlineKeyboardButton("yes", callback_data="img_Yes")],
        [InlineKeyboardButton("No", callback_data="img_No")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("image received..!")
    await update.message.reply_text("Do you want me to convert the image to pdf?", reply_markup=reply_markup)
    


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_file = update.message.video

    if video_file.duration <= 300:
        file_id = video_file.file_id
        video = await context.bot.get_file(file_id)
        await update.message.reply_text("wait a moment....")
        print(video_file.duration)
        await video.download_to_drive(f"user_data/media/videos/{update.effective_user.id}.mp4")

        keyboard = [
            [InlineKeyboardButton("yes", callback_data="YES") ],
            [InlineKeyboardButton("No", callback_data="NO")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("video received..!")
        await update.message.reply_text("Do you want me to Extract the Audio?", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Video duration is too long try to send below 5min!")


async def extract_audio(update: Update, contect: ContextTypes.DEFAULT_TYPE):
    user = get_user_data(update)
    path = mediaHandler.cvtVideo_to_Audio(f"user_data/media/videos/{user[0]}.mp4",user[3])

    await update.effective_user.send_audio(audio=open(path, 'rb'),caption="Extracted audio")


async def cvtImg(update:Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_data(update)
    pdf_path = mediaHandler.cvtImg_to_pdf(f"user_data/media/photos/{user[0]}.png", user[3])

    await update.effective_user.send_document(document=open(pdf_path, 'rb'))



async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    await callback.answer()

    if callback.data == "img_Yes":
        await callback.edit_message_text("converting image to pdf wait a moment!")
        await cvtImg(update,context)

    if callback.data == "YES":
        await callback.edit_message_text("Extracting Audio wait a moment!")
        await extract_audio(update, context)
    else:
        await callback.edit_message_text("No problem!")
    
    


if __name__ == "__main__":
    
    #your token
    TOKEN = ""

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("get_Audio", vid_to_audio))
    app.add_handler(CommandHandler("get_pdf",img_to_pdf))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.add_handler(MessageHandler(filters.VIDEO, receive_video))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(CallbackQueryHandler(callback_handler))


    print("polling")
    app.run_polling(poll_interval=2)
