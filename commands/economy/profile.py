# File: Profile
# Description: Get's a user's profile and displays it.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
from components.command import Command

class Profile(Command):
    """
    Get's a user's profile and displays it.
    """

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
        # Set the default user to the author
        user = await self.message.guild.fetch_member(self.message.author.id)

        # Check if the user has passed a user
        if len(self.args) > 0:
            # Check if the user mentioned a user
            if len(self.message.mentions) > 0:
                # If the user did  mention a user get the first user mentioned
                user = self.message.mentions[0]
            else:
                # Check if the user passed an ID or a username
                try:
                    # Try to get the user from the ID
                    user = await self.message.guild.fetch_member(int(self.args[0]))
                except:
                    # If the user did not pass an ID, get the user from the username
                    user = await self.message.guild.get_member_named(" ".join(self.args))
        
        

        # Send the economy.profile message
        await self.client.economy.profile(user.id, self)