import os
from telegram import ParseMode
from utils.user_data import save_user_data
from utils.car_info import get_car_list, find_car_in_list, get_car_details
from utils.constants import CAR_TYPE_MAPPING, COMPANY_MAPPING

# Получение переменных окружения
ADMIN_ID = int(os.getenv("ADMIN_ID"))
RESTRICTED_CAR_NUMBER = int(os.getenv("RESTRICTED_CAR_NUMBER"))

def start(update, context):
    update.message.reply_text("Hello! Enter the car number to get information.")

def format_car_information(car_info, details, hidden_value, company_name, car_type):
    formatted_details = details.replace("-Cell#:", "\n📞 *Phone:*").replace(" -", "\n• ")
    message = (
        "📋 *General Information:*\n"
        f"• *Car Number:* {car_info['CarNo']}\n"
        f"• *Company:* {company_name}\n"
        f"• *Car Type:* {car_type}\n"
        f"• *In Shift:* {'Yes' if car_info['InShift'] == '1' else 'No'}\n"
        f"• *Shift Day:* {car_info['shiftday'] if car_info['shiftday'] else 'No data'}\n\n"
        "📄 *Detailed Information:*\n"
        f"{formatted_details}\n\n"
        f"📍 *Destination:* {hidden_value}"
    )
    return message

def handle_message(update, context):
    try:
        car_number = update.message.text.strip()
        user_id = update.message.from_user.id
        username = update.message.from_user.username

        # Проверка на корректность ввода
        if not car_number.isdigit():
            update.message.reply_text("Please enter the car number as a number.")
            return

        car_number = int(car_number)

        # Получение списка машин
        root = get_car_list()  # API-запрос или загрузка данных
        if root:
            car_info = find_car_in_list(root, car_number)
            if car_info:
                details, image_url, hidden_value = get_car_details(car_info["CarNo"], car_info["Comp"])
                if details:
                    # Форматируем сообщение
                    company_name = COMPANY_MAPPING.get(car_info["Comp"], "Unknown company")
                    car_type = CAR_TYPE_MAPPING.get(car_info["CarType"], "Unknown type")
                    message = format_car_information(car_info, details, hidden_value, company_name, car_type)

                    # Отправляем сообщение пользователю
                    update.message.reply_text(message, parse_mode='Markdown')

                    # Отправляем фото, если доступно
                    if image_url:
                        context.bot.send_photo(chat_id=update.message.chat_id, photo=image_url, caption="Driver photo")
                else:
                    update.message.reply_text("Failed to retrieve detailed information.")
            else:
                update.message.reply_text(f"Car number {car_number} not found.")
        else:
            update.message.reply_text("Failed to retrieve car list data.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

def broadcast_message(update, context):
    from utils.user_data import load_user_data
    import time

    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("You do not have permission to use this command.")
        return

    message_text = " ".join(context.args)
    if not message_text:
        update.message.reply_text("Please provide a message to broadcast.")
        return

    users = load_user_data()
    if not users:
        update.message.reply_text("No user data found.")
        return

    failed_users = []
    for user in users:
        try:
            context.bot.send_message(chat_id=user["user_id"], text=message_text)
            time.sleep(1)  # Avoid rate limiting
        except Exception:
            failed_users.append(user["user_id"])

    update.message.reply_text(f"Broadcast completed. Failed: {len(failed_users)}")

from utils.user_data import get_detailed_statistics
from utils.constants import ADMIN_ID

def send_detailed_stats_to_admin(update, context):
    # Только для администратора
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("You do not have permission to use this command.")
        return

    # Получаем полную статистику
    detailed_stats = get_detailed_statistics()

    if not detailed_stats:
        update.message.reply_text("No user data available.")
        return

    # Формируем подробное сообщение
    stats_message = "📊 Detailed User Statistics:\n"

    for user_id, stats in detailed_stats.items():
        stats_message += (
            f"👤 User: @{stats['username']} (ID: {user_id})\n"
            f"   - Total Requests: {stats['total_requests']}\n"
            f"   - Requests:\n"
        )
        for req in stats["requests"]:
            stats_message += (
                f"      • Car Number: {req['car_number']} "
                f"(Timestamp: {req['timestamp']})\n"
            )
        stats_message += "\n"

    # Отправляем статистику администратору
    context.bot.send_message(chat_id=ADMIN_ID, text=stats_message)
