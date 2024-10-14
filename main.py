"""Основной файл бота.
Здесь находятся все хэндлеры для обработки сообщений"""

from telebot import TeleBot
from telebot import types, util

import config
from database import DatabaseSQ
from database import make_file_with_all_participants

import messages
import my_filters

from commands import default_commands

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(my_filters.IsUserAdminOfBot())

db = DatabaseSQ('database.db')
db.create_table()

def has_no_command_arguments(message: types.Message):
    return not util.extract_arguments(message.text)

@bot.message_handler(commands=['start'])
def handler_start_command(message: types.Message):
    if not db.get_user(message.chat.id):
        db.add_user(message.chat.id)

    bot.send_message(
        message.chat.id,
        messages.message_start.format(username=message.from_user.username),
        parse_mode='HTML'
    )

@bot.message_handler(commands=['help'])
def handler_help_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.message_help,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['about'])
def handler_about_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.make_message_about(db, message),
        parse_mode='HTML'
    )

@bot.message_handler(commands=['participate'], func=has_no_command_arguments)
def handler_participate_command_with_not_args(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.message_participate_with_no_args,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['participate'])
def handler_participate_command(message: types.Message):
    args = util.extract_arguments(message.text)
    try:
        funpay_id = int(args)
    except Exception as ex:
        bot.send_message(
            message.chat.id,
            messages.message_bad_funpay_id,
            parse_mode='HTML'
        )
        return

    if db.add_funpay_id(message.chat.id, funpay_id):
        bot.send_message(
            message.chat.id,
            messages.message_add_funpay_id.format(funpay_id=funpay_id),
            parse_mode = 'HTML'
        )
    else:
        bot.send_message(
            message.chat.id,
            messages.message_not_add_funpay_id.format(funpay_id=funpay_id),
            parse_mode='HTML'
        )

@bot.message_handler(commands=['list_participants'], is_bot_admin=False)
def handle_list_participants_is_not_admin(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.message_not_admin,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['list_participants'], is_bot_admin=True)
def handle_list_participants(message: types.Message):
    output_file = make_file_with_all_participants(db.get_all_info())
    bot.send_document(
        chat_id=message.chat.id,
        document=output_file,
        visible_file_name="list_participants.txt",
        caption=messages.user_info_doc_caption,
    )

@bot.message_handler(commands=['choose_winners'], is_bot_admin=False)
def handle_choose_winners_is_not_admin(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.message_not_admin,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['choose_winners'], func=has_no_command_arguments)
def handle_choose_winners_not_args(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.message_choose_winner_not_args,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['choose_winners'], is_bot_admin=True)
def handle_choose_winners(message: types.Message):
    args = util.extract_arguments(message.text)
    try:
        count = int(args)
    except Exception as ex:
        bot.send_message(
            message.chat.id,
            messages.message_bad_count_winners,
            parse_mode='HTML'
        )
        return

    all_participants = db.get_all_info()
    winners = messages.make_message_choose_winner(all_participants, count)
    if winners is False:
        bot.send_message(
            message.chat.id,
            messages.message_count_more_than_len,
            parse_mode='HTML'
        )
        return

    bot.send_message(
        message.chat.id,
        winners,
        parse_mode='HTML'
    )

if __name__ == "__main__":
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True)