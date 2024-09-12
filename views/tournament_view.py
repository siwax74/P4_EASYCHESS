import time

class TournamentView:
    def display_tournament_menu(self) -> str:
        menu = "=" * 47 + "\n"
        menu += "         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ \n"
        menu += "                 EASYCHESS \n"
        menu += "=" * 47 + "\n"
        menu += "╔════════════════════════════════════════════╗\n"
        menu += "║               MENU TOURNOIS                ║\n"
        menu += "╚════════════════════════════════════════════╝\n"
        menu += "╔════════════════════════════════════════════╗\n"
        menu += "║  -- Actions --                             ║\n"
        menu += "║  1. Ajouter un nouveau tournoi             ║\n"
        menu += "║  2. Liste des tournois à venir             ║\n"
        menu += "║  3. Liste des tournois en cours            ║\n"
        menu += "║  4. Démarrer tournoi                       ║\n"
        menu += "║  5. Quitter le programme                   ║\n"
        menu += "╚════════════════════════════════════════════╝\n"
        menu += "=" * 47 + "\n"
        print(menu)
        choice = input(" Entrez votre choix : ")
        return choice

    def ask_name(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        name = input("Entrez le nom du tournoi : ")
        return name

    def ask_location(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        location = input("Entrez la localisation du tournoi : ")
        return location

    def ask_start_date(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        start_date = input("Date et heure de début du tournoi (ex: 25/02/2024 09:00) : ")
        return start_date

    def ask_end_date(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        end_date = input("Entrez la date de fin du tournoi (JJ/MM/AAAA) : ")
        return end_date

    def ask_rounds(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        rounds = input("Nombre de rounds (par défaut: 4) : ")
        return rounds if rounds.strip() else None

    def ask_description(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        description = input("Entrez une description du tournoi : ")
        return description

    def ask_player_registration_method(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        menu += "1. Importer les joueurs automatiquement\n"
        menu += "2. Importer les joueurs manuellement\n"
        menu += "3. Crée et importer un joueur\n"
        print(menu)
        method = input("Choisissez une option (1, 2 ou 3) : ").strip()
        return method

    def ask_add_another_player(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        input_add_another_player = input("Souhaitez-vous ajouter d'autres joueurs au tournoi ? (o/n): ")
        return input_add_another_player.lower()

    def ask_player_selection(self, players):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        for i, player in enumerate(players, start=1):
            menu += f"{i}. {player['last_name']} {player['first_name']}\n"
        print(menu)
        selected_player_input = input(
            "Veuillez saisir le numéro des joueurs à ajouter au tournoi (séparés par des espaces) : "
        )
        return selected_player_input

    def ask_start_tournament(self):
        menu = "=" * 47 + "\n"
        menu += "0. Revenir au menu principal\n"
        print(menu)
        start_tournament_input = input("Souhaitez-vous commencer le tournoi ? : ")
        return start_tournament_input.lower()

    def display_tournament_list(self, tournament_data):
        menu = "\n" + "=" * 47 + "\n"
        for tournament in tournament_data:
            menu += "\n" + "=" * 47 + "\n"
            menu += f"ID: {tournament['id']}\n"
            menu += f"Nom: {tournament['name']}\n"
            menu += f"Emplacement: {tournament['location']}\n"
            menu += f"Date de début: {tournament['start_date']}\n"
            menu += f"Date de fin: {tournament['end_date']}\n"
            menu += f"Nombre de tours: {tournament['number_of_rounds']}\n"
            menu += f"Tour actuel: {tournament['current_round']}\n"
            menu += f"Listes des tours: {tournament['list_rounds']}\n"
            menu += f"Description: {tournament['description']}\n"
            
            if tournament['player_details']:
                menu += "Liste des joueurs inscrits :\n"
                for player in tournament['player_details']:
                    menu += f"  - {player['first_name']} {player['last_name']}, Date de naissance: {player['birthdate']}, ID National: {player['national_id']}\n"
            else:
                menu += "Pas de joueurs inscrits.\n"
        menu += "=" * 47 + "\n"
        print(menu)

    def display_error(self, message):
        menu = "=" * 47 + "\n"
        menu += f"⚠️  ERREUR: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(2)

    def display_success(self, message):
        menu = "=" * 47 + "\n"
        menu += f"✔️  SUCCÈS: {message}\n"
        menu += "=" * 47 + "\n"
        print(menu)
        time.sleep(2)