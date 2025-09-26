import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Env variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")   # ✅ AI Studio model

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your Gemini AI Bot. Type anything and I'll reply!")

# Handle normal messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(user_message))

        # Extract text safely
        reply = ""
        if response and response.candidates:
            parts = response.candidates[0].content.parts
            if parts:
                reply = parts[0].text

        if not reply:
            reply = "⚠️ No response from Gemini API."

        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        await update.message.reply_text(f"⚠️ Gemini API error: {e}")

# Main function
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhook setup (Render)
    port = int(os.environ.get("PORT", 10000))  # Render assigns PORT automatically
    render_url = os.getenv("RENDER_EXTERNAL_URL", "https://your-render-app.onrender.com")
    webhook_url = f"{render_url}/{TELEGRAM_BOT_TOKEN}"

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    main()
