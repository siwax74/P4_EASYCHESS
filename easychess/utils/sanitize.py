############################################################################################################
#  SANITIZE                                                                                                #
############################################################################################################
class Sanitize:
    """
    Class to sanitize text input by replacing accented characters with their non-accented counterparts.

    Attributes:
        view (View): The view object for displaying messages.
    """

    def __init__(self, view):
        """
        Initializes the Sanitize class.

        Args:
            view (View): The view object for displaying messages.
        """
        self.view = view

    def sanitize_text(self, text):
        """
        Replaces accented characters in the given text with their non-accented counterparts.

        Args:
            text (str): The input text to sanitize.

        Returns:
            str: The sanitized text with accented characters replaced.
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
