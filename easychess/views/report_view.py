import time


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
        menu += "║  3. Détails d'un tournoi                    ║\n"
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
    
    def display_all_tournaments(self, tournaments):
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        menu += f"--- Liste des tournois ---"
        for key, tournament in tournaments.items():
            menu += f"\n{key}:\n"
            menu += f"  Nom: {tournament['name']}\n"
            menu += f"  Date de début: {tournament['start_date']}\n"
            menu += f"  Date de fin: {tournament['end_date']}\n"
            menu += f"  Nombre de tours: {tournament['number_of_rounds']}\n"
            menu += f"  Description: {tournament['description']}\n"
        print(menu)
        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice
    
    def display_tournaments_name(self, tournaments):
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               MENU RAPPORTS                 ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        for key, tournament in tournaments.items():
            menu += f"{key}:\n"
            menu += f"  Nom: {tournament['name']}\n"
        print(menu)    

    def ask_tournament_name_input(self):
        tournament_name = input("Veuillez saisir le Nom du tournoi : ")
        return tournament_name
    
    def display_tournament_details(self, tournament):
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔═════════════════════════════════════════════╗\n"
        menu += "║               DÉTAILS DU TOURNOI            ║\n"
        menu += "╚═════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        menu += f"Nom: {tournament['name']}\n"
        menu += f"Lieu: {tournament['location']}\n"
        menu += f"Date de début: {tournament['start_date']}\n"
        menu += f"Date de fin: {tournament['end_date']}\n"
        menu += "  Liste des joueurs:\n"
        for player in tournament['players']:
            menu += f"    - {player['last_name']} {player['first_name']}\n"
        menu += "  Liste des tours:\n"
        for round in tournament['list_rounds']:
            menu += f"    - {round['name']}\n"
            menu += "      Matchs:\n"
            for match in round['matches']:
                menu += f"        - {match[0][0]} vs {match[1][0]} - Score: {match[0][1]}-{match[1][1]}\n"
        menu += f"  Description: {tournament['description']}\n"
        print(menu)
        choice = input("Veuillez saisir 0 + entrée pour revenir au menu : ")
        return choice

    
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