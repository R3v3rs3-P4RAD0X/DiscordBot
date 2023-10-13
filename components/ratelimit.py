# File: Ratelimit
# Description: Allows rate limits on a command, therefore it can only
#              be ran x time per guild before it timesout.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import datetime
import time

class Ratelimit:
    """
    A class that represents a ratelimit for a command.

    Attributes:
    -----------
    command : Command
        The command that the ratelimit is applied to.
    limit : int
        The maximum number of times the command can be used within the specified time.
    time : int
        The time period (in seconds) during which the limit applies.
    type : str or tuple
        The type of ratelimit. Can be "guild", "user", or ("command", "guild").
    cache : dict
        A dictionary that stores the cache for the ratelimit.
    """

    def __init__(self, command, limit: int = 1, time: int = 5, type: str = "guild", disabled: bool = False):
        """
        Initializes the Ratelimit class with a command, limit, time, and cache.

        Parameters:
        -----------
        command : Command
            The command that the ratelimit is applied to.
        limit : int, optional
            The maximum number of times the command can be used within the specified time. Default is 1.
        time : int, optional
            The time period (in seconds) during which the limit applies. Default is 5.
        type : str or tuple, optional
            The type of ratelimit. Can be "guild", "user", or "command" = ("command", "guild"). Default is "guild".
        """
        self.command = command
        self.limit = limit
        self.time = time
        self.type = (type, "guild") if type == "command" else type
        self.disabled = disabled

        self.cache = {}

    def structure(self, id: int) -> dict:
        """
        Makes a structure for the cache.
        Only creates the structure if it doesn't exist.

        Parameters:
        -----------
        id : int
            The ID of the user or guild.

        Returns:
        --------
        dict
            The cache structure for the specified ID.
        """
        self.cache[self.type] = self.cache.get(self.type, {})
        self.cache[self.type][id] = self.cache[self.type].get(id, {
            "timestamp": datetime.datetime.now(),
            "uses": 0
        })
        self.cache[self.type][id][self.command.__class__.__name__] = self.cache[self.type][id].get(self.command.__class__.__name__, {
            "uses": 0,
            "timestamp": datetime.datetime.now()
        })

        return self.cache[self.type][id][self.command.__class__.__name__]

    def add(self, id: int, reset: bool = False):
        """
        Adds to the cache.

        Parameters:
        -----------
        id : int
            The ID of the user or guild.
        reset : bool, optional
            Whether to reset the cache. Default is False.
        """
        # Ensure the cache is structured correctly
        prev = self.structure(id)

        # Update the cache
        self.cache[self.type][id][self.__class__.__name__] = {
            "uses": prev['uses'] + 1 if not reset else 1,
            "timestamp": datetime.datetime.now() if self.cache[self.type][id][self.command.__class__.__name__]['timestamp'] + self.time < time.time() else prev['timestamp']
        }

        self.cache

    def limited(self, id: int) -> bool:
        """
        Checks the cache to see if the command is limited.

        Parameters:
        -----------
        id : int
            The ID of the user or guild.

        Returns:
        --------
        bool
            True if the command is limited, False otherwise.
        """
        # Check if the ratelimit is disabled
        if self.disabled:
            return False

        # Ensure the cache is structured correctly
        self.structure(id)

        cache = {}

        # Check the type of ratelimit
        if isinstance(self.type, tuple) and self.type[0] == "command":
            # Check if the command is limited
            if self.cache[self.type[1]][id][self.command.__class__.__name__]['timestamp'] + self.time < time.time():
                # Reset the cache
                self.cache[self.type[1]][id][self.command.__class__.name] = {
                    "uses": 0,
                    "timestamp": datetime.datetime.now()
                }

                cache = self.cache[self.type[1]][id][self.command.__class__.__name__]

        if self.type == "guild":
            # Check if the command is limited
            if self.cache[self.type]['timestamp'] + self.time < time.time():
                # Reset the cache
                self.cache[self.type] = {
                    "timestamp": datetime.datetime.now(),
                    "uses": 0
                }

                cache = self.cache[self.type]

        if self.type == "user":
            # Check if the command is limited
            if self.cache[self.type][id]['timestamp'] + self.time < time.time():
                # Reset the cache
                self.cache[self.type][id] = {
                    "uses": 0,
                    "timestamp": datetime.datetime.now()
                }

                cache = self.cache[self.type][id]

        # Check if the command is limited
        if cache['uses'] >= self.limit:
            # Check if the timestamp is over the limit
            if cache['timestamp'] + self.time < time.time():
                return True
            
            self.add(id)
            return False
        
        self.add(id)
        return False