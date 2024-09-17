class Sanitize:
    def __init__(self, view):
        self.view = view

    def sanitize_text(self, text):
        """
        Replace accented characters with their non-accented counterparts.
        """
        accents = {
            "é": "e",
            "è": "e",
            "à": "a",
            "ù": "u",
            "ç": "c",
            "â": "a",
            "ê": "e",
            "î": "i",
            "ô": "o",
            "û": "u",
            "ä": "a",
            "ë": "e",
            "ï": "i",
            "ö": "o",
            "ü": "u",
            "ÿ": "y",
        }
        for accented, non_accented in accents.items():
            text = text.replace(accented, non_accented)
        return text
