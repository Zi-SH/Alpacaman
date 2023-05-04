from datetime import datetime
from time import mktime
from discord.ext import tasks
from handlers.UserDB import UserDB

######
## Timer Cache consists of a User Dict, using user ID (int) as the key and holding
## an array with a message count at [0] and a timestamp at [1]
######

class TimerCache:
    def __init__(self):
        self.users = {}
        self.database = UserDB()

    def updateCache(self, id: int) -> None:
        now = self.currentTime()

        if id in self.users:
            # Grab message count, update count and timestamp
            msgCount = self.users[id][0]
            self.users[id] = [msgCount+1, now]

        if id not in self.users:
            self.users[id] = [0, now]

    @tasks.loop(minutes=60.0)
    async def cleanCache(self):
        now = self.currentTime()

        for user in self.users:
            # If the user hasn't posted in an hour, remove them
            if (self.users[user][1] + 3600) < now:
                self.users.pop(user, None)

    @cleanCache.before_loop
    async def writeCache(self) -> None:
        self.database.writeCache(self.users)

    def readCache(self) -> None:
        self.users = self.database.readCache()

    def getUser(self, id) -> list:
        try:
            user = self.users[id]
            return [id, user[0], user[1]]
        except KeyError:
            return []

    def currentTime(self) -> float:
        # Dealing in Epoch time for simplicity
        now = datetime.now()
        return mktime(now.timetuple())