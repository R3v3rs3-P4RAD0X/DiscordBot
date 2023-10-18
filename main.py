# File: Main
# Description: This is the heart of the project, this is where
#              all the different features and brought into one.
# Author: StrangeParadox
# Version: 0.0.3

# Imports
import components
import discord
import os
import rich
import sys

class Main:
    """
    This is the heart of the project, where all the different features are brought into one.

    Attributes:
    -----------
    components : object
        An object containing all the components of the bot.
    client : object
        An object representing the Discord bot client.
    env : dict
        A dictionary containing the environment variables loaded from the .env file.
    """

    def __init__(self):
        """
        Combine all the components into one and start the bot.
        """
        # Create the components object
        self.components = components

        # Initialise the logger
        self.console = self.components.Logger()

        # Clear the console
        os.system("clear" if os.name == "posix" else "cls")

        # Print the header
        self.console.print("[bold]StrangeParadox's Discord Bot[/bold]")


        # Get the env file read and loaded
        self.env = self.components.Util().read_key_val_file(".env")

        # Create the database object
        self.database = self.components.Database(self.env["MYSQL_URL"])

        # Create the command handler
        self.command_handler = self.components.Handler(console=self.console)

        # Create the event handler
        self.event_handler = self.components.Handler("events", console=self.console)

        # Get the longest lengthed item
        self.longest = max(self.command_handler.longest, self.event_handler.longest)

        # Loop over the commands and register them
        for found in self.command_handler.find_all():
            command = self.command_handler.load(found)

            self.console.log("Handler -> [green]Command[/green]: {0} ([green]Loaded[/green])".format(command['name'].ljust(self.longest, ' ')))

        self.console.log()
        self.command_handler.initialised = True

        # Loop over the events and register them
        for found in self.event_handler.find_all():
            event = self.event_handler.load(found)

            # Register the event
            setattr(self.components.Client, event['name'], event['object'])

            # Print the event
            self.console.log(f"Handler -> [green]Event   [/green]: {event['name'].ljust(self.longest, ' ')} ([green]Loaded[/green])")

        self.console.log()
        self.event_handler.initialised = True

        # Initialise the components.RateLimit
        self.ratelimit = self.components.Ratelimit()

        # Create the client
        self.client = self.components.Client(
            intents=discord.Intents.all(), 
            console=self.console,
            command_handler=self.command_handler,
            ratelimit=self.ratelimit,
            database=self.database
        )

        

    def start(self):
        """
        Start the bot.
        """
        # Get the token from the env dictionary
        TOKEN = self.env["TOKEN"]

        # Remove the token from the env dictionary
        del self.env["TOKEN"]

        # Set the env dictionary as an attribute of the client
        self.client.env = self.env

        # Run the bot
        self.client.run(TOKEN)

        # Print the keyboard interrupt message
        os.system("clear" if os.name == "posix" else "cls")
        self.console.log("[red]Shutting down... will only take a second.[/red]")

        # Delete all the attributes of main
        del self.console
        del self.components
        del self.client
        del self.env
        del self.command_handler
        del self.event_handler
        del self.ratelimit
        del self.database

        # Exit the program
        sys.exit(0)

if __name__ == '__main__':
    Main().start()
