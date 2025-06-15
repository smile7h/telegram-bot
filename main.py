
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re

BOT_TOKEN = "8168574937:AAEEMmYUHK_wietmfyNv9DQRRrJ0K8NgI5k"
CHANNEL_ID = "@tabrizchannel"
SIGNATURE = "\n\n🔗 @tabrizchannel"

def clean_caption(caption):
    if not caption:
        return ""
    return re.sub(r"@\w+", "", caption)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    try:
        if msg.text:
            clean_text = re.sub(r"@\w+", "", msg.text).strip()
            await context.bot.send_message(chat_id=CHANNEL_ID, text=clean_text + SIGNATURE)
        elif msg.caption and msg.photo:
            clean = clean_caption(msg.caption).strip()
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=msg.photo[-1].file_id, caption=clean + SIGNATURE)
        elif msg.caption and msg.video:
            clean = clean_caption(msg.caption).strip()
            await context.bot.send_video(chat_id=CHANNEL_ID, video=msg.video.file_id, caption=clean + SIGNATURE)
        elif msg.document:
            clean = clean_caption(msg.caption).strip()
            await context.bot.send_document(chat_id=CHANNEL_ID, document=msg.document.file_id, caption=clean + SIGNATURE)
        elif msg.voice:
            await context.bot.send_voice(chat_id=CHANNEL_ID, voice=msg.voice.file_id)
        elif msg.audio:
            await context.bot.send_audio(chat_id=CHANNEL_ID, audio=msg.audio.file_id, caption=clean_caption(msg.caption) + SIGNATURE)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    handler = MessageHandler(filters.ALL, forward_message)
    app.add_handler(handler)
    print("Bot started...")
    app.run_polling()
