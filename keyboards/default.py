'''
SIZ BU YERDA ODDIY KNOPKALAR YARATA OLASIZ
'''

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    catalog = KeyboardButton("Katalog 📇")
    feedback = KeyboardButton("Bog'lanish ☎")
    settings = KeyboardButton("Sozlamalar 🛠")
    markup.add(catalog, feedback, settings)
    return markup

def register_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Ro'yxatdan o'tish")
    markup.add(btn)
    return markup

def send_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    contact = KeyboardButton("Kontaktni ulashish", request_contact=True)
    markup.add(contact)
    return markup