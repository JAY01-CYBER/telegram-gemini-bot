import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# ✅ Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ✅ Configure Gemini AI with AI Studio API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# ✅ Select AI Studio model (no Vertex path)
model = genai.GenerativeModel("gemini-1.5-flash")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your Gemini AI Bot. Type anything and I'll reply!")

# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # Async call to Gemini
        response = await model.generate_content_async(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        await update.message.reply_text("⚠️ Sorry, something went wrong with Gemini API.")

def main():
    # ✅ Get Telegram bot token
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

    app = ApplicationBuilder().token(token).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ✅ Use webhook or polling based on Render
    port = int(os.environ.get("PORT", 10000))
    url = os.environ.get("RENDER_EXTERNAL_URL")

    if url:
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=f"{url}/{token}"
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
