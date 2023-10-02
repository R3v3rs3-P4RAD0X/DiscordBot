# DiscordBot
import discord
import rich
import os
import config
import client


class Main:
    # Constructor
    def __init__(self):
        # Load the .env file
        self.env = config.ReadKeyValStore('.env')

        # Initialise the Rich console
        self.console = rich.get_console()

        # Initialise the database class
        self.database = config.Database()

        # Initialise the Discord client
        self.client = client.Client(
            intents=discord.Intents.all(), 
            console=self.console,
            config=config,
            database=self.database
        )

    # A method for running the bot
    def start(self):
        # Run the bot
        self.client.run(self.env['TOKEN'])

# Run the Main class
if __name__ == '__main__':
    # Initialise the Main class
    main = Main() 

    # Call the start method
    main.start()
