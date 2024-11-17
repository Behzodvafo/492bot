import json
import os

USER_DATA_FILE = "users.json"

def save_user_data(user_id, username, car_number):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append({"user_id": user_id, "username": username, "car_number": car_number})

    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return []
