'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import register_button, send_contact
from keyboards.inline import get_categories_buttons

@bot.message_handler(func=lambda message: message.text == "Katalog 📇")
def catalog(message: Message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    from_user_id = message.from_user.id
    check = db.check_user_info(from_user_id)
    if None in check:
        text = "Siz ro'yxatdan o'tmagansiz. Iltimos ro'yxatdan o'ting!"
        markup = register_button()
    else:
        bot.send_message(chat_id, "Katalogni tanlang:", reply_markup=ReplyKeyboardRemove())
        text = "Katalog"
        category_list = db.select_all_categories()
        markup = get_categories_buttons(category_list)
    bot.send_message(chat_id, text, reply_markup=markup)
    # bot.send_message(chat_id, text, reply_markup=markup)

data = {}

@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish")
def register(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    msg = bot.send_message(chat_id, "Ism va familiyangizni kiriting: ", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, name_save)

def name_save(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    full_name = message.text

    data[from_user_id] = {'full_name': full_name}

    msg = bot.send_message(chat_id, "Telefon nomeringizni kiriting: ", reply_markup=send_contact())
    bot.register_next_step_handler(msg, save_contact)

def save_contact(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    contact = message.contact.phone_number

    data[from_user_id]['contact'] = contact

    msg = bot.send_message(chat_id, "Tug'ilgan sanangizni dd.mm.yyyy ko'rinishida kiriting: ", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, user_save)

def user_save(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    birth_data = message.text

    data[from_user_id]['birth_date'] = birth_data
    full_name = data[from_user_id]['full_name']
    contact = data[from_user_id]['contact']

    db.save_user_info(full_name, contact, birth_data, from_user_id)

    categories = db.select_all_categories()
    bot.send_message(chat_id, "Katalog", reply_markup=get_categories_buttons(categories))
