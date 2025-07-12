"""Automatic translation pipeline for frontend messages.

This script reads the Portuguese base translations from
``translations_pt.json`` and generates English and Spanish versions using
``googletrans`` if available. The resulting dictionaries are written back to
``bot_keydrop/frontend/src/js/i18n.js``.
"""

from __future__ import annotations

import json
from pathlib import Path

try:
    from googletrans import Translator
except Exception:  # pragma: no cover - optional dependency
    Translator = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
BASE_FILE = ROOT / "scripts" / "translations_pt.json"
I18N_FILE = ROOT / "bot_keydrop" / "frontend" / "src" / "js" / "i18n.js"

LANGS = {
    "en": "en",
    "es": "es",
}


def load_base() -> dict[str, str]:
    with open(BASE_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def translate_entries(base: dict[str, str], lang: str) -> dict[str, str]:
    if Translator is None:
        # Fallback: return keys untranslated
        return {k: v for k, v in base.items()}
    translator = Translator()
    translations = {}
    for key, text in base.items():
        try:
            translated = translator.translate(text, src="pt", dest=lang).text
        except Exception:
            translated = text
        translations[key] = translated
    return translations


def build_js_content(
    pt: dict[str, str],
    others: dict[str, dict[str, str]],
) -> str:
    lines = ["(function(global) {", "  const translations = {"]
    # Portuguese first
    lines.append("    pt: {")
    for k, v in pt.items():
        lines.append(f"      {k}: '{v}',")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("    },")
    for lang, data in others.items():
        lines.append(f"    {lang}: {{")
        for k, v in data.items():
            lines.append(f"      {k}: '{v}',")
        lines[-1] = lines[-1].rstrip(",")
        lines.append("    },")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("  };")
    lines.append("\n  let currentLanguage = ")
    lines.append("    localStorage.getItem('language') || 'pt';")
    lines.append(
        "  function t(key) {\n"
        "    return (translations[currentLanguage] && "
        "translations[currentLanguage][key]) ||\n"
        "           (translations.pt && translations.pt[key]) ||\n"
        "           key;\n  }"
    )
    lines.append(
        "  function setLanguage(lang) {\n"
        "    if (translations[lang]) {\n"
        "      currentLanguage = lang;\n"
        "      localStorage.setItem('language', lang);\n"
        "    }\n  }"
    )
    lines.append(
        "  function getLanguage() {\n" "    return currentLanguage;\n" "  }"
    )  # noqa: E501
    lines.append(
        "\n  global.i18n = { t, setLanguage, getLanguage };\n})(this);\n"
    )  # noqa: E501
    return "\n".join(lines)


def main() -> None:
    pt = load_base()
    translations = {
        lang: translate_entries(pt, code) for lang, code in LANGS.items()
    }  # noqa: E501
    content = build_js_content(pt, translations)
    I18N_FILE.write_text(content, encoding="utf-8")
    print(f"i18n file updated at {I18N_FILE}")


if __name__ == "__main__":
    main()
