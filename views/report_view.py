class ReportView:
    def display_reports_menu(self) -> str:
        self.clear_terminal()
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"

        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                              ║\n"
        menu += "║  0. Liste de tous les joueurs (A-Z)         ║\n"
        menu += "║  1. Liste de tous les tournois              ║\n"
        menu += "║  2. Détails d'un tournoi (nom et dates)     ║\n"
        menu += "║  3. Liste des joueurs d'un tournoi (A-Z)    ║\n"
        menu += "║  4. Voir tous les tours et matchs d'un tournoi║\n"
        menu += "║  5. Retour au menu principal                ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"

        choice = input("Veuillez sélectionner une option : ")
        return choice
