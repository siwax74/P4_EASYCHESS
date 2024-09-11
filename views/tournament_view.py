import time


class TournamentView:
    def display_tournament_menu(self) -> str:
        print("\n" + "=" * 50)
        print("         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ ")
        print("                 EASYCHESS ")
        print("=" * 50 + "\n")

        print(" ╔════════════════════════════════════════════╗")
        print(" ║               MENU TOURNOIS                ║")
        print(" ╚════════════════════════════════════════════╝")

        print(" ╔════════════════════════════════════════════╗")
        print(" ║  -- Actions --                             ║")
        print(" ║  1. Ajouter un nouveau tournoi             ║")
        print(" ║  2. Liste des tournois à venir             ║")
        print(" ║  3. Liste des tournois en cours            ║")
        print(" ║  4. Démarrer tournoi                       ║")
        print(" ║  5. Quitter le programme                   ║")
        print(" ╚════════════════════════════════════════════╝")

        print("\n" + "=" * 50)

        choice = input(" Entrez votre choix : ")
        return choice

    def ask_name(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        print("\n" + "=" * 50)
        name = input("Entrez le nom du tournoi : ")
        print("=" * 50 + "\n")
        return name

    def ask_location(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        location = input("Entrez la localisation du tournoi : ")
        print("=" * 50 + "\n")
        return location

    def ask_start_date(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        start_date = input(
            "Date et heure de début du tournoi (ex: 25/02/2024 09:00) : "
        )
        print("=" * 50 + "\n")
        return start_date

    def ask_end_date(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        end_date = input("Entrez la date de fin du tournoi (JJ/MM/AAAA) : ")
        print("=" * 50 + "\n")
        return end_date

    def ask_rounds(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        rounds = input("Nombre de rounds (par défaut: 4) : ")
        print("=" * 50 + "\n")
        return rounds if rounds.strip() else None

    def ask_description(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        description = input("Entrez une description du tournoi : ")
        print("=" * 50 + "\n")
        return description

    def ask_player_registration_method(self):
        """
        Asks the user if they want to register players automatically or manually.

        Returns:
            str: 'manual' if manual registration, 'auto' if automatic registration
        """
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        print("\n" + "=" * 50)
        print("1. Importer les joueurs automatiquement")
        print("2. Importer les joueurs manuellement")
        print("3. Crée et importer un joueur")
        print("=" * 50 + "\n")
        method = input("Choisissez une option (1, 2 ou 3) : ").strip()
        return method
    
    def ask_add_another_player(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        input_add_another_player = input("Souhaitez vous ajouter d'autre joueurs au tournoi ? (o/n): ")
        print("=" * 50 + "\n")
        return input_add_another_player.lower()
    
    def ask_player_selection(self, players):
        """
        Prompts the user to select players by their index from the list.

        Returns:
            list: A list of player indices entered by the user.
        """
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        print("\n" + "=" * 50)
        for i, player in enumerate(players, start=1):
            print(f"{i}. {player['last_name']} {player['first_name']}")
        selected_player_input = input(
            "Veuillez saisir le numéro des joueurs à ajouter au tournoi (séparés par des espaces) : "
        )
        print("=" * 50 + "\n")
        return selected_player_input


    def display_tournament_list(self, tournament_data):
        print("\n" + "=" * 50)
        for tournament in tournament_data:
            print("\n" + "=" * 50)
            print(f"ID: {tournament['id']}")
            print(f"Nom: {tournament['name']}")
            print(f"Emplacement: {tournament['location']}")
            print(f"Date de début: {tournament['start_date']}")
            print(f"Date de fin: {tournament['end_date']}")
            print(f"Nombre de tours: {tournament['number_of_rounds']}")
            print(f"Tour actuel: {tournament['current_round']}")
            print(f"Listes des tours: {tournament['list_rounds']}")
            print(f"Description: {tournament['description']}")
            
            if tournament['player_details']:
                print("Liste des joueurs inscrits :")
                for player in tournament['player_details']:
                    print(f"  - {player['first_name']} {player['last_name']}, Date de naissance: {player['birthdate']}, ID National: {player['national_id']}")
            else:
                print("Pas de joueurs inscrits.")
            
            print("=" * 50)

    def ask_confirmation_start_tournament(self, choosen_tournament_name):
        print("\n" + "=" * 50)
        print(f"Vous avez choisi de démarrer le tournoi: {choosen_tournament_name}")
        print("=" * 50)
        return input("Confirmer en appuyant sur la touche Entrée...")

    def display_error(self, message):
        print("\n" + "=" * 50)
        print(f"⚠️  ERREUR: {message}")
        print("=" * 50 + "\n")
        time.sleep(2)

    def display_success(self, message):
        print("\n" + "=" * 50)
        print(f"✔️  SUCCÈS: {message}")
        print("=" * 50 + "\n")
        time.sleep(2)
