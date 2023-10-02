# Imports
import sqlite3
import datetime

# A database class
class Database:
    cache = {
        'guilds': {},
        'users': {},
    }

    file = 'data/storage.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def check_cache(self, table, id) -> bool:
        # Check if the table exists in the cache
        if table not in self.cache:
            return False
        
        # Check if the id exists in the cache
        if id not in self.cache[table]:
            return False
        
        # Check if the data is older than 5 minutes
        if (datetime.datetime.now() - self.cache[table][id]['timestamp']).seconds > 300:
            del self.cache[table][id]
            return False
        
        # Return True if the data is in the cache and is less than 5 minutes old
        return True
    

    def get_guild(self, guildID: int) -> dict:
        # Check if the data is in the cache
        if self.check_cache('guilds', guildID):
            return self.cache['guilds'][guildID]['data']

        # Execute the data/queries/guild_table.sql query
        self.cursor.execute(open('data/queries/guild_table.sql', 'r').read())

        # Check if data exists for the guildID
        self.cursor.execute('SELECT * FROM guilds WHERE guildID=?', (guildID,))

        # Fetch the data
        data = self.cursor.fetchone()

        # Check if the data exists
        if data is None:
            # Data doesn't exist, so insert a new entry
            self.cursor.execute('INSERT INTO guilds (guildID, prefix) VALUES (?, ?)',
                                (guildID, 's!'))
            self.conn.commit()

            # Fetch the data (whether it was existing or newly created)
            self.cursor.execute('SELECT * FROM guilds WHERE guildID=?', (guildID,))

            # Fetch the data
            data = self.cursor.fetchone()

        # Convert the data to a dictionary
        data = {
            'id': data[0],
            'guildID': data[1],
            'prefix': data[2],
        }

        # Add the data to the cache
        self.cache['guilds'][guildID] = {
            'data': data,
            'timestamp': datetime.datetime.now()
        }

        # Return the data
        return data