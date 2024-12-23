
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


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
def main_menu_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text="🍴Меню")
    button2 = KeyboardButton(text="✍️Отзыв")
    button3 = KeyboardButton(text="🛒Корзина")
    kb.row(button1)
    kb.row(button2, button3)
    return kb
def product_in(all_products):
    kb = InlineKeyboardMarkup(row_width=2)
    # статичные кнопки
    back = InlineKeyboardButton(text="Назад", callback_data="back")
    cart = InlineKeyboardButton(text="Корзина", callback_data="cart")
    # динамичные кнопки
    buttons = [InlineKeyboardButton(text=f"{product[1]}", callback_data=f"prod_{product[0]}")
               for product in all_products]
    kb.add(*buttons)
    kb.row(cart)
    kb.row(back)
    return kb



