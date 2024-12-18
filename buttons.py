
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def phone_number_bt():
    # создание пространства для кнопок
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # создание самой кнопки
    button = KeyboardButton(text="Поделиться контактами",
                            request_contact=True)
    # добавляем кнопки в пространство
    kb.add(button)
    return kb
def location_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text="Поделиться локацией",
                            request_location=True)
    kb.add(button)
    return kb
