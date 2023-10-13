# File: Ping
# Description: Pong! The first basic command implemented into the bot, will
#              have support for -v which makes it verbose and displays
#              response time.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
from components import Command


class Ping(Command):
    """
    Pong! The first basic command implemented into the bot, will
    have support for -v which makes it verbose and displays
    response time.
    """
    permissions = ["send_messages", "read_messages"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        Set the variables.
        """
        super().__init__(*args, **kwargs)


    async def run(self):
        """
        Run the command.
        """
        # Send a message to the channel
        await self.send("Pong!")