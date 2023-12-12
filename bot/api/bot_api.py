from telebot import types
from geo.geo import Points

geo_laction = {}


class BotMessage:

    def __init__(self, chat_id, text, reply_markup, parse_mode=None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup
        self.parse_mode = parse_mode


class UserSession:

    def __init__(self, lat, lon, distance):
        self.lat = lat
        self.lon = lon
        self.distance = distance
        self.points = []

    def add_points(self, points: list):
        self.points = points

    def get5points(self):
        res = self.points[:5]
        del self.points[0:6]
        return res



def send_hello(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отправить своё местоположение", request_location=True)
    markup.add(btn1)

    return BotMessage(chat_id=chat_id,
                      text="Привет, я телеграм бот, который поможет тебе рассмотреть все достопримечательности города Санкт-Петербург. Нажмите кнопку, чтобы отправить своё местоположение",
                      reply_markup=markup)



def get_request_distance_message(chat_id):
    keyboard = [
        [
            types.InlineKeyboardButton("50", callback_data="50"),
            types.InlineKeyboardButton("100", callback_data="100"),
        ],
        [
            types.InlineKeyboardButton("250", callback_data="250"),
            types.InlineKeyboardButton("500", callback_data="500")
        ]

    ]

    reply_markup = types.InlineKeyboardMarkup(keyboard)

    return BotMessage(chat_id, 'Выбери радиус поиска', reply_markup=reply_markup)


def get_next_place_button(chat_id: int):
    keyboard = [types.InlineKeyboardButton("Next", callback_data="Next")]
    reply_markup = types.InlineKeyboardMarkup([keyboard])

    return BotMessage(chat_id, 'Продолжить?', reply_markup=reply_markup)


def get_places_to_send(chat_id: int, points: Points, id_to_place_dict: dict, session: UserSession):
    messages = []

    points = session.get5points()
    for key in points:
        rs = id_to_place_dict.get(key.id)

        place_name = str(rs[1])
        print(place_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        messages.append(BotMessage(
            chat_id=chat_id,
            text=f'{place_name}\n https://yandex.ru/maps/2/saint-petersburg/?text={rs[4][0]}%2C{rs[4][1]}',
            reply_markup=markup))
    return messages




def send_places(chat_id: int, points: Points, id_to_place_dict: dict, session: UserSession):
    print(f"distance is {session.distance}")
    messages = []
    closest_points = points.get_closest(lat=session.lat,
                                        lon=session.lon,
                                        radius=session.distance)
    session.add_points(closest_points)
    points = session.get5points()
    for key in points:
        rs = id_to_place_dict.get(key.id)
        place_name = str(rs[1])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        messages.append(BotMessage(
            chat_id=chat_id,
            text=f'{place_name}\n https://yandex.ru/maps/2/saint-petersburg/?text={rs[4][0]}%2C{rs[4][1]}',
            reply_markup=markup))

    return messages
