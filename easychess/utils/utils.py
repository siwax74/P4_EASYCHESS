import os
import platform
import time


class Utils:
    @staticmethod
    def clear_terminal():
        """
        Clear the terminal screen based on the operating system.
        """
        if platform.system() == "Windows":
            time.sleep(0.50)
            os.system("cls")
        else:
            time.sleep(0.50)
            os.system("clear")

    def display_error(self, message):
        """
        Display an error message in a formatted manner.

        :param message: The error message to be displayed.
        """
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERREUR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)

    def display_success(self, message):
        """
        Display a success message in a formatted manner.

        :param message: The success message to be displayed.
        """
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCÈS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)
