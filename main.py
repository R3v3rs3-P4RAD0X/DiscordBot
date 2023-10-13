# File: Main
# Description: This is the heart of the project, this is where
#              all the different features and brought into one.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import components
import discord

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
        self.components = components

        # Create the client
        self.client = self.components.Client(intents=discord.Intents.all())

        # Get the env file read and loaded
        self.env = self.components.Util().read_key_val_file(".env")

    def start(self):
        """
        Start the bot.
        """
        # Run the bot
        self.client.run(self.env["TOKEN"])


if __name__ == '__main__':
    Main().start()