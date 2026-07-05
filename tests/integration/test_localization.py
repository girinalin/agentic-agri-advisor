import ast
import json
import os
import re


def parse_js_dict(js_code, dict_name):
    match = re.search(dict_name + r"\s*=\s*(\{[\s\S]*?\n\s*\});", js_code)
    if not match:
        match = re.search(dict_name + r"\s*=\s*(\{[\s\S]*?\n\s*\})", js_code)
    if not match:
        raise ValueError(f"Could not find dictionary {dict_name} in javascript code")

    dict_str = match.group(1)
    # Strip single line comments
    dict_str = re.sub(r"//.*", "", dict_str)
    # Parse as Python literal dictionary
    return ast.literal_eval(dict_str)


def get_schema_keys():
    keys = set()
    schema_dir = "ui/schemas"
    for fname in os.listdir(schema_dir):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(schema_dir, fname), encoding="utf-8") as f:
            data = json.load(f)

        def recurse(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k.endswith("Key") and isinstance(v, str):
                        keys.add(v)
                    elif k in [
                        "titleKey",
                        "descriptionKey",
                        "labelKey",
                        "placeholderKey",
                        "textKey",
                        "descKey",
                        "valueKey",
                    ] and isinstance(v, str):
                        keys.add(v)
                    else:
                        recurse(v)
            elif isinstance(o, list):
                for item in o:
                    recurse(item)

        recurse(data)
    return keys


def test_translation_keys_defined():
    """Verify that all keys referenced in UI schemas are fully defined across all 5 languages."""
    with open("ui/agui/translations.js", encoding="utf-8") as f:
        js_code = f.read()

    translations = parse_js_dict(js_code, "TRANSLATIONS")
    schema_translations = parse_js_dict(js_code, "SCHEMA_TRANSLATIONS")

    languages = ["en", "hi", "mr", "te", "sw"]
    for lang in languages:
        assert lang in translations, f"Language '{lang}' missing in TRANSLATIONS"
        assert lang in schema_translations, (
            f"Language '{lang}' missing in SCHEMA_TRANSLATIONS"
        )

    schema_keys = get_schema_keys()

    # Assert each schema key is present for all 5 languages
    missing = []
    for key in schema_keys:
        for lang in languages:
            in_schema = key in schema_translations[lang]
            in_layout = key in translations[lang]
            if not in_schema and not in_layout:
                missing.append((key, lang))

    assert not missing, f"Missing translations in translations.js: {missing}"


def test_script_separation_and_leak_prevention():
    """Verify that Telugu characters never leak into Hindi, and Hindi/Devanagari characters never leak into Telugu."""
    with open("ui/agui/translations.js", encoding="utf-8") as f:
        js_code = f.read()

    translations = parse_js_dict(js_code, "TRANSLATIONS")
    schema_translations = parse_js_dict(js_code, "SCHEMA_TRANSLATIONS")

    # Telugu unicode block: \u0c00 - \u0c7f
    telugu_regex = re.compile(r"[\u0c00-\u0c7f]")
    # Devanagari unicode block: \u0900 - \u097f
    devanagari_regex = re.compile(r"[\u0900-\u097f]")

    # 1. Check Hindi mode contains no Telugu characters
    for key, val in translations["hi"].items():
        assert not telugu_regex.search(val), (
            f"Telugu character leak in Hindi TRANSLATIONS for key '{key}': {val}"
        )
    for key, val in schema_translations["hi"].items():
        assert not telugu_regex.search(val), (
            f"Telugu character leak in Hindi SCHEMA_TRANSLATIONS for key '{key}': {val}"
        )

    # 2. Check Telugu mode contains no Devanagari characters
    for key, val in translations["te"].items():
        assert not devanagari_regex.search(val), (
            f"Devanagari character leak in Telugu TRANSLATIONS for key '{key}': {val}"
        )
    for key, val in schema_translations["te"].items():
        assert not devanagari_regex.search(val), (
            f"Devanagari character leak in Telugu SCHEMA_TRANSLATIONS for key '{key}': {val}"
        )


def test_english_translation_cleanliness():
    """Verify that English translations are clean and free of unresolved keys or raw placeholders."""
    with open("ui/agui/translations.js", encoding="utf-8") as f:
        js_code = f.read()

    translations = parse_js_dict(js_code, "TRANSLATIONS")
    schema_translations = parse_js_dict(js_code, "SCHEMA_TRANSLATIONS")

    # English mode should not have Telugu or Devanagari characters
    telugu_regex = re.compile(r"[\u0c00-\u0c7f]")
    devanagari_regex = re.compile(r"[\u0900-\u097f]")

    for key, val in translations["en"].items():
        assert not telugu_regex.search(val), (
            f"Leak in English TRANSLATIONS for key '{key}'"
        )
        assert not devanagari_regex.search(val), (
            f"Leak in English TRANSLATIONS for key '{key}'"
        )

    for key, val in schema_translations["en"].items():
        assert not telugu_regex.search(val), (
            f"Leak in English SCHEMA_TRANSLATIONS for key '{key}'"
        )
        is_raw_key = "." in val and " " not in val and not val.endswith(".")
        assert not is_raw_key, (
            f"Suspected raw dot key in English value for key '{key}': {val}"
        )


def test_preservation_of_farmer_names():
    """Verify that the farmer's name 'माधव जी' is preserved correctly in Hindi and Marathi translations."""
    with open("ui/agui/translations.js", encoding="utf-8") as f:
        js_code = f.read()

    schema_translations = parse_js_dict(js_code, "SCHEMA_TRANSLATIONS")

    assert "माधव जी" in schema_translations["hi"]["home.greeting.title"]
    assert "माधव जी" in schema_translations["mr"]["home.greeting.title"]
    assert "మాధవ్ జీ" in schema_translations["te"]["home.greeting.title"]
