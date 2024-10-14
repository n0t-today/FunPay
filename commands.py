"""Создание команд для меню бота"""

from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "начало работы"),
    BotCommand("help", "помощь"),
    BotCommand("participate", "зарегистрироваться"),
    BotCommand("about", "информация о себе"),
]