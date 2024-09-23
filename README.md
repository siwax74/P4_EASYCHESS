
# ♟️ **Application de Gestion de Tournois d'Échecs** ♟️

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flake8](https://img.shields.io/badge/Flake8-PEP8--Compliant-green)
![Status](https://img.shields.io/badge/Status-Offline%20App-brightgreen)

Bienvenue dans l'application de gestion de tournois d'échecs. Cette application hors ligne, développée en Python, vous permet de créer, gérer et suivre des tournois d'échecs avec une base de données JSON. Elle suit le modèle de conception **MVC** pour une meilleure maintenabilité et est compatible avec **Windows**, **Mac**, et **Linux**.

## 📋 **Fonctionnalités**

- **Gestion des Joueurs** :
  - Ajout manuel des joueurs (Nom, Prénom, Date de naissance, ID National d'Échecs).
- **Tournois** :
  - Création, gestion et suivi des tournois, tours et matchs.
  - Calcul automatique des scores.
- **Rapports** :
  - Liste des joueurs par ordre alphabétique.
  - Liste des tournois.
  - Détails complets des tournois : rounds, matchs, scores.
- **Sauvegarde/Chargement** : 
  - Sauvegarde automatique en **JSON** après chaque action.
  - Rechargement des données à partir de fichiers JSON pour reprise instantanée.

## 🛠 **Prérequis**

- **Python 3.8+** doit être installé sur votre machine.
- Créez et activez un environnement virtuel pour isoler vos dépendances :
   ```
  python -m venv env
  source env/bin/activate # Sur Mac/Linux
  env\Scripts\activate    # Sur Windows
   ```
## 🚀 **Lancement de l'application**

1. Lancez l'application depuis la console :
   ```
   python main.py
   ```

2. Vous serez accueilli par le menu principal, où vous pourrez :
   - Ajouter un joueur.
   - Créer/démarrer un tournoi.
   - Générer et afficher les rapports.

## 🧩 **Modèle de Conception : MVC**

L'application est structurée selon le modèle **Modèle-Vue-Contrôleur** :
- **Modèles** : Gèrent les données et la logique métier (Tournois, Joueurs, Rounds, Matchs).
- **Vues** : Gèrent l'affichage des rapports et des informations à l'utilisateur.
- **Contrôleurs** : Gèrent les interactions entre les modèles et les vues.

## 📝 **Données et Sauvegarde**

- **Joueurs** et **Tournois** sont sauvegardés dans des fichiers JSON situés dans le dossier `/easychess/datas` :
  - `/easychess/datas/data_players.json` : Contient les informations des joueurs.
  - `/easychess/datas/data_tournaments.json` : Contient les informations des tournois.
  
- La synchronisation entre les objets en mémoire et les fichiers JSON est automatique après chaque modification.

## 📊 **Rapports Disponibles**

Vous pouvez afficher les rapports suivants directement dans la console ou via des templates HTML :
- **Liste des joueurs** (ordre alphabétique).
- **Liste des tournois**.
- **Détails d'un tournoi** : Nom, date, nombre de tours..
- **Rounds et Matchs** : Détails des matchs pour chaque round.

## 🔍 **Exécution des Tests et Conformité PEP8**

Pour assurer la qualité du code et le respect des normes PEP8, utilisez **flake8** avec le rapport HTML pour vérifier votre code :

1. Installez Flake8 et Flake8 HTML :
   ```
   pip install flake8 flake8-html
   ```

2. Exécutez Flake8 pour analyser le code :
   ```
   cd votre repo
   
   ```
   ```
   flake8 --format=html --htmldir=rapport_flake8

   ```
   ```
   start index.html

   ```
3. Consultez le rapport généré dans le répertoire `flake8_rapport`.

## 🛠 **Maintenance et Améliorations Futures**

Voici quelques améliorations prévues pour les versions futures :
- Intégration d'une base de données relationnelle (SQLite, PostgreSQL).
- Exportation des rapports au format PDF ou CSV.
- Interface utilisateur graphique (GUI).
  
## 📄 **Licences**

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](./LICENSE) pour plus d'informations.

## 👨‍💻 **Auteur**

Développé par [DGEY].

N'hésitez pas à contribuer en ouvrant une issue ou en soumettant une pull request !