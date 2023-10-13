# File: Command
# Description: This is the basis of each command. A command will
#              just extend this class and implement a way of running
#              the command.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
from components.help import Help
from components.permissions import Permissions
from components.ratelimit import Ratelimit
import discord


class Command:
    """
    This is the base class for all commands.
    Functions for all commands are defined here.
    Call the execute() method to run the command if the checks pass.
    """

    help: Help = Help
    permissions: ["send_messages", "read_messages"]

    dev = False
    hidden = False
    NSFW = False
    economy = False
    music = False
    disabled = False

    def __init__(self, message: discord.Message, args: list[str], client: any = None, config: dict = {}):
        """
        Initializes the command and run's the help setup.
        """
        self.message = message
        self.args = args
        self.client = client
        self.config = config
        self.command_permissions = Permissions(False, *self.permissions)
        self.user_permissions = Permissions(self.message.channel.permissions_for(self.message.author).value)
        self.bot_permissions = Permissions(self.message.channel.permissions_for(self.message.guild.me).value)
        self.ratelimit = {
            "timeout": 5,
            "limit": 1,
            "ratelimit": "command"
        }
        self.aliases = [self.__class__.__name__[::-1].lower()]

        self.help = self.help(self)


    def create_embed(self, **kwargs) -> discord.Embed:
        """
        Creates an embed with the given parameters.
        """

        return discord.Embed(**kwargs)
    
    def send(self, content: str = None, embed: discord.Embed = None):
        """
        Sends a message to the channel.
        """

        return self.message.channel.send(content=content, embed=embed)

    async def run(self):
        """
        Run method, if not overridden, will just send the help message.
        """
        
        # Check if the bot has the embed_permissions
        if not self.bot_permissions.has("embed_links"):
            # Send the get_text() of the help message
            await self.send(content=self.help.get_text())
            return
        
        # Send the embed of the help message
        await self.send(embed=self.help.get_embed())

    async def check(self) -> (bool, str):
        """
        Makes sure all checks related to the command pass.
        """
        if self.disabled:
            return False, "This command is disabled."

        # Check if the command is a developer command
        if self.dev and self.message.author.id not in self.config["developers"]:
            return True, "This is a developer command."
        
        # Check if the command is NSFW
        if self.NSFW and not self.message.channel.is_nsfw():
            return True, "This command can only be used in NSFW channels."
            
        # Check if the bot has the required permissions
        if self.bot_permissions < self.command_permissions:
            # Get the permissions that the bot doesn't have
            missing = self.command_permissions.missing(self.bot_permissions)

            # Check if the bot doesn't have send_messages permission
            if self.bot_permissions < Permissions(False, "send_messages"):
                return True, "I don't have the required permissions to run this command. I need the send_messages permission."
            
            # Send the missing permissions message
            resp = await self.send(f"{self.client.user.name} doesn't have the required permissions to run this command.\nMissing permissions: {', '.join(m['name'] for m in missing)}")
            await resp.delete(delay=10)
            return True, "I don't have the required permissions to run this command."
        
        # Check if the user has the required permissions
        if self.user_permissions < self.command_permissions:
            # Get the permissions that the user doesn't have
            missing = self.command_permissions.missing(self.user_permissions)

            # Send the missing permissions message
            resp = await self.send(f"You don't have the required permissions to run this command.\nMissing permissions: {', '.join(m['name'] for m in missing)}")
            await resp.delete(delay=10)
            return True, "You don't have the required permissions to run this command."
        
        # Check if the command is ratelimited
        if not self.config["ratelimiter"].check_command(self, self.message.author.id if self.ratelimit["ratelimit"] == "command" else self.message.guild.id, self.ratelimit):
            return True, "You are ratelimited."

        # Return False if all checks pass
        return False, None

    async def execute(self):
        """
        Executes the command after it passes all the checks.
        """
        # Run the checks and handle the return
        check, message = await self.check()

        if check:
            # Return the message
            return (message, False)

        # Run the command
        return await self.run()
