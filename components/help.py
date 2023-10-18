# File: Help
# Description: This component is for getting and displaying all the help
#              related data for any item.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
import discord

class Help:
    """
    This class is for getting and displaying all the help related data for any item.
    Takes an item which can be any object as a parameter.
    """

    def __init__(self, command, aliases: list[str] = [], description: str = "No description provided.", usage: str = None):
        """
        Initializes the help class.

        Args:
        - command (Command): The command object for which help is being generated.
        - aliases (list[str]): A list of aliases for the command.
        - description (str): A description of the command.
        - usage (str): A string representing the usage of the command.
        """
        self.aliases = aliases
        self.description = description
        self.usage = "{}{}".format(command.client.env['PREFIX'], command.__class__.__name__.lower()) if usage == None else usage
        self.command = command
        self.docstr = self.command.__doc__ or "No documentation provided."


    def get_embed(self) -> discord.Embed:
        """
        Returns an embed with all the help information.

        Returns:
        - discord.Embed: An embed containing all the help information.
        """
        embed = self.command.create_embed(
            title=self.command.__class__.__name__,
            description=f"{self.description}\n{self.docstr}",
            color=0x00ff00
        )

        embed.add_field(name="Usage", value=self.usage, inline=False)

        if len(self.aliases) > 0:
            embed.add_field(name="Aliases", value=", ".join(self.aliases), inline=False)

        return embed
    
    def get_text(self) -> str:
        """
        Returns a string with all the help information.

        Returns:
        - str: A string containing all the help information.
        """
        text = "**{}**\n{}\n\n**Usage:** {}\n".format(self.command.__class__.__name__, self.description, self.usage)

        if len(self.aliases) > 0:
            text += "**Aliases:** {}\n".format(", ".join(self.aliases))

        return text