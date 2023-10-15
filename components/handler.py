# File: CommandHandler
# Description: Will handle the locating, caching and loading/reloading of each command.
#              Whilst doing this it all makes sure the command passes
#              the checks.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import subprocess
import importlib
import datetime
import rich


class Handler:
    """
    Will handle the locating, caching and loading/reloading of each item.
    Whilst doing this it all makes sure the item passes
    the checks.
    """

    def __init__(self, folder: str = "commands", timeout: int = 20, console: rich.console.Console = rich.get_console()):
        """
        Initialize the class.
        Set the variables.
        """
        self.folder = folder
        self.cache = {}
        self.console = console
        self.longest = max([len(item) for item in self.find_all()]) + 1


    def generalise(self, path: str) -> str:
        """
        Converts the string to a generalised format.
        That can be used in importlib
        """
        # Remove the .py
        path = path.replace(".py", "")

        # Replace the / with .
        path = path.replace("/", ".")

        # Return the path
        return path
        
    def find_all(self) -> list[str]:
        """
        This method will use subprocess to run a linux command to find all the item 
        files in the self.folder variable.
        """
        # Construct the command
        command = ["fd", ".py", self.folder]

        # Run the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        # Get the output
        output, error = process.communicate()

        # Decode the output
        output = output.decode("utf-8")

        # Split the output
        output = output.split("\n")

        # Remove the last item
        output.pop()

        # Return the output
        return [self.generalise(path) for path in output] or []

    def find(self, name) -> str:
        """
        This method will use subprocess to run a linux command to find a item
        file in the self.folder variable.
        """
        # Construct the command
        command = ["fd", f"{name.lower()}.py", self.folder]

        # Run the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        # Get the output
        output, error = process.communicate()

        # Decode the output
        output = output.decode("utf-8")

        # Split the output
        output = output.split("\n")

        # Remove the last item
        output.pop()

        # Return the output
        return None if len(output) == 0 else self.generalise(output[0])
    
    def load(self, path: str, developer: bool = False) -> object:
        """
        Loads the item from the path.
        If the item is in the cache and has not exceeded the timeout,
        return the item from the cache.
        
        If the item is not in the cache,
        load the item and add it to the cache.

        If the item cache has exceeded the timeout,
        reload the item and add it to the cache.
        """
        # Get the name of the item
        name = path.split(".")[-1] if self.folder != "commands" else path.split(".")[-1].title()
        
        # Check if the developer flag is set
        if not developer:
            # Check if the item is in the cache
            if path in self.cache:
                # Check if the item has exceeded the timeout
                if self.cache[path]["timeout"] > datetime.datetime.now():
                    # Return the item from the cache
                    return self.cache[path]
                
                # Reload the module
                module = importlib.reload(importlib.import_module(path))

                 # Check if the module has an attribute called name
                if not hasattr(module, name):
                    # Print the error
                    self.console.log(f"Handler -> [red]Error[/red]: {path.ljust(self.longest, ' ')} ([red]Missing name attribute[/red])")

                    # Return None
                    return None
                
                # Get the item
                obj = getattr(module, name)

                # Update the cache
                self.cache[path] = {
                    "module": module,
                    "object": obj,
                    "name": name,
                    "timeout": datetime.datetime.now() + datetime.timedelta(seconds=20)
                }

                # Return the item from the cache
                return self.cache[path]

            # Load the module
            module = importlib.import_module(path)

             # Check if the module has an attribute called name
            if not hasattr(module, name):
                # Print the error
                self.console.log(f"Handler -> [red]Error[/red]: {path.ljust(self.longest, ' ')} ([red]Missing name attribute[/red])")

                # Return None
                return None
            
            # Get the item
            obj = getattr(module, name)

            # Update the cache
            self.cache[path] = {
                "module": module,
                "object": obj,
                "name": name,
                "timeout": datetime.datetime.now() + datetime.timedelta(seconds=20)
            }

            # Return the item from the cache
            return self.cache[path]
        
        # Print the path
        self.console.log(f"Handler -> [red]Load[/red]: {path.ljust(self.longest, ' ')} ([magenta]Developer[/magenta])")

        # Load the item
        module = importlib.import_module(path)

        # Reload the item
        module = importlib.reload(module)

        # Check if the module has an attribute called name
        if not hasattr(module, name):
            # Print the error
            self.console.log(f"Handler -> [red]Error[/red]: {path.ljust(self.longest, ' ')} ([red]Missing name attribute[/red])")

            # Return None
            return None
        
        # Get the item
        obj = getattr(module, name)

        # Update the cache
        self.cache[path] = {
            "module": module,
            "object": obj,
            "name": name,
            "timeout": datetime.datetime.now() + datetime.timedelta(seconds=20)
        }

        # Return the item
        return self.cache[path]
