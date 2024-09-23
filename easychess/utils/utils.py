############################################################################################################
#  UTILS                                                                                                   #
############################################################################################################
import os
import platform
import time


class Utils:
    @staticmethod
    def clear_terminal():
        """
        Clears the terminal based on the operating system.
        """
        if platform.system() == "Windows":
            time.sleep(0.50)
            os.system("cls")
        else:
            time.sleep(0.50)
            os.system("clear")

    def display_error(self, message):
        """
        Displays a formatted error message in the terminal.

        :param message: The error message to display.
        """
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERROR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)

    def display_success(self, message):
        """
        Displays a formatted success message in the terminal.

        :param message: The success message to display.
        """
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCESS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)
