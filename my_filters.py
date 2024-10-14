"""Кастомные фильтры"""

from telebot.types import Message
from telebot.custom_filters import SimpleCustomFilter

import config

class IsUserAdminOfBot(SimpleCustomFilter):
    key = "is_bot_admin"

    def check(self, message: Message):
        return message.from_user.id in config.BOT_ADMIN_USER_IDS