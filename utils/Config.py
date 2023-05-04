import json
import discord

class Config:
    def __init__(self):
        with open("config.json", "r") as f:
            bot = json.load(f)
        self.prefix = bot['prefix']
        self.desc   = bot['desc']
        self.token  = bot['token']

        # Pain in my ass to be quite honest
        self.intents = discord.Intents.default()

        self.intents.guild_messages = True
        self.intents.members = True
        self.intents.messages = True
        self.intents.message_content = True