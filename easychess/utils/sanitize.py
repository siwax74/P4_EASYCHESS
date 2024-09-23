############################################################################################################
#  SANITIZE                                                                                                #
############################################################################################################
class Sanitize:
    def __init__(self, view):
        """
        Initializes the Sanitize class with a view.

        :param view: The view object for displaying messages.
        """
        self.view = view

    def sanitize_text(self, text):
        """
        Replaces accented characters in the input text with their non-accented counterparts.

        :param text: The input string potentially containing accented characters.
        :return: A string with accented characters replaced by non-accented characters.
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
