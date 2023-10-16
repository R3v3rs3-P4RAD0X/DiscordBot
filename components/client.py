# File: Client
# Description: This is the heart of the discord bot, this class
#              is an extension of discord.Client
# Author: StrangeParadox
# Version: 0.0.4

# Imports
import discord
from components.handler import Handler
from components.ratelimit import Ratelimit
from components.database import Database, User, Economy
from components.economy import Economy
from components.logger import Logger

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

        self.console: Logger = kwargs.get("console")
        self.env: dict = {}
        self.command_handler: Handler = kwargs.get("command_handler")
        self.ratelimit: Ratelimit = kwargs.get("ratelimit")
        self.database: Database = kwargs.get("database")
        self.db_supported_types: dict[str, User|Economy] = {
            "user": User,
            "economy": Economy
        }
        self.economy: Economy = Economy(self)
