from ..utils.utils import Utils


class MainView:
    @staticmethod
    def display_menu():
        Utils.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Joueurs --                              ║\n"
        menu += "║  1. Menu Joueur                             ║\n"
        menu += "║                                             ║\n"
        menu += "║  -- Tournois --                             ║\n"
        menu += "║  2. Menu Tournois                           ║\n"
        menu += "║                                             ║\n"
        menu += "║  -- Rapports --                             ║\n"
        menu += "║  3. Menu Rapports                           ║\n"
        menu += "║                                             ║\n"
        menu += "║  -- Quitter --                              ║\n"
        menu += "║  4. Quitter l'application                   ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        print(menu)
        return input(" Veuillez choisir une option : ")


