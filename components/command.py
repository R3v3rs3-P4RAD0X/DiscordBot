# File: Command
# Description: This is the basis of each command. A command will
#              just extend this class and implement a way of running
#              the command.
# Author: StrangeParadox
# Version: 0.0.4

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
            # Get the colour
            colour = kwargs["colour"]
            # Check what type of colour it is
            if isinstance(colour, str):
                # If it's a string, get the attribute from discord.Colour
                colour = getattr(discord.Colour, colour)()

            if isinstance(colour, (list, tuple)):
                # If it's a list or tuple, create a discord.Colour from the list
                colour = discord.Colour.from_rgb(*colour)

            if isinstance(colour, int):
                # If it's an int, create a discord.Colour from the int
                colour = discord.Colour(colour)

            if isinstance(colour, dict):
                # Get the RGB values from the dict
                colour = discord.Colour.from_rgb(**colour)

            # Set the colour
            embed.colour = colour

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

        # Set the timestamp
        if "timestamp" in kwargs:
            embed.timestamp = kwargs["timestamp"]

        # Return the embed
        return embed
    
    async def paginate(self, embeds: list[discord.Embed], timeout: int = 60):
        """
        Creates a pagination session.
        """

        current_page = 0

        class Paginate(discord.ui.View):
            def __init__(this, pages: list[str|discord.Embed]):
                super().__init__()
                this.pages = pages

            def invert(this, type: bool = True) -> None:
                """
                Changes the colour of the buttons.
                """
                # Check if type was passed: True = next, False = prev | 0 = prev, 1 = next
                if type:
                    this.children[0].disabled = current_page <= 0
                    this.children[0].style = discord.ButtonStyle.green if not this.children[0].disabled else discord.ButtonStyle.danger
                    this.children[1].disabled = current_page == len(this.pages) - 1
                    this.children[1].style = discord.ButtonStyle.danger if this.children[1].disabled else discord.ButtonStyle.green
                else:
                    this.children[0].disabled = current_page <= 0
                    this.children[0].style = discord.ButtonStyle.green if not this.children[0].disabled else discord.ButtonStyle.danger
                    this.children[1].disabled = current_page == len(this.pages) - 1
                    this.children[1].style = discord.ButtonStyle.danger if this.children[1].disabled else discord.ButtonStyle.green
            
            @discord.ui.button(label='<<', disabled=True, custom_id='prev', style=discord.ButtonStyle.danger)
            async def previous_page(this, interaction, _):
                nonlocal current_page

                # Check if the user is the author
                if interaction.user.id != self.message.author.id:
                    return
                
                # Check if current page < 0 if so, set current page to len(pages) - 1 else subtract 1
                current_page = len(this.pages) - 1 if current_page - 1 < 0 else current_page - 1

                # Call the invert method
                this.invert(False)
    
                # Check if the list is a list of embeds or strings
                if isinstance(this.pages[current_page], discord.Embed):
                    await interaction.response.edit_message(embed=this.pages[current_page], view=this)
                else:
                    await interaction.response.edit_message(content=this.pages[current_page], view=this)

            @discord.ui.button(label='>>', custom_id='next', style=discord.ButtonStyle.green)
            async def next_page(this, interaction, _):
                nonlocal current_page

                # Check if the user is the author
                if interaction.user.id != self.message.author.id:
                    return

                # Check if current page > len(pages) if so, set current page to 0 else add 1
                current_page = 0 if current_page + 1 >= len(this.pages) else current_page + 1

                # Call the invert method
                this.invert(True)

                # Check if the list is a list of embeds or strings
                if isinstance(this.pages[current_page], discord.Embed):
                    await interaction.response.edit_message(embed=this.pages[current_page], view=this)
                else:
                    await interaction.response.edit_message(content=this.pages[current_page], view=this)
                
            @discord.ui.button(label='Close', custom_id='close', style=discord.ButtonStyle.danger)
            async def close(this, interaction: discord.Interaction, _):
                nonlocal current_page

                # Check if the user is the author
                if interaction.user.id != self.message.author.id:
                    return
                
                # Stop the listener
                this.stop()

                await interaction.response.edit_message(view=None, delete_after=1)
                await self.message.delete(delay=1)

        # Create the view
        view = Paginate(embeds)
        
        # Check if the list is a list of embeds or strings
        if isinstance(embeds[current_page], discord.Embed):
            # Check if the bot has the embed_links permission
            if self.bot_permissions.has("embed_links"):
                await self.message.channel.send(embed=embeds[current_page], view=view)
            else:
                await self.send("I don't have the embed_links permission.")

        else:
            await self.message.channel.send(content=embeds[current_page], view=view)

    
    def send(self, content: str = None, embed: discord.Embed = None):
        """
        Sends a message to the channel.
        """

        return self.message.channel.send(content=content, embed=embed)

    async def run(self):
        """
        Run method, if not overridden, will just send the help message.
        """
        
        # Check if the bot doesn't have the embed_links permission
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
            return True, "This command is disabled."

        # Check if the command is a developer command
        if self.dev and self.message.author.id != self.client.application.owner.id:
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
        if not self.config['ratelimiter'].check_command(self, self.message.author.id, self.ratelimit):
            return True, "You're being ratelimited."

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
