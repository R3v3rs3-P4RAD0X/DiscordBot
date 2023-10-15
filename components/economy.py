# File: Economy
# Description: File will handle retrieving a user from the database, any
#              economy related commands e.g. gamble, profile.
# Author: StrangeParadox
# Version: 0.0.1
import random
from components.client import Client

class Economy:
    """
    File will handle retrieving a user from the database, any
    economy related commands e.g. gamble, profile.
    """

    def __init__(self, client: Client = None):
        """
        Initialize the class.
        Set the variables.
        """
        self.database = {}
        self.win_chance = 0.475
        self.client = client

    def gamble(self, amount: int) -> tuple(bool, int, float):
        """
        Handles the gamble command's logic.
        """
        # Determine the chance of winning
        chance: bool = random.choices([True, False], weights=[self.win_chance, 1 - self.win_chance])

        # If the user won
        if chance:
            # Calculate the win multiplier
            win_multiplier = 1+(random.randint(1, 100) / 100)
                              
            # Calculate the amount won
            amount_won: int = amount * win_multiplier

            # Return the win tuple
            return tuple(True, amount_won, win_multiplier)
        else:
            # Return the loss tuple
            return tuple(False, amount, 0.0)

    def profile(self, user: int):
        """
        Handles the profile command's logic.
        """
        pass