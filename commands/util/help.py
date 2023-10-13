# File: Help
# Description: This command will display help for a command or all
#              if none specified.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import os
from components import Command


class Help(Command):
    """
    This command will display help for a command or all
    if none specified.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

