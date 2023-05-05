import asyncio
from datetime import datetime
from handlers import userDB
from utils.Config import Config
from handlers.messageHandler import cache

config = Config()

# TODO: See TODO in UserCache regarding the purgeCache
# async def purgeCacheTask():
#     await asyncio.sleep(60)
#     cache.purgeCache()

async def cacheWriteTask():
    while True:
        await asyncio.sleep(600)
        userDB.writeCache(cache.users)

async def monthlyThreshold():
    ####
    ## Check if today is the first day of the month
    ## If it is not the first day, get the amount of time until tomorrow and sleep until then
    ####

    while True:
        today = datetime.now()
        if today.day == 1:
            userDB.monthlySubduction(cache.users, config.threshold)
            # TODO: Role assignment

        # Conversion of hours and minutes to seconds
        timeUntilTomorrow = ((24 - today.hour) * 3600) +\
                            ((60 - today.minute) * 60) + \
                            ((60 - today.second))

        await asyncio.sleep(timeUntilTomorrow)