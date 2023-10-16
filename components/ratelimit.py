# File: Ratelimit
# Description: This file handle the timeouts and ratelimits of commnads on
#              a user, command or guild based setup.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
import datetime as dt

class Ratelimit:
    """
    This file handle the timeouts and ratelimits of commnads on
    a user, command or guild based setup.
    """

    def __init__(self):
        """
        Initialize the class.
        Set the variables.
        """
        self.cache = {
            "guilds": {},
            "users": {},
            "command": {}
        }

    def ensure(self, cache = None, key = None, default = {}) -> dict:
        """
        Gets an item from the cache, if it doesn't exist it will set it to the default value.
        """
        # Check if the key is in the cache
        if key not in cache:
            # Set the key to the default value
            cache[key] = default

        # Set the return data
        return cache[key]

    def check_command(self, command: object, ID: int, config: dict) -> bool:
        """
        Checks the cache of ratelimit for a command.
        If it's not in the cache it will add it.
        If it is in the cache it will check if the time has passed.
        If it has passed it will update the cache.
        If it hasn't passed it will return False.
        """
        # Destrucuturise the config -> if cache limit is >= {limit} and within last {timeout} seconds
        timeout = config['timeout'] # This will be the amount of time a command can be run in seconds
        limit = config['limit'] # This will be the amount of times the command can be used
        ratelimit = config['ratelimit'] # This will be the type of ratelimit

        # Destructurise the command
        name = command.__class__.__name__

        # Get the current time
        now = dt.datetime.now()
        
        # Match each case for the ratelimit
        match ratelimit:

            # If the ratelimit is guild
            case "guild":
                print("Guild")

            # If the ratelimit is user
            case "user":
                print("User")

            # If the ratelimit is command
            case "command":
                # Get the cache or default to {}
                cache = self.ensure(self.cache, ratelimit, { name: { ID: { "last": now, "amount": 0 } } })
                cache = self.ensure(cache, name, { ID: { "last": now, "amount": 0 }})
                cache = self.ensure(cache, ID, { "last": now, "amount": 0 })

                # Get the last time the command was run
                last = cache['last']

                # Get the amount of times it was ran
                amount = cache['amount']

                # Check if amount >= limit
                if amount >= limit:
                    # Check if the last + timeout > now
                    if last + dt.timedelta(seconds=timeout) > now:
                        # Return False
                        return False
                    
                    # Reset the amount
                    cache['amount'] = 0

                # Update the cache
                cache['last'] = now
                cache['amount'] += 1

                # Return True
                return True 
                

        # Return true if isn't timed out
        return True
        




