import json


def set_tournament_to_json(data, file_path):
    try:
        existing_data = load_from_json(file_path)
        tournament_key = f"{len(existing_data) + 1}"
        existing_data[tournament_key] = data
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data to {file_path}: {e}")
