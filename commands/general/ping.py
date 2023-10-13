# File: Ping
# Description: This is the ping command, responds with a simple pong.
#              If provided with -v for verbose it'll also include the
#              response time.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
from components import Command


class Ping(Command):
    """
    This is the ping command, responds with a simple pong.
    If provided with -v for verbose it'll also include the
    response time.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

