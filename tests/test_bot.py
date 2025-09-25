import pytest
from unittest.mock import AsyncMock, patch
from bot import handle_message

@pytest.mark.asyncio
async def test_handle_message_success():
    mock_update = AsyncMock()
    mock_update.message.text = "Hello bot"
    mock_update.message.chat_id = 123

    with patch("bot.call_gemini_api", new=AsyncMock(return_value="Hi human!")) as mock_gemini:
        await handle_message(mock_update, None)
        mock_gemini.assert_called_once_with("Hello bot")
        mock_update.message.reply_text.assert_called_once_with("Hi human!")


@pytest.mark.asyncio
async def test_handle_message_error():
    mock_update = AsyncMock()
    mock_update.message.text = "Error please"
    mock_update.message.chat_id = 123

    with patch("bot.call_gemini_api", new=AsyncMock(side_effect=Exception("Boom"))):
        await handle_message(mock_update, None)
        mock_update.message.reply_text.assert_called_once()
        assert "error" in mock_update.message.reply_text.call_args[0][0].lower()


@pytest.mark.asyncio
async def test_set_language_command():
    from language_manager import get_user_language

    mock_update = AsyncMock()
    mock_update.message.chat_id = 123
    mock_update.message.reply_text = AsyncMock()
    mock_update.message.text = "/language es"

    context = AsyncMock()
    context.args = ["es"]

    from bot import set_language
    await set_language(mock_update, context)

    assert get_user_language(123) == "es"
    mock_update.message.reply_text.assert_called_once_with("✅ Language set to es")


@pytest.mark.asyncio
async def test_handle_message_in_spanish():
    mock_update = AsyncMock()
    mock_update.message.text = "Hola bot"
    mock_update.message.chat_id = 123
    mock_update.message.reply_text = AsyncMock()

    with patch("bot.call_gemini_api", new=AsyncMock(return_value="¡Hola humano!")) as mock_gemini:
        from language_manager import set_user_language
        set_user_language(123, "es")

        from bot import handle_message
        await handle_message(mock_update, None)

        mock_gemini.assert_called_once_with("Hola bot", target_lang="es")
        mock_update.message.reply_text.assert_called_once_with("¡Hola humano!")
      
