import logging
import os
import sys
import time

import deethon
from dotenv import load_dotenv
from telethon import TelegramClient, events, functions, types

formatter = logging.Formatter('%(levelname)s %(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler(f'{__name__}.log', 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.WARNING)
telethon_logger.addHandler(ch)
telethon_logger.addHandler(fh)

botStartTime = time.time()

load_dotenv()

try:
    API_ID = int("7684605")
    API_HASH = "d270d70e8d3c3ad969ea6ecb5857e30b"
    BOT_TOKEN = "5610672568:AAGmdzaJ7QDC3tnR0aeZNoTrDj9U8KH58BQ"
    DEEZER_TOKEN = "a5a43398fa06b55f9eb8b072b71628df2739652f168b321f969f213d4b5704dc531fa1ef492f74026121e6fd99b2ce298bbb82caea3f2326c6b749b59f1761962df05f635e91cb2b02090bcf30eff9e0a61a4efa6cc66ac5d35f09a1c384e5d4"
    OWNER_ID = int("5004180573")
except KeyError:
    logger.error("One or more environment variables are missing! Exiting now…")
    sys.exit(1)

deezer = deethon.Session(DEEZER_TOKEN)
logger.debug(f'Using deethon v{deethon.__version__}')

bot = TelegramClient(__name__, API_ID, API_HASH, base_logger=telethon_logger).start(bot_token=BOT_TOKEN)
logger.info("Bot started")

# Saving user preferences locally
users = {}

bot.loop.run_until_complete(
    bot(functions.bots.SetBotCommandsRequest(
        commands=[
            types.BotCommand(
                command='start',
                description='Get the welcome message'),
            types.BotCommand(
                command='help',
                description='How to use the bot'),
            types.BotCommand(
                command='settings',
                description='Change your preferences'),
            types.BotCommand(
                command='info',
                description='Get some useful information about the bot'),
            types.BotCommand(
                command='stats',
                description='Get some statistics about the bot'),
        ]
    ))
)

@bot.on(events.NewMessage())
async def init_user(event):
    if event.from_id not in users.keys():
        users[event.from_id] = {
            "quality": "FLAC"
        }
