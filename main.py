# DiscordBot
import discord
import rich
import config
import client
import database


class Main:
    # Constructor
    def __init__(self):
        # Initialise the config class
        self.config = config.Config()

        # Load the .env file
        self.env = self.config.HandleKeyValStore(".env")

        # Initialise the Rich console
        self.console = rich.get_console()

        # Initialise the database class
        self.database = database.Database()

        # Get the events
        events = self.config.HandleEvents()

        # Loop over the events
        for event in events:
            # Deconstruct the event
            name, func = event

            # Add the event to the client
            setattr(client.Client, name, func)

        # Initialise the Discord client
        self.client = client.Client(
            intents=discord.Intents.all(),
            console=self.console,
            config=self.config,
            database=self.database,
        )

    # A method for running the bot
    def start(self):
        # Run the bot
        self.client.run(self.env["TOKEN"])


# Run the Main class
if __name__ == "__main__":
    # Initialise the Main class
    main = Main()

    # Call the start method
    main.start()
