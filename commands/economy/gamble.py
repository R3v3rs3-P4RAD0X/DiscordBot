# File: Gamble
# Description: Handles the gamble command running in the economy handler.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
from components import Command

class Gamble(Command):
    """
    Handles the gamble command running in the economy handler.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        Set the variables.
        """
        super().__init__(*args, **kwargs)

        self.ids = [
            412812963288973314,
            472571500637978626
        ]

    async def run(self):
        """
        Run the command.
        """
        # Get the user from the database
        user = self.client.database.handle_user(self.message.author.id)

        # Get the economy from the database
        economy = self.client.database.handle_economy(user.id)

        # Check if the user has passed args
        if len(self.args) < 1:
            return await self.message.channel.send("You must pass a number to gamble!")
        
        # Check if the user has passed a valid number
        if not self.args[0].isdigit():
            return await self.message.channel.send("You must pass a valid number to gamble!")
        
        # Check if the user has enough money to gamble
        if int(self.args[0]) > economy.balance:
            return await self.message.channel.send("You don't have enough money to gamble that much!")
        
        # Check if the user's number is < 1
        if int(self.args[0]) < 1:
            return await self.message.channel.send("You must pass a number > 0 to gamble!")
        
        # Check if the user's number is > 125000
        if int(self.args[0]) > 125000 and not self.message.author.id in self.ids:
            return await self.message.channel.send("You can't gamble more than 125000!")
        
        # Gamble the money
        won, amount, chance = self.client.economy.gamble(int(self.args[0]))

        if won:
            economy.balance += amount

        else:
            economy.balance -= int(self.args[0])

        self.client.database.update_economy(
            user_id=self.message.author.id,
            balance=economy.balance
        )

        # Check if the bot can embed_links:
        if self.bot_permissions.has("embed_links"):
            await self.send(embed=self.create_embed(
                title = f"{self.message.author.name}'s Gamble",
                description = "You {} £{} with a {}% chance!".format(
                    "won" if won else "lost",
                    f"{amount:,}",
                    chance
                ),
                colour=0x00ff00 if won else 0xff0000
            ))
            return
        
        # Send the message
        await self.send("{} {} £{} with a {}% \chance!".format(
            self.message.author.name,
            "won" if won else "lost",
            f"{amount:,}",
            chance
        ))