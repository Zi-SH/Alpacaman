import asyncio
from datetime import datetime
from time import mktime

import discord.ext.commands
from discord.ext import tasks
from handlers import userDB

######
## Timer Cache consists of a User Dict, using user ID (int) as the key and holding
## an array with a message count at [0] and a timestamp at [1]
######

class UserCache:
    def __init__(self):
        self.users = self.loadCache()

    def loadCache(self):
        return userDB.loadCache()

    def dumpCache(self):
        userDB.writeCache(self.users)

    def getUser(self, id: int) -> list:
        try:
            user = self.users[id]
            return [id, user[0], user[1]]
        except KeyError:
            return []

    def setUser(self, id: int) -> None:
        now = self.currentTime()

        if id in self.users:
            # Grab message count, update count and timestamp
            msgCount = self.users[id][0]
            self.users[id] = [msgCount+1, now]

        if id not in self.users:
            self.users[id] = [0, now]

    # TODO: Data verification on user update, pulling from DB first
    # def purgeCache(self):
    #     now = self.currentTime()
    #
    #     for user in self.users:
    #         # If the user hasn't posted in an hour, remove them
    #         if (self.users[user][1] + 3600) < now:
    #             self.users.pop(user, None)

    def currentTime(self) -> float:
        # Dealing in Epoch time for simplicity
        now = datetime.now()
        return mktime(now.timetuple())