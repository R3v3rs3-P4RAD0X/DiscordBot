# File: Client
# Description: This is the heart of the discord bot, this class
#              is an extension of discord.Client
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import discord


class Client(discord.Client):
    """
    Client is an extension of the Discord Client and implements some custom functionality.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises the client.
        Binds passed data to the client.
        """
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        """
        Called when the client is ready.
        Will print basic information about the client.
        """
        
        # Print some basic information about the client
        print("Logged in as: {}".format(self.user))

        # Set the client's status
        await self.change_presence(activity=discord.Game(name="with Python"))

    async def on_message(self, message: discord.Message):
        pass
