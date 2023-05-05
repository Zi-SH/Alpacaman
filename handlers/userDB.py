import sqlite3
database = "users.db"

def updateUser(id: int, count: int, time: float) -> None:
    c = sqlite3.connect(database)
    cur = c.cursor()

    cur.execute(f"INSERT OR REPLACE INTO users values('{id}', '{count}', '{time}'")
    c.commit()
    c.close()

def loadCache() -> (dict):
    c = sqlite3.connect(database)
    cur = c.cursor()

    query = cur.execute("SELECT * FROM users")

    ## Loop through all results and add them to the dict until we hit a None
    user = query.fetchone()
    users = {}
    while (user != None):
        users[user[0]] = [user[1], user[2]]
        user = query.fetchone()

    c.close()
    return users

def writeCache(cache: dict) -> None:
    c = sqlite3.connect(database)
    cur = c.cursor()

    for user in cache:
        # {user} = ID, [0] = message count, [1] = time
        cur.execute(f"INSERT OR REPLACE INTO users values('{user}', '{cache[user][0]}', '{cache[user][1]}')")

    c.commit()
    c.close()

def dbCheck() -> None:
    c = sqlite3.connect(database)
    cur = c.cursor()

    cur.execute("CREATE TABLE if not exists users (id integer UNIQUE, count integer, time float)")
    c.commit()
    c.close()

def monthlySubduction(cache: dict, threshold: int) -> None:
    c = sqlite3.connect(database)
    cur = c.cursor()

    print(cache)

    for user in cache:
        # {user} = ID, [0] = message count, [1] = time
        cur.execute(f"SELECT count FROM users WHERE id={user}")
        count = cur.fetchone()

        count = count[0] - threshold
        if count < 0:
            count = 0

        cur.execute(f"INSERT OR REPLACE INTO users values('{user}', '{count}', '{cache[user][1]}')")

    c.commit()
    c.close()

dbCheck()
