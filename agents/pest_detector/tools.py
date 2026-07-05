# Tools for pest & disease detection


def prescribe_treatment(pest_name: str, crop: str) -> dict:
    """Prescribe biological or chemical treatment for a detected pest/disease.

    Args:
        pest_name: Name of the detected pest or disease.
        crop: Crop species affected.

    Returns:
        dict: Treatment prescription details.
    """
    return {
        "status": "success",
        "treatment": "Apply organic neem oil spray.",
        "urgency": "high",
    }
