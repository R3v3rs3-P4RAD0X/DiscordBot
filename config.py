# Imports
import datetime
import subprocess
import importlib
import command
import asyncio

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

# A function for loading all the events from events
def LoadEvents() -> [str]:
    # Get all events from events directory
    output = WalkDirectory('events', '.py')

    # Events list
    events = []

    # Loop through the output
    for file in output:
        # Get the module of the file, reload the file
        module = ImportReload(file)

        # Get the name from file
        name = file.split('.')[-1]

        # Check if the module has the function
        if hasattr(module, name):
            # Get the function
            func = getattr(module, name)

            # Check if the function is a coroutine
            if not asyncio.iscoroutinefunction(func):
                # Raise an error if the function is not a coroutine
                raise TypeError(f"Event '{name}' is not a coroutine")
            
            # Add the event to the events list
            events.append((name, func))

    # Return the events list
    return events

# A function for loading all the aliases from commands
def LoadCommandAliases() -> [str]:
    aliases = {}

    # Get all the files in the commands directory
    output = WalkDirectory('commands', '.py')

    # Loop through the output
    for file in output:
        # Get the module of the file, reload the file
        module = ImportReload(file)

        # Get the name from file
        name = file.split('.')[-1]

        # Check if the module has the class
        if hasattr(module, name.title()):
            # Get the class
            cls = getattr(module, name.title())

            # Check if the class has the aliases attribute
            if hasattr(cls, 'aliases'):
                # Loop through the aliases
                for alias in cls.aliases:
                    # Add the alias to the aliases dictionary
                    aliases[alias] = name

    return aliases

# A function for returning the paths of all files inside a directory
def WalkDirectory(directory, file_ext, replace: bool = True) -> [str]:
    # Construct the command
    command = ['fd', file_ext, directory]

    # Run the command and get the output
    output = subprocess.check_output(command, text=True).split('\n')[:-1]

    # If replace is True, replace the directory slashses with dots and remove the extension
    if replace:
        output = [file.replace('/', '.').replace(file_ext, '') for file in output]

    # Return the output
    return output

# A function for searching a directory for a specific file
def SearchDirectory(directory, file_ext, searchstr, replace: bool = True) -> str:
    # Construct the command
    command = ['fd', f"{searchstr}{file_ext}", directory]

    # Run the command and get the output
    output = subprocess.check_output(command, text=True).split('\n')[:-1]

    # If replace is True, replace the directory slashses with dots and remove the extension
    if replace:
        output = [file.replace('/', '.').replace(file_ext, '') for file in output]

    # Return the first item in the output
    return output[0] if output else False

# A function for importing and reloading a module
def ImportReload(path, reload: bool = True):
    # Get the module
    module = importlib.import_module(path)

    # If reload is True reload the module
    if reload:
        module = importlib.reload(module)

    # Return the module
    return module


# A function for handling the loading of a command
def HandleCommand(searchstr: str) -> command.Command:
    # Get the command
    command = SearchDirectory('commands', '.py', searchstr)

    # Check if the command exists
    if not command or len(command) == 0:
        return False

    # Get the module of the command
    module = ImportReload(command)

    # Check if the module has searchstr.title() as attr
    if not hasattr(module, searchstr.title()):
        return False

    # Return the class
    return getattr(module, searchstr.title())
