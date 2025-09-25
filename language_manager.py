# language_manager.py

# Simple in-memory user language store
# (for production, replace with DB or Redis)

user_languages = {}

def set_user_language(user_id: int, lang: str):
    """Set preferred language for a user."""
    user_languages[user_id] = lang

def get_user_language(user_id: int) -> str:
    """Get user's preferred language (default: English)."""
    return user_languages.get(user_id, "en")
