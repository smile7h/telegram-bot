
import os
from telegram import Update, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8168574937:AAEEMmYUHK_wietmfyNv9DQRRrJ0K8NgI5k")
CHANNEL_ID = "@tabrizchannel"
SIGNATURE = "🔗 @tabrizchannel"

# حذف هر کلمه که با @ شروع میشه از متن
def clean_caption(caption):
    if not caption:
        return SIGNATURE
    words = caption.split()
    cleaned = [w for w in words if not w.startswith("@")]
    return " ".join(cleaned) + "\n\n" + SIGNATURE

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        msg = update.message

        # حذف فورواردر
        if msg.forward_from_chat or msg.forward_from:
            msg.forward_from_chat = None
            msg.forward_from = None

        if msg.text:
            text = clean_caption(msg.text)
            await context.bot.send_message(chat_id=CHANNEL_ID, text=text)

        elif msg.photo:
            caption = clean_caption(msg.caption)
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=msg.photo[-1].file_id, caption=caption)

        elif msg.video:
            caption = clean_caption(msg.caption)
            await context.bot.send_video(chat_id=CHANNEL_ID, video=msg.video.file_id, caption=caption)

        elif msg.document:
            caption = clean_caption(msg.caption)
            await context.bot.send_document(chat_id=CHANNEL_ID, document=msg.document.file_id, caption=caption)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات آنلاین است ✅")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_all))

app.run_polling()
