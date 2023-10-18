# File: Mute
# Description: Will mute a user, can either be mentioned or passed
#              via ID.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
from components import Command

class Mute(Command):
    """
    Will mute a user, can either be mentioned or passed
    via ID.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        Set the variables.
        """
        super().__init__(*args, **kwargs)

