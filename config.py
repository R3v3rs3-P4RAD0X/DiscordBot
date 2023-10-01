# Imports
import datetime
import subprocess
import sqlite3
import importlib

# A function to read a key=value file and return the values as a dictionary
def ReadKeyValStore(filename):
    keyval = {}
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            key, value = line.split('=')
            keyval[key.strip()] = value.strip()
    return keyval


# A function to get the current date and time in the format: 01-Jan-23 12:34:56
def GetDateTime():
    return datetime.datetime.now().strftime('%d-%b-%y %H:%M:%S')

# A function that'll handle the finding of a command using Rust FD
def SearchCommand(cmdstr):
    # Create the command for searching
    command = [
        'fd',
        f"{cmdstr}.py",
        'commands',
    ]

    # Run the command
    output = subprocess.run(command, capture_output=True)

    # Check if the command was found
    if output.returncode == 0:
        # Get the output
        output = output.stdout.decode('utf-8').split('\n')

        # Remove the last item
        output.pop()

        # Return the output
        return output[0]
    
    else:
        # Return an empty list
        return False

# A function for handling the loading of a command
def HandleCommand(searchstr):
    # Search for the command
    command = SearchCommand(searchstr)

    # Check if the command was found
    if command:
        # Import the command and reload
        command = importlib.import_module(command.replace('/', '.').replace('.py', ''))
        command = importlib.reload(command)

        # Check if the command has a class called searchstr.title()
        if hasattr(command, searchstr.title()):
            # Return the command
            return getattr(command, searchstr.title())

    return False

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