# File: On_Message
# Description: Handles the message event from the client.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
import discord
from components import Client

async def on_message(self: Client, message: discord.Message):
    """
    Handles the message event from the client.
    """
    # Check if the message wasn't sent in a guild
    if message.channel.type != discord.ChannelType.text:
        # Return
        return
    
    # Check if the message was received from a bot
    if message.author.bot:
        # Return
        return
    
    # Get the prefix from the database
    prefix = self.env.get("PREFIX", "s!")

    # Check if the message doesn't start with the prefix
    if not message.content.startswith(prefix):
        # Return
        return
    
    # Get the command and args from the message
    command, *args = message.content.lstrip(prefix).strip().split()

    # Find the command using the command handler
    found = self.command_handler.find(command)

    # Check if the command was found
    if found:
        # Load the command
        command = self.command_handler.load(found, True if message.author.id == 472571500637978626 else False)

        # Initialize the command
        cmd = command["object"](message, args, self, {
            "ratelimiter": self.ratelimit
        })

        # Run the command
        returned = await cmd.execute()

        # Check if the instance of returned is a tuple
        if isinstance(returned, tuple):
            print(returned[0])
        

    


