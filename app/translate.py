from libretranslatepy import LibreTranslateAPI
from flask import current_app

def translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate the given text from source_lang to target_lang using LibreTranslate API.

    :param text: The text to be translated.
    :param source_lang: The source language code (e.g., 'en' for English).
    :param target_lang: The target language code (e.g., 'es' for Spanish).
    :return: The translated text.
    """
    try:
        lt = LibreTranslateAPI(current_app.config['LIBRETRANSLATE_URL'])  # Adjust the URL if your LibreTranslate server is running elsewhere
        translated_text = lt.translate(text, source=source_lang, target=target_lang)
        return translated_text
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Translation error: {e}")
        return text  # Return the original text if translation fails