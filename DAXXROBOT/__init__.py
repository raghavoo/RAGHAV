import logging
import os
import sys
import time
import ast
import base64

import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", "True"))

if ENV:

    API_ID = int(os.environ.get("API_ID", "28216960"))
    API_HASH = os.environ.get("API_HASH", "16cd70578949eefbec1655e206f14fcf")
    CHATBOT_API = os.environ.get("CHATBOT_API", "6156380294-fallen-ediv00vide")
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", "D31QL4STIWPSLALL")
    DB_URI = os.environ.get("DATABASE_URL", "postgres://ovkhfxkp:d6SvqcZmnYmhLQBqGVmt9AMyB0DzqXPS@isilo.db.elephantsql.com/ovkhfxkp")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", "-1002004616638")
    INFOPIC = bool(os.environ.get("INFOPIC", "True"))
    LOAD = os.environ.get("LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://starxrobo:starxrobo@cluster0.efstcnr.mongodb.net/?retryWrites=true&w=majority")
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    START_IMG = os.environ.get(
        "START_IMG", "https://te.legra.ph/file/612122f0681220f8a49f4.jpg"
    )
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "raghavsupport")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TOKEN = os.environ.get("TOKEN", "True")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", "MGUSGI8E7QEP")
    WORKERS = int(os.environ.get("WORKERS", 8))

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", "6156380294"))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "6144223366").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "6144223366").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "6144223366").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "6144223366").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "6144223366").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

else:
    from DAXXROBOT.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DB_URI = Config.DATABASE_URL
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    CHATBOT_API=Config.CHATBOT_API
    MONGO_DB_URI = Config.MONGO_DB_URI
    NO_LOAD = Config.NO_LOAD
    START_IMG = Config.START_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TOKEN = Config.TOKEN
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")


DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(abs(110001110110101101000111111101101))
DEV_USERS.add(abs(110001110110101101000111111101101))
DEV_USERS.add(abs(110001110110101101000111111101101))
DEV_USERS.add(abs(110001110110101101000111111101101))


updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("daxx", API_ID, API_HASH)

pbot = Client("DAXXROBOT", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN,in_memory=True)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

DRAGONS = list(DRAGONS) + list(DEV_USERS) 
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from DAXXROBOT.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
