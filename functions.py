import json
import random
from datetime import datetime, timedelta

USER_DATA_FILE = 'user_data.json'


def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file, default=str)


def load_user_data():
    try:
        with open(USER_DATA_FILE, 'r') as file:
            data = json.load(file)
            for user_name, user_info in data.items():
                user_info['last_command_time'] = datetime.fromisoformat(user_info['last_command_time'])
            return data
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        return {}


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), int(seconds)


# --------------------------------------------------------------------------------

def remove_inactive_users(user_data):
    current_time = datetime.now()
    inactive_users = []

    for user_name, data in user_data.items():
        last_command_time = data['last_command_time']
        if (current_time - last_command_time).total_seconds() >= 14 * 24 * 60 * 60:
            inactive_users.append(user_name)

    for user_name in inactive_users:
        del user_data[user_name]


# --------------------------------------------------------------------------------

class ChatHistory:
    def __init__(self):
        self.history = []


chat_history = ChatHistory()

# --------------------------------------------------------------------------------

# Пасхалки
penis_paschal = {
    0: "плохие новости, у тебя вагина",
    1: "лупу подать?0)0)0)0((",
    3: "Полное погружение",
    12: "че за год усох уже на 1см? 13 же был.",
    13: "поздравляю, у вас хуй китайца",
    15: "15 сантиметров, 15 сантиметров Пися плюс минус 15 сантиметров 15 сантиметров, 15 сантиметров 15 сантиметров откровенно — п**дец",
    20: "И что, люблю большой член. И что, сосу каждый день",
    25: "[ТВИЧ НЕ ОДОБРЯЕТ]",
    33: "А вы верите в Бога?",
    37: "Дмитрий Ликс бы позавидовал",
    42: "узнайте ответ на любой вопрос жизни",
    50: "У ТЕБЯ ПЕНИС СТАЛИНА 50 СМ",
    51: "54 см. Мировой рекорд. У тебя длиннее хуя Сталина",
    52: "69 см. С таким размером в такую позу не свернёшься",
    53: "70 см. У вас хуй Вовочки",
    54: "Error 488. Твич не одобряет",
    55: "228 см. Все вопросы к стримеру"
}

iq_paschal = {
    -1: "Есть пробитие",
    0: "медузаааа, медуза, медуза, мы друзьяяяя...",
    1: "у тебя iq пчёлки. Жу-жу",
    20: "Вы самый умный слоник",
    26: "Температура воды, в которой я обитаю, выше, чем твой IQ",
    30: "У тебя iq ниже твоего размера обуви",
    47: "[ТВИЧ НЕ ОДОБРЯЕТ]",
    50: "Тебе с такими шутками только в смехлыст",
    69: "Ха-ха, пися)0)0())0)",
    89: "Братишкина одобряем",
    110: "Ты уже получше тапочка",
    162: "У ТЕБЯ IQ ЭЙНШТЕЙНА",
    200: "Приятно осознавать, что люди с IQ за двести тоже не боги",
    228: "ВЫ САМЫЙ УМНЫЙ НА ПЛАНЕТЕ",
    256: "Дай",
    300: "Отсоси у тракториста"
}

boobs_paschal = {
    0: "плохие новости, ты доска",
    1: "-главное, чтобы помещались в ладошку...)- Но не обе сразу...",
    5: "Найс бубс)0)))0)0)"
}


def get_paschal_message(paschal_list, value):
    if value in paschal_list:
        return paschal_list[value]
    return ""


# --------------------------------------------------------------------------------

class PasswordGame:
    def __init__(self):
        self.password = self.generate_password()
        self.correct_guesses = set()

    def generate_password(self):
        file_path = 'wordlistPassword.txt'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
        except FileNotFoundError:
            print(f"Файл {file_path} не знайдено.")
            words = []

        return random.choice(words) if words else "Файл порожній або не існує."

    def display_partial_password(self):
        partial_password = ''
        revealed_position = None

        for i, char in enumerate(self.password):
            if i in self.correct_guesses:
                partial_password += char
            else:
                partial_password += '_'

                if revealed_position is None and i not in self.correct_guesses:
                    revealed_position = i

        return partial_password


# --------------------------------------------------------------------------------

voices = [
    '!св', '!св2', '!сх3', '!хрон', '!кварт', '!дьявол',
    '!монстр', '!футко2', '!тролесо', '!скоросорт',
    '!колесо', '!голова', '!шпион', '!roulette', '!roulette да'
]
# --------------------------------------------------------------------------------
