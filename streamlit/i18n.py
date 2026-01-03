# -*- coding: utf-8 -*-
"""
Internationalization (i18n) module for Streamlit Holiday Greeting QR application.

Provides translation infrastructure for multi-language support using session state
and JSON-based translation files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st


# Path to translations file
TRANSLATIONS_FILE = Path(__file__).parent / "translations.json"

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "中文 (简体)"
}

# Default language
DEFAULT_LANGUAGE = "en"

# Cache for loaded translations
_translations_cache: Optional[Dict[str, Dict[str, str]]] = None


def load_translations() -> Dict[str, Dict[str, str]]:
    """
    Load translations from JSON file.

    Returns:
        Dictionary with language codes as keys and translation dictionaries as values.
        Example: {"en": {"key": "value"}, "zh": {"key": "值"}}
    """
    global _translations_cache

    # Return cached translations if available
    if _translations_cache is not None:
        return _translations_cache

    # Load translations from file
    if not TRANSLATIONS_FILE.exists():
        st.error(f"Translations file not found: {TRANSLATIONS_FILE}")
        return {"en": {}, "zh": {}}

    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            translations = json.load(f)
            _translations_cache = translations
            return translations
    except json.JSONDecodeError as e:
        st.error(f"Error parsing translations file: {e}")
        return {"en": {}, "zh": {}}
    except Exception as e:
        st.error(f"Error loading translations: {e}")
        return {"en": {}, "zh": {}}


def init_language():
    """
    Initialize language setting in session state.
    Call this once at app startup before any translation calls.
    """
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE


def get_current_language() -> str:
    """
    Get the currently selected language code.

    Returns:
        Language code (e.g., "en", "zh")
    """
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def set_language(lang_code: str):
    """
    Set the active language and trigger app rerun.

    Args:
        lang_code: Language code to set (e.g., "en", "zh")
    """
    if lang_code in SUPPORTED_LANGUAGES:
        st.session_state.language = lang_code
        st.rerun()
    else:
        st.warning(f"Unsupported language code: {lang_code}")


def get_text(key: str, **kwargs) -> str:
    """
    Get translated text for the given key in the current language.

    Implements fallback chain: current language → English → show key
    Supports variable substitution using keyword arguments.

    Args:
        key: Translation key in dot notation (e.g., "app.sidebar.title")
        **kwargs: Variables to substitute in the translated text

    Returns:
        Translated text with variables substituted

    Examples:
        >>> get_text("app.sidebar.title")
        "Holiday Greeting QR"

        >>> get_text("qr.stats", bytes=1024, version=5)
        "Data size: 1024 bytes, Version: 5"
    """
    # Get current language
    current_lang = get_current_language()

    # Load translations
    translations = load_translations()

    # Try to get translation in current language
    if current_lang in translations and key in translations[current_lang]:
        text = translations[current_lang][key]
    # Fallback to English
    elif "en" in translations and key in translations["en"]:
        text = translations["en"][key]
    # Show missing key indicator
    else:
        return f"[missing: {key}]"

    # Substitute variables if provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            st.warning(f"Missing variable in translation '{key}': {e}")
        except Exception as e:
            st.warning(f"Error formatting translation '{key}': {e}")

    return text


def get_language_selector():
    """
    Create a language selector widget for the sidebar.

    Returns:
        Streamlit selectbox widget for language selection
    """
    current_lang = get_current_language()

    # Create language options with display names
    language_options = list(SUPPORTED_LANGUAGES.keys())
    language_labels = [SUPPORTED_LANGUAGES[code] for code in language_options]

    # Find current index
    try:
        current_index = language_options.index(current_lang)
    except ValueError:
        current_index = 0

    # Create selectbox
    selected_label = st.selectbox(
        "🌐 Language / 语言",
        options=language_labels,
        index=current_index,
        key="language_selector"
    )

    # Get selected language code
    selected_index = language_labels.index(selected_label)
    selected_code = language_options[selected_index]

    # Update language if changed
    if selected_code != current_lang:
        set_language(selected_code)

    return selected_code


# Convenience alias for shorter code
_ = get_text
