# Imports
import subprocess
import importlib
import command
import asyncio
import random
from types import ModuleType


class Config:

    def __init__(self):
        pass

    # Importing a module
    def Import(self, path: str) -> ModuleType:
        return importlib.import_module(path)

    # Reloading a module
    def Reload(self, module: ModuleType) -> ModuleType:
        return importlib.reload(module)

    # Finding a file in a directory
    def Find(self, file: str, directory: str) -> str:
        # Construct the command
        command = ["fd", file, directory]

        # Run the command and get the output
        output = subprocess.check_output(command, text=True).split("\n")[:-1]

        # Loop through the output and run HandlePath
        output = [self.HandlePath(path) for path in output]

        # Return the output
        return output[0] if len(output) > 0 else False

    # Finding all files in a directory
    def FindAll(self, ext: str, directory: str) -> list[str]:
        # Construct the command
        command = ["fd", ext, directory]

        # Run the command and get the output
        output = subprocess.check_output(command, text=True).split("\n")[:-1]

        # Loop through the output and run HandlePath
        output = [self.HandlePath(path) for path in output]

        # Return the output
        return output if len(output) > 0 else False

    # Handling paths from strings
    def HandlePath(self, path: str) -> str:
        # Split by the dot and select first element
        path = path.split(".")[0]

        # Replace the slashes with dots
        path = path.replace("/", ".")

        # Return the path
        return path

    # Handling command finding and loading
    def HandleCommand(self, searchstr: str) -> command.Command:
        # Get the command
        command = self.Find(searchstr + ".py", "commands")

        # Check if the command exists
        if not command or len(command) == 0:
            return False

        # Get the module of the command
        module = self.Import(command)

        # Reload the module
        module = self.Reload(module)

        # Check if the module has searchstr.title() as attr
        if not hasattr(module, searchstr.title()):
            return False

        # Return the class
        return getattr(module, searchstr.title())

    # Handling command aliases
    def HandleCommandAliases(self) -> dict[str, str]:
        # Get all the files in the commands directory
        output = self.FindAll(".py", "commands")

        # Aliases dictionary
        aliases = {}

        # Loop through the output
        for file in output:
            # Get the module of the file, reload the file
            module = self.Import(file)

            # Get the name from file
            name = file.split(".")[-1]

            # Check if the module has the class
            if hasattr(module, name.title()):
                # Get the class
                cls = getattr(module, name.title())

                # Check if the class has the aliases attribute
                if hasattr(cls, "aliases"):
                    # Loop through the aliases
                    for alias in cls.aliases:
                        # Add the alias to the aliases dictionary
                        aliases[alias] = name

        # Return the aliases dictionary
        return aliases

    # Handling event finding and loading
    def HandleEvents(self) -> list[tuple[str, any]]:
        # Get all events from events directory
        output = self.FindAll(".py", "events")

        # Events list
        events = []

        # Loop through the output
        for file in output:
            # Get the module of the file, reload the file
            module = self.Import(file)

            # Get the name from file
            name = file.split(".")[-1]

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

    # Handles reading key=value files and returning the values as a dictionary
    def HandleKeyValStore(self, filename: str) -> dict[str, str]:
        # Create the dictionary
        keyval = {}

        # Open the file
        with open(filename, "r") as f:
            # Loop through the lines, ignoring comments are keyless lines
            for line in f:
                if line[0] == "#":
                    continue

                # If the line doesn't have a key, raise an error
                if line.startswith("="):
                    raise ValueError(f"No key found in '{filename}'")

                # Split the line into a key and value
                key, value = line.split("=")

                # Check if the key already exists
                if key in keyval:
                    # Raise an error if the key already exists
                    raise ValueError(
                        f"Duplicate key '{key}' found in '{filename}'")

                # Add the key and value to the dictionary
                keyval[key.strip()] = value.strip()

        # Return the dictionary
        return keyval

    # A levenstein distance function
    def Similar(self, str1, str2):
        len_str1 = len(str1)
        len_str2 = len(str2)

        # Create a matrix to store distances
        matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]

        # Initialize the matrix
        for i in range(len_str1 + 1):
            matrix[i][0] = i
        for j in range(len_str2 + 1):
            matrix[0][j] = j

        # Fill in the matrix
        for i in range(1, len_str1 + 1):
            for j in range(1, len_str2 + 1):
                cost = 0 if str1[i - 1] == str2[j - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,  # Deletion
                    matrix[i][j - 1] + 1,  # Insertion
                    matrix[i - 1][j - 1] + cost,  # Substitution
                )

        # Calculate the similarity ratio
        max_len = max(len_str1, len_str2)
        similarity = (1 - (matrix[len_str1][len_str2] / max_len)) * 100

        return round(similarity)

    # A function for filtering a list by it's type and validating using a passed function if needed
    def FilterFirstType(self,
                        array: list,
                        type: type,
                        validate: callable = None) -> any:
        # Check if array is a list and length > 0
        if not isinstance(array, list) or len(array) == 0:
            return False

        # Loop through the array
        for item in array:
            try:
                # Try to cast the item to the type
                item = type(item)

                # Check if validate is a function
                if (validate and callable(validate)) and not validate(item):
                    continue

                # Return the item
                return item
            except Exception:
                # Continue if the cast fails
                continue

        # Return False
        return False

    # A functio for generating a random number between a min and max
    def RandomNumber(self, min: int, max: int) -> int:
        return random.randint(min, max)
