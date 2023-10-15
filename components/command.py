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
    permissions: list[str] = ["send_messages", "read_messages"]

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

        Parameters:
            title: str
            description: str
            colour: Colour
            footer: dict { text: str, icon_url: str}
            thumbnail: str
            image: str
            author: dict { name: str, url: str, icon_url: str}
            fields: list[dict] { name: str, value: str, inline: bool}
        """

        # Create the embed
        embed = discord.Embed()

        # Set the title
        if "title" in kwargs:
            embed.title = kwargs["title"]

        # Set the description
        if "description" in kwargs:
            embed.description = kwargs["description"]

        # Set the colour
        if "colour" in kwargs:
            embed.colour = kwargs["colour"]

        # Set the footer
        if "footer" in kwargs:
            embed.set_footer(**kwargs["footer"])

        # Set the thumbnail
        if "thumbnail" in kwargs:
            embed.set_thumbnail(url=kwargs["thumbnail"])

        # Set the image
        if "image" in kwargs:
            embed.set_image(url=kwargs["image"])

        # Set the author
        if "author" in kwargs:
            embed.set_author(**kwargs["author"])

        # Set the fields
        if "fields" in kwargs:
            for field in kwargs["fields"]:
                embed.add_field(name=field[0], value=field[1], inline=field[2] if len(field) > 2 else False)

        # Return the embed
        return embed
    
    async def paginate(self, embeds: list[discord.Embed], timeout: int = 60):
        """
        Creates a pagination session.
        """
        # Send the first embed
        message = await self.message.channel.send(embed=embeds[0])

        # Add the reactions
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        # Define the check
        def check(reaction, user):
            return user.id == self.message.author.id and str(reaction.emoji) in ["⬅️", "➡️"]
        
        # Define the variables
        index = 0
        running = True

        # While the session is running
        while running:
            # Wait for a reaction
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=timeout, check=check)
            except:
                # If the timeout is reached, stop the session
                running = False
                break

            # If the reaction is left
            if str(reaction.emoji) == "⬅️":
                # If the index is 0, loop back to the end
                if index == 0:
                    index = len(embeds)-1
                else:
                    # Else, go back one
                    index -= 1
            # If the reaction is right
            elif str(reaction.emoji) == "➡️":
                # If the index is the end, loop back to the start
                if index == len(embeds)-1:
                    index = 0
                else:
                    # Else, go forward one
                    index += 1

            # Edit the message
            await message.edit(embed=embeds[index])

            # Remove the reaction
            await message.remove_reaction(reaction, user)

        # Remove the reactions
        await message.clear_reactions()

    
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
