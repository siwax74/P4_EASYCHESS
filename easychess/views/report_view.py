class ReportView:
    def display_reports_menu(self) -> str:
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                              ║\n"
        menu += "║  1. Liste de tous les joueurs (A-Z)         ║\n"
        menu += "║  2. Liste de tous les tournois              ║\n"
        menu += "║  3. Détails d'un tournoi (nom et dates)     ║\n"
        menu += "║  4. Liste des joueurs d'un tournoi (A-Z)    ║\n"
        menu += "║  5. Voir les tours et matchs d'un tournoi   ║\n"
        menu += "║  0. Retour au menu principal                ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        print(menu)
        choice = input("Veuillez sélectionner une option : ")
        return choice

    def display_alphabetical_players(self, formatted_players):
        # Construction du menu
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        for player in formatted_players:
            menu += (player + "\n")  # Ajout de chaque joueur formaté avec un saut de ligne
        print(menu)

        # Demander à l'utilisateur d'entrer une commande
        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice