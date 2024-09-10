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
        print(" ║  2. Liste des tournois en cours            ║")
        print(" ║  3. Liste des tournois a venir             ║")
        print(" ║  4. Démarrer tournois                      ║")
        print(" ║  5. Quitter le programme                   ║")
        print(" ╚════════════════════════════════════════════╝")

        print("\n" + "=" * 50)

        choice = input(" Entrez votre choix : ")
        return choice

    def ask_name(self):
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
        start_date = input("Date et heure de début du tournoi (ex: 25/02/2024 09:00) : ")
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

    def ask_player_selection(self):
        """
        Prompts the user to select players by their index from the list.

        Returns:
            list: A list of player indices entered by the user.
        """
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        selected_player_input = input(
            "Entrez les indices des joueurs sélectionnés, séparés par des virgules (par exemple : 1,3,5) : "
        )
        print("=" * 50 + "\n")
        return selected_player_input

    def ask_player_registration(self):
        """
        Asks the user if they want to register players automatically or manually.

        Returns:
            str: 'auto' if automatic registration, 'manual' if manual registration
        """
        while True:
            print("\n" + "=" * 50)
            registration_method = input(
                "Importer les joueurs automatiquement ou manuellement ? (a/m) : "
            )
            print("=" * 50 + "\n")
            if registration_method.lower() in ["a", "m"]:
                return registration_method.lower()
            else:
                self.display_error("Entrée invalide. Répondez par 'a' ou 'm'.")

    def display_selected_players(self, selected_players):
        """
        Displays the list of selected players.

        Args:
            selected_players (list): List of selected players
        """
        print(f"\nJoueurs sélectionnés ({len(selected_players)}) :")
        for player in selected_players:
            print(
                f"{player['first_name']} {player['last_name']} (Date de naissance: {player['birthdate']})"
            )

    def display_tournaments(self, tournaments):
        """
        Display the list of tournaments.
        """
        if not tournaments:
            print("Aucun tournoi à afficher.")
            return
        print("\n" + "=" * 50)
        print("Liste des tournois :")
        print()
        for tournament_id, tournament in tournaments.items():  
            print(f"ID: {tournament_id}")
            print(f"Nom: {tournament['name']}")
            print(f"Lieu: {tournament['location']}")
            print(f"Date de début: {tournament['start_date']}")
            print(f"Date de fin: {tournament['end_date']}")
            print(f"Nombre de rounds: {tournament['number_of_rounds']}")
            print(f"Description: {tournament['description']}")
            print(f"Joueurs:{([player['first_name'] + ' ' + player['last_name'] for player in tournament['players'].values()])}")
            print()
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")    
        print("1. Demarrer tournoi")
        return input("Veuilez saisir une option : ")
    
    def ask_confirmation_start_tournament(self, choosen_tournament_name):
        print(f"Vous avez choisi de démarrer le tournois, {choosen_tournament_name}")
        return input("Confirmer en apuyant sur la touche entré...")

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
