import sys
from easychess.controllers.main_controller import run

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("Arrêt du script...")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur : {e}")
