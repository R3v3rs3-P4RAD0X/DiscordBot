# Imports
import datetime
import subprocess
import sqlite3
import importlib

# A function to read a key=value file and return the values as a dictionary
def ReadKeyValStore(filename):
    # Create the dictionary
    keyval = {}

    # Open the file
    with open(filename, 'r') as f:
        # Loop through the lines, ignoring comments are keyless lines
        for line in f:
            if line[0] == '#':
                continue

            # If the line doesn't have a key, raise an error
            if line.startswith('='):
                raise ValueError(f"No key found in '{filename}'")

            # Split the line into a key and value
            key, value = line.split('=')

            # Check if the key already exists
            if key in keyval:
                # Raise an error if the key already exists
                raise ValueError(f"Duplicate key '{key}' found in '{filename}'")

            # Add the key and value to the dictionary
            keyval[key.strip()] = value.strip()

    # Return the dictionary
    return keyval

# A function to get the current date and time in the format: 01-Jan-23 12:34:56
def GetDateTime():
    return datetime.datetime.now().strftime('%d-%b-%y %H:%M:%S')

# A function that'll handle the finding of a command using Rust FD
def SearchCommand(cmdstr):
    # Create the command for searching
    command = ['fd', f"{cmdstr}.py", 'commands']

    # Run the command and get the output
    output = subprocess.check_output(command, text=True).split('\n')[:-1]

    # Return the first item in the output
    return output[0] if output else False

# A function for handling the loading of a command
def HandleCommand(searchstr):
    if command := SearchCommand(searchstr):
        return getattr(
            # Reload the module
            importlib.reload(
                # Import the module
                importlib.import_module(
                    # Get the module name
                    command.replace('/', '.')\
                        .replace('.py', '')
                    )
                ), 
                # Get the class name
                searchstr.title(), 
                # Return False if the class doesn't exist
                False
            )

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