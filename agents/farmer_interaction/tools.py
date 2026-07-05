# Tools for voice transcription and synthesis


def translate_query(text: str, target_lang: str) -> dict:
    """Translate query to or from local farmer dialect.

    Args:
        text: Input text string.
        target_lang: ISO language code (en, es, sw).

    Returns:
        dict: Translation results.
    """
    return {"status": "success", "translated_text": text, "lang": target_lang}


def record_farm_activity_details(
    activity_type: str, quantity: float, unit: str, target_field: str, details: str
) -> dict:
    """Record the parsed details of a farm activity to be confirmed by the farmer.

    Args:
        activity_type: The type of activity (irrigation, fertilization, pest_treatment, or harvest).
        quantity: The amount or duration of the activity (e.g. 2.0, 10.0).
        unit: The unit of measurement (e.g. hours, kg, litres).
        target_field: The name of the field where the activity took place (e.g. 'north field').
        details: A description of what was done.

    Returns:
        dict: A status dict containing the parsed parameters.
    """
    return {
        "status": "success",
        "activity_type": activity_type,
        "quantity": quantity,
        "unit": unit,
        "target_field": target_field,
        "details": details,
    }
