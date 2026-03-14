import json
import os

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")

_translations = {}
_current_locale = "en"

def load_locale(locale: str) -> dict:
    locale_path = os.path.join(LOCALES_DIR, f"{locale}.json")
    if os.path.exists(locale_path):
        with open(locale_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def init_localization():
    global _translations
    
    available_locales = ["en", "es"]
    
    for locale in available_locales:
        _translations[locale] = load_locale(locale)
    
    for locale in available_locales:
        if locale not in _translations:
            _translations[locale] = {}
            
    print(f" [+] Loaded locales: {', '.join(available_locales)}")

def get_locale() -> str:
    return _current_locale

def set_locale(locale: str):
    global _current_locale
    if locale in _translations:
        _current_locale = locale
    else:
        _current_locale = "en"
        print(f" [!] Locale '{locale}' not found, using 'en'")

def t(key: str, default_locale: str = None) -> str:
    locale = default_locale if default_locale else _current_locale
    
    if locale in _translations and key in _translations[locale]:
        return _translations[locale][key]
    
    if "en" in _translations and key in _translations["en"]:
        return _translations["en"][key]
    
    return key

def get_translated_text(key: str, locale: str = None) -> str:
    return t(key, locale)

def get_all_translations(locale: str = None) -> dict:
    loc = locale if locale else _current_locale
    if loc in _translations:
        return _translations[loc]
    return {}

def get_available_locales() -> list:
    return list(_translations.keys())

def get_localized_game_config(locale: str = None) -> dict:
    from get_game_config import get_game_config
    
    config = get_game_config()
    loc = locale if locale else _current_locale
    
    if isinstance(config, dict) and "localization_strings" in config:
        for item in config["localization_strings"]:
            if isinstance(item, dict):
                key = item.get("name")
                if key:
                    translated = t(key, loc)
                    if translated != key:
                        item["text"] = translated
    
    return config

init_localization()
