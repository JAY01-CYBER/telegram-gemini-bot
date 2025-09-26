import os
import time
import logging
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from language_manager import set_user_language, get_user_language
from utils import clean_text
from voice_utils import transcribe_audio

# 🔹 Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔹 Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.environ.get("PORT", "8443"))
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is not set!")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is not set!")

# 🔹 Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# 🔹 Conversation memory {user_id: [messages]}
user_conversations = {}
MAX_HISTORY = 10

# 🔹 Rate limiting {user_id: timestamp}
last_request_time = {}
COOLDOWN_SECONDS = 5

def is_rate_limited(user_id: int) -> bool:
    now = time.time()
    if user_id in last_request_time:
        elapsed = now - last_request_time[user_id]
        if elapsed < COOLDOWN_SECONDS:
            return True
    last_request_time[user_id] = now
    return False

# 🔹 Gemini helper
def generate_reply(prompt: str, history: list) -> str:
    try:
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API error: {e}"

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User %s started bot", update.effective_user.id)
    await update.message.reply_text("👋 Hello! I’m your Gemini AI Bot. Send me a text or voice message.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_conversations[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]
    logger.info("Conversation reset for user %s", user_id)
    await update.message.reply_text("🧹 Conversation reset!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_rate_limited(user_id):
        await update.message.reply_text("⏳ Please wait a few seconds before sending another message.")
        return

    user_text = update.message.text
    logger.info("Message from %s: %s", user_id, user_text)

    prompt = clean_text(user_text)

    if user_id not in user_conversations:
        user_conversations[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]

    user_conversations[user_id].append({"role": "user", "content": prompt})
    user_conversations[user_id] = user_conversations[user_id][-MAX_HISTORY:]

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        sent_msg = await update.message.reply_text("💭 Thinking...")

        reply = await asyncio.to_thread(generate_reply, prompt, user_conversations[user_id])
        await sent_msg.edit_text(reply.strip())

        user_conversations[user_id].append({"role": "assistant", "content": reply})
        logger.info("Reply to %s: %s", user_id, reply)

    except Exception as e:
        error_msg = f"⚠️ Error: {e}"
        logger.error("Gemini error for user %s: %s", user_id, e)
        await update.message.reply_text(error_msg)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_rate_limited(user_id):
        await update.message.reply_text("⏳ Please wait a few seconds before sending another voice message.")
        return

    logger.info("Voice message received from %s", user_id)

    voice = update.message.voice
    if not voice:
        await update.message.reply_text("Cannot process voice.")
        return

    file = await context.bot.get_file(voice.file_id)
    file_path = await file.download_to_drive()

    text = await transcribe_audio(file_path)
    if not text:
        await update.message.reply_text("Could not transcribe voice.")
        return

    logger.info("Transcribed voice from %s: %s", user_id, text)
    prompt = clean_text(text)

    if user_id not in user_conversations:
        user_conversations[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]

    user_conversations[user_id].append({"role": "user", "content": prompt})
    user_conversations[user_id] = user_conversations[user_id][-MAX_HISTORY:]

    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        sent_msg = await update.message.reply_text("🎙️ Processing your voice...")

        reply = await asyncio.to_thread(generate_reply, prompt, user_conversations[user_id])
        await sent_msg.edit_text(reply.strip())

        user_conversations[user_id].append({"role": "assistant", "content": reply})
        logger.info("Reply to %s (voice): %s", user_id, reply)

    except Exception as e:
        error_msg = f"⚠️ Error: {e}"
        logger.error("Gemini error (voice) for user %s: %s", user_id, e)
        await update.message.reply_text(error_msg)

# --- Main ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    if HOSTNAME:  # Render (webhook mode)
        logger.info("🌐 Starting bot in WEBHOOK mode: https://%s/%s", HOSTNAME, TELEGRAM_TOKEN)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TELEGRAM_TOKEN,
            webhook_url=f"https://{HOSTNAME}/{TELEGRAM_TOKEN}"
        )
    else:  # Local dev (polling mode)
        logger.info("🖥️ Starting bot in POLLING mode")
        app.run_polling()

if __name__ == "__main__":
    main()


async def set_language(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /language <code>, e.g., /language es")
        return
    lang = context.args[0]
    set_user_language(update.message.chat_id, lang)
    await update.message.reply_text(f"✅ Language set to {lang}")