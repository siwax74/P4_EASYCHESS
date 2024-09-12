import os


class MainView:
    @staticmethod
    def display_menu():
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔════════════════════════════════════════════╗\n"
        menu += "║  -- Joueurs --                             ║\n"
        menu += "║  1. Menu Joueur                            ║\n"
        menu += "║                                            ║\n"
        menu += "║                                            ║\n"
        menu += "║  -- Tournois --                            ║\n"
        menu += "║  2. Menu Tournois                          ║\n"
        menu += "║                                            ║\n"
        menu += "║                                            ║\n"
        menu += "║  -- Quitter --                             ║\n"
        menu += "║  3. Quitter l'application                  ║\n"
        menu += "╚════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"

        print(menu)
        return input(" Veuillez choisir une option : ")
