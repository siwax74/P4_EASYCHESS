class MainView:
    @staticmethod
    def display_menu():
        print("\n" + "=" * 40)
        print("       ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ ")
        print("               EASYCHESS ")
        print("=" * 40 + "\n")

        print(" ╔════════════════════════════════════╗")
        print(" ║               MENU                 ║")
        print(" ╚════════════════════════════════════╝")

        print(" ║  -- Joueurs --                     ║")
        print(" ║  1. Menu Joueur                    ║")
        print(" ║                                    ║")

        print(" ║  -- Tournois --                    ║")
        print(" ║  2. Menu Tournois                  ║")
        print(" ║                                    ║")

        print(" ║  -- Quitter --                     ║")
        print(" ║  3. Quitter l'application          ║")
        print(" ╚════════════════════════════════════╝")

        print("\n" + "=" * 40)

        return input(" Veuillez choisir une option : ")
