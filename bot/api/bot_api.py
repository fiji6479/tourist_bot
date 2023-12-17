import time

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
        self.timestamp = time.time()
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


def get_places_to_send(chat_id: int, id_to_place_dict: dict, session: UserSession):
    messages = []

    points = session.get5points()
    for key in points:
        rs = id_to_place_dict.get(key.id)
        print(rs)
        place_name = str(rs[1]) if rs[1] else 'достопримечательность'
        art_type = str(rs[2]) if rs[2] else 'неизвестно'
        web_site = str(rs[3]) if rs[3] else 'неизвестно'


        print(place_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        messages.append(BotMessage(
            chat_id=chat_id,
            text=f'Название: {place_name}\n Категория: {art_type}\n Веб-сайт:{web_site}\n Яндекс-карта:'+ f'[{place_name}](https://yandex.ru/maps/2/saint-petersburg/?text={rs[4][0]}%2C{rs[4][1]})',
            reply_markup=markup, parse_mode='Markdown'))
    return messages




def set_all_places_for_distance(points: Points, session: UserSession):
    print(f"distance is {session.distance}")
    closest_points = points.get_closest(lat=session.lat,
                                        lon=session.lon,
                                        radius=session.distance)
    session.add_points(closest_points)

    # for key in points:
    #     rs = id_to_place_dict.get(key.id)
    #     place_name = str(rs[1])
    #
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     messages.append(BotMessage(
    #         chat_id=chat_id,
    #         text=f'{place_name}\n https://yandex.ru/maps/2/saint-petersburg/?text={rs[4][0]}%2C{rs[4][1]}',
    #         reply_markup=markup))

    # return messages
