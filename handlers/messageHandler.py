import discord
from datetime import datetime
from time import mktime
from handlers.UserCache import UserCache

cache = UserCache()

class messageHandler:
    def __init__(self):
        self.msgLenThreshold = 2
        self.timerThreshold = 3

    def processMessage(self, msg):
        if self.criteriaFilter(msg):
            print(cache.getUser(msg.author.id))
            cache.setUser(msg.author.id)

    def criteriaFilter(self, msg: discord.Message) -> bool:
        ## Message must be at least 2 characters
        if len(msg.content) < self.msgLenThreshold:
            return False

        ## Message will only count if previous message was 3 seconds ago
        now = mktime(datetime.now().timetuple())
        record = cache.getUser(msg.author.id)
        if record:
            if (record[2] + self.timerThreshold) > now:
                return False

        return True