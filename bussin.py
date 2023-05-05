import asyncio
import json, sys, logging
from handlers.messageHandler import messageHandler
from utils.Config import Config
from handlers import userCacheTimer
from discord.ext import commands

setting = Config()

# Init bot
client = commands.Bot(command_prefix=setting.prefix, description=setting.desc, case_insensitive=True, intents=setting.intents)

# Init Message Handler
messageHandler = messageHandler()

# Enable logging
log = logging.getLogger()
con = logging.StreamHandler()

log.addHandler(con)
log.setLevel(logging.WARN)


@client.event
async def setup_hook():
    # Init Timers
    timerLoop = asyncio.get_event_loop()
    timerLoop.create_task(userCacheTimer.cacheWriteTask())
    timerLoop.create_task(userCacheTimer.monthlyThreshold())

    # Load roleHandler

@client.event
async def on_ready():
    print(client.user.name + "( " + str(client.user.id) + ")" + " connected successfully.")
    print('------')

@client.event
async def on_message(msg):
    messageHandler.processMessage(msg)

client.run(setting.token)