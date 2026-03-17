# ==============================
# CONFIG (EDIT THESE VALUES)
# ==============================

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

IG_USERNAME = "YOUR_INSTAGRAM_USERNAME"
IG_PASSWORD = "YOUR_INSTAGRAM_PASSWORD"

VIDEO_TEXT = "🔥 Fine Bearing Store Ludhiana"
OUTPUT_VIDEO = "output.mp4"


# ==============================
# IMPORTS
# ==============================

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from moviepy.editor import TextClip, CompositeVideoClip
from instagrapi import Client


# ==============================
# VIDEO GENERATION FUNCTION
# ==============================

def create_video(text):
    clip = TextClip(text, fontsize=80, color='white', size=(1080,1920))
    clip = clip.set_duration(5)

    video = CompositeVideoClip([clip])
    video.write_videofile(OUTPUT_VIDEO, fps=24)

    return OUTPUT_VIDEO


# ==============================
# INSTAGRAM UPLOAD FUNCTION
# ==============================

def upload_to_instagram(video_path, caption):
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)

    cl.video_upload(video_path, caption)
    print("Uploaded to Instagram!")


# ==============================
# TELEGRAM HANDLER
# ==============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("🎬 Creating video...")

    # Step 1: Create video
    video_path = create_video(user_text)

    await update.message.reply_text("📤 Uploading to Instagram...")

    # Step 2: Upload
    upload_to_instagram(video_path, user_text)

    await update.message.reply_text("✅ Posted successfully!")


# ==============================
# MAIN BOT RUNNER
# ==============================

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
