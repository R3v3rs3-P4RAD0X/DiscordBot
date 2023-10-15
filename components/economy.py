# File: Economy
# Description: File will handle retrieving a user from the database, any
#              economy related commands e.g. gamble, profile.
# Author: StrangeParadox
# Version: 0.0.1
import random
import discord
from components.command import Command
class Economy:
    """
    File will handle retrieving a user from the database, any
    economy related commands e.g. gamble, profile.
    """

    def __init__(self, client: object = None):
        """
        Initialize the class.
        Set the variables.
        """
        self.database = {}
        self.win_chance = 0.3
        self.client = client

    def gamble(self, amount: int) -> tuple[bool, int, float]:
        """
        Handles the gamble command's logic.
        """
        # Determine the chance of winning
        chance: bool = random.choices([True, False], weights=[self.win_chance, 1 - self.win_chance])[0]
        
        # If the user won
        if chance:
            # Calculate the win multiplier
            win_multiplier = 1+(random.randint(1, 100) / 100)
                              
            # Calculate the amount won
            amount_won: int = amount * win_multiplier

            # Return the win tuple
            return True, round(amount_won), win_multiplier * 100
        else:
            # Return the loss tuple
            return False, amount, 0.0

    def profile(self, user_id: int, command: Command):
        """
        Handles the profile command's logic.
        """
        # Get the user from the database
        user = self.client.database.handle_user(user_id, create=False if user_id not in [command.message.author.id, self.client.user.id] else True)

        # Define message
        message = command.message

        # If the user is not in the database
        if user is None:
            # Send an error message
            return message.channel.send("User not found.")
        
        # If the user is in the database, get the economy data
        economy = self.client.database.handle_economy(user.id)

        # If the user has no economy data
        if economy is None:
            # Send an error message
            return message.channel.send("User has no economy data.")
        
        # Get the user from message.guild
        member = message.guild.get_member(user.id)
        
        # If the user has economy data, send the profile
        if message.channel.permissions_for(message.guild.me).embed_links:
            return message.channel.send(
                embed=command.create_embed(
                    title=f"{member.name}'s Profile",
                    description=f"{user.badges}",
                    fields=[
                        ("Balance", f"£{economy.balance:,}", True),
                        ("Bank", f"£{economy.bank:,}")
                    ],
                    thumbnail=member.avatar.url,
                    colour=discord.Colour.blurple(),
                    footer={
                        "text": f"Requested by {message.author.name}",
                        "icon_url": message.author.avatar.url
                    },
                    author={
                        "name": f"{message.guild.me.name}",
                        "icon_url": message.guild.me.avatar.url
                    }
                )
            )
        else:
            return message.channel.send(content=f"{member.name}'s Profile\n{user.badges if len(user.badges) > 0 else ''}\nBalance: £{economy.balance:,}\nBank: £{economy.bank:,}")