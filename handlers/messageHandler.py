import discord
from datetime import datetime
from time import mktime

from handlers.TimerCache import TimerCache

def processMessage(msg):
    if criteriaFilter(msg):
        TimerCache.updateCache(id)

def criteriaFilter(message: discord.Message) -> bool:
    ## Message must be at least 2 characters
    if len(message.content) < 2:
        return False

    ## Message will only count if previous message was 3 seconds ago
    now = mktime(datetime.now().timetuple())

    record = TimerCache.getUser(message.author.id)
    print(record)
    if (record[2] + 3) < now:
        return False

    return True