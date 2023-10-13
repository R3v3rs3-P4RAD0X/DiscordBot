# File: On_Ready
# Description: Called when the client is ready.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
from components import Client
import discord

async def on_ready(self: Client):
    """
    Setups the bot when it is ready.
    """
    self.console.log(f"Logged in as: {self.user}")

    # Set the bots status
    await self.change_presence(activity=discord.Game(name="StrangeBot"))