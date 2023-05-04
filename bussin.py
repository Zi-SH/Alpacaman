import json, sys, logging
import discord
from handlers import messageHandler

from utils.Config import Config
from handlers.TimerCache import TimerCache
from discord.ext import commands

setting = Config()

# Init bot
client = commands.Bot(command_prefix=setting.prefix, description=setting.desc, case_insensitive=True, intents=setting.intents)

# Init Cache
cache = TimerCache()

# Enable logging
log = logging.getLogger()
con = logging.StreamHandler()

log.addHandler(con)
log.setLevel(logging.WARN)

@client.event
async def on_ready():
    print(client.user.name + "( " + str(client.user.id) + ")" + " connected successfully.")
    print('------')

@client.event
async def on_message(msg):
    messageHandler.processMessage(msg)

    print(msg.author)
    print(msg.author.id)

client.run(setting.token)