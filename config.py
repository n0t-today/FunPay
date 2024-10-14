"""Расшифровка конфига.
Файл конфига config.ini
Токен бота записывается без кавычек в соответствующий параметр
ID админов записываются без кавычек через запятую в соответствующий параметр"""

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

BOT_TOKEN = config.get("bot", "token")

def get_admin_ids():
    admin_ids = config.get("admin", "admin_ids", fallback="")
    admin_ids = [admin_id.strip() for admin_id in admin_ids.split(",")]
    admin_ids = [
        int(admin_id)
        for admin_id in admin_ids
        if admin_id
    ]
    return admin_ids


BOT_ADMIN_USER_IDS = get_admin_ids()

print(BOT_ADMIN_USER_IDS)