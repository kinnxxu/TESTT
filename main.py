import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from moviepy.editor import TextClip, CompositeVideoClip
from instagrapi import Client

# ==============================
# ENV VARIABLES (SET IN RAILWAY)
# ==============================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")

OUTPUT_VIDEO = "output.mp4"

# ==============================
# VIDEO FUNCTION
# ==============================

def create_video(text):
    clip = TextClip(text, fontsize=70, color='white', size=(1080,1920))
    clip = clip.set_duration(5)

    video = CompositeVideoClip([clip])
    video.write_videofile(OUTPUT_VIDEO, fps=24)

    return OUTPUT_VIDEO

# ==============================
# INSTAGRAM FUNCTION
# ==============================

def upload_to_instagram(video_path, caption):
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)
    cl.video_upload(video_path, caption)

# ==============================
# TELEGRAM HANDLER
# ==============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("🎬 Creating video...")

    video_path = create_video(text)

    await update.message.reply_text("📤 Uploading...")

    upload_to_instagram(video_path, text)

    await update.message.reply_text("✅ Posted!")

# ==============================
# RUN BOT
# ==============================

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
