import os


class MainView:
    @staticmethod
    def display_menu():
        print("\n" + "=" * 47)
        print("       ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ ")
        print("               EASYCHESS ")
        print("=" * 47 + "\n")

        print(" ╔════════════════════════════════════════════╗")
        print(" ║  -- Joueurs --                             ║")
        print(" ║  1. Menu Joueur                            ║")
        print(" ║                                            ║")
        print(" ║                                            ║")
        print(" ║  -- Tournois --                            ║")
        print(" ║  2. Menu Tournois                          ║")
        print(" ║                                            ║")
        print(" ║                                            ║")
        print(" ║  -- Quitter --                             ║")
        print(" ║  3. Quitter l'application                  ║")
        print(" ╚════════════════════════════════════════════╝")

        print("\n" + "=" * 47)

        return input(" Veuillez choisir une option : ")
