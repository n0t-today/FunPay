"""Все сообщения, которые отправляет бот"""

from telebot import formatting
import random

message_start = formatting.format_text(
    "Привет <b>{username}</b>!",
    "Чтобы зарегистрироваться используй команду <code>/participate ТВОЙ_FUNPAY_ID</code>",
    "Узнать информацию о себе можешь по команде <code>/about</code>",
    "Если понадобится помощь пиши <code>/help</code>",
    "Удачи!"
)

message_help = formatting.format_text(
    "<code>/participate ТВОЙ_FUNPAY_ID</code> - зарегистрироваться в розыгрыше",
    "<code>/about</code> - узнать информацию о себе",
    "<code>/help</code> - помощь",
)

message_about = formatting.format_text(
    "Никнейм: <b>{username}</b>",
    "Телеграмм ID: <b>{telegram_id}</b>",
    "FUNPAY ID: <b>{funpay_id}</b>",
)

def make_message_about(db, message):
    info = db.get_info(message.chat.id)
    result_message = message_about.format(
        username=message.from_user.username,
        telegram_id=info[0][0],
        funpay_id=info[0][1] if info[0][1] is not None else '-'
    )
    return result_message

message_participate_with_no_args = formatting.format_text(
    "Необходимо указать свой FUNPAY ID для регистрации на розыгрыш, например:",
    "<code>/participate 123456789</code>"
)

message_bad_funpay_id = formatting.format_text(
    "Неправильно указан FUNPAY ID!",
    message_participate_with_no_args
)

message_add_funpay_id = formatting.format_text(
    "Твой FUNPAY ID - {funpay_id} добавлен.",
    "Ты успешно зарегистрировался!",
    'Удачи!'
)

message_not_add_funpay_id = formatting.format_text(
    "Твой FUNPAY ID - {funpay_id} уже был зарегистрирован!",
)

message_not_admin = 'Упс... Тебе нельзя пользоваться это командой!'

user_info_doc_caption = 'Все участники'

message_bad_count_winners = 'Введите корректное число!'

message_choose_winner_not_args = formatting.format_text(
    'Необходимо указать количество победителей, например',
    '<code>/choose_winners 2</code>'
)
message_count_more_than_len = 'Количество выбранных победителей больше, чем количество участников!'

message_choose_winner = '<b>Телеграмм ID</b> | FUNPAY ID'
def make_message_choose_winner(all_participants, count):
    if count > len(all_participants):
        return False
    winners = random.sample(all_participants, count)
    result = message_choose_winner + '\n'
    result += '\n'.join(f'<b>{winner[0]}</b> | {winner[1]}' for winner in winners)
    return result