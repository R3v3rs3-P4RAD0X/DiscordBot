# File: Client
# Description: This is the heart of the discord bot, this class
#              is an extension of discord.Client
# Author: StrangeParadox
# Version: 0.0.2

# Imports
import discord
import rich
from components.handler import Handler
from components.ratelimit import Ratelimit


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

        self.console: rich.console.Console = kwargs.get("console")
        self.env: dict = {}
        self.command_handler: Handler = kwargs.get("command_handler")
        self.ratelimit: Ratelimit = kwargs.get("ratelimit")
