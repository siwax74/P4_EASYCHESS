import json


def set_player_to_json(data, file_path):
    try:
        existing_data = load_from_json(file_path)
        player_key = f"player{len(existing_data) + 1}"
        existing_data[player_key] = data
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data to {file_path}: {e}")


def load_from_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


def set_tournament_to_json(data, file_path):
    try:
        existing_data = load_from_json(file_path)
        tournament_key = f"tournament{len(existing_data) + 1}"
        existing_data[tournament_key] = data
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data to {file_path}: {e}")
