import time


class PlayerView:
    def display_player_menu(self) -> str:
        print("\n" + "=" * 50)
        print("         ♛ ♚ ♜ ♝ ♞ ♟ ♔ ♕ ♖ ♗ ♘ ♙ ")
        print("                 EASYCHESS ")
        print("=" * 50 + "\n")

        print(" ╔════════════════════════════════════════════╗")
        print(" ║               MENU JOUEUR                  ║")
        print(" ╚════════════════════════════════════════════╝")

        print(" ║  -- Actions --                             ║")
        print(" ║  1. Ajouter un nouveau joueur              ║")
        print(" ║  2. Voir liste de joueurs                  ║")
        print(" ╚════════════════════════════════════════════╝")

        print("\n" + "=" * 50)

        return input(" Veuillez choisir une option : ")

    def ask_first_name(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        first_name = input("Entrez le prénom du joueur : ")
        print("=" * 50 + "\n")
        return first_name

    def ask_last_name(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        last_name = input("Entrez le nom du joueur : ")
        print("=" * 50 + "\n")
        return last_name

    def ask_birthdate(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        birthdate = input("Date de naissance du joueur (jj/mm/aaaa) : ")
        print("=" * 50 + "\n")
        return birthdate

    def ask_national_id(self):
        print("\n" + "=" * 50)
        print("0. Revenir au menu principal")
        national_id = input("Entrez le N° d'identité nationale du joueur : ")
        print("=" * 50 + "\n")
        return national_id

    def player_list(self, players):
        print("\n" + "=" * 50)
        print("      --- Liste des joueurs ---      ")
        print("=" * 50)
        for key, player in players.items():
            print(
                f"{key}: {player['first_name']} {player['last_name']} "
                f"{player['birthdate']} {player['national_id']}"
            )
        print("=" * 50 + "\n")
        time.sleep(2)

    def ask_to_return_to_menu(self):
        """
        Asks the user if they want to return to the menu.
        """
        choice = input("Voulez-vous revenir au menu ? (o/n) ? ")
        return choice == "o"

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
