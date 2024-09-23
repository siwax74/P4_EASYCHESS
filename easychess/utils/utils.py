import os
import platform
import time


class Utils:
    @staticmethod
    def clear_terminal():
        """Efface le terminal en fonction du système d'exploitation."""
        if platform.system() == "Windows":
            time.sleep(0.50)
            os.system("cls")
        else:
            time.sleep(0.50)
            os.system("clear")

    def display_error(self, message):
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERREUR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)

    def display_success(self, message):
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCÈS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(1)