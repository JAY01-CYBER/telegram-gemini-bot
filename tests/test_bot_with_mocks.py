import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes

# Helper: create a fake update with text
def make_update(user_id=123, text="Hello Bot"):
    user = User(id=user_id, first_name="Test", is_bot=False)
    chat = Chat(id=user_id, type="private")
    message = Message(message_id=1, date=None, chat=chat, text=text, from_user=user)
    update = Update(update_id=1, message=message)
    return update

@pytest.mark.asyncio
@patch("bot.generate_reply", return_value="Mocked Gemini reply")
async def test_handle_message(mock_generate):
    from bot import handle_message

    update = make_update()
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.send_chat_action = AsyncMock()
    context.bot.send_message = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.edit_text = AsyncMock()

    await handle_message(update, context)

    mock_generate.assert_called_once()
    context.bot.send_chat_action.assert_called()

@pytest.mark.asyncio
@patch("bot.transcribe_audio", return_value="mocked voice text")
@patch("bot.generate_reply", return_value="Mocked Gemini voice reply")
async def test_handle_voice(mock_generate, mock_transcribe):
    from bot import handle_voice

    user = User(id=123, first_name="Test", is_bot=False)
    chat = Chat(id=123, type="private")
    message = AsyncMock()
    message.voice = AsyncMock(file_id="dummy")
    update = Update(update_id=2, message=message)

    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.send_chat_action = AsyncMock()
    update.message = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.edit_text = AsyncMock()

    await handle_voice(update, context)

    mock_transcribe.assert_called_once()
    mock_generate.assert_called_once()
