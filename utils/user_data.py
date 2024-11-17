import json
import os
from datetime import datetime

USER_DATA_FILE = "users.json"

# Функция для сохранения данных пользователя
def save_user_data(user_id, username, car_number):
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}

    # Если пользователя еще нет в базе, создаем запись
    if str(user_id) not in data:
        data[str(user_id)] = {
            "username": username,
            "requests": []
        }

    # Добавляем запрос пользователя
    data[str(user_id)]["requests"].append({
        "car_number": car_number,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # Сохраняем обновленные данные
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Функция для загрузки всех данных
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Функция для получения полной статистики
def get_detailed_statistics():
    data = load_user_data()
    stats = {}

    for user_id, user_info in data.items():
        stats[user_id] = {
            "username": user_info["username"],
            "total_requests": len(user_info["requests"]),
            "requests": user_info["requests"]
        }

    return stats
