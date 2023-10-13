# File: Ratelimit
# Description: This file handle the timeouts and ratelimits of commnads on
#              a user, command or guild based setup.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import datetime as dt
import time

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
        self.cache = {}

    def get_set(self, cache = None, key = None, default = {}) -> dict:
        if cache == None:
            cache = self.cache

        if key == None:
            raise Exception("No key was given.")
        
        cache[key] = cache.get(key, default)

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

        # Determine the type of ratelimit
        match ratelimit:
            case "guild":
                # When rate limit is guild, it will be based on the guild id and for all commands in that guild
                cache = self.get_set(self.cache, "guild")
                cache = self.get_set(cache, ID, {
                    "latest": [dt.datetime.now()]
                })

                # Get the latest {limit} time and check the count of the command
                latest = cache["latest"]

                # Check if the latest is >= limit
                latest = latest[0:min(limit, len(latest))]

                # Count the amount of times the command has been used
                count = len(latest)

                # Check if the first element in latest is within the timeout
                if (dt.datetime.now() - latest[0]).seconds <= timeout * 1000:
                    # Check if the count is >= limit
                    if count >= limit:
                        return False, "You are being ratelimited."
                    
                    # Add the latest time to the cache
                    latest.append(dt.datetime.now())
                    self.cache["guild"][ID]["latest"].insert(0, dt.datetime.now())
                    
                    return True, "You are not being ratelimited."
                
                else:
                    return False, "You are being ratelimited."

            case "user":
                # When the rate limit is user, it will be based on the user id
                cache = self.get_set(self.cache, "user")
                cache = self.get_set(cache, ID, {
                    "latest": [dt.datetime.now()]
                })

                # Get the latest {limit} time and check the count of the command
                latest = cache["latest"]

                # Check if the latest is >= limit
                latest = latest[0:min(limit, len(latest))]

                # Count the amount of times the command has been used
                count = len(latest)

                # Check if the first element in latest is within the timeout
                if (dt.datetime.now() - latest[0]).seconds <= timeout * 1000:
                    # Check if the count is >= limit
                    if count >= limit:
                        return False, "You are being ratelimited."
                    
                    # Add the latest time to the cache
                    latest.append(dt.datetime.now())
                    self.cache["user"][ID]["latest"].insert(0, dt.datetime.now())
                    
                    return True, "You are not being ratelimited."
                
                else:
                    return False, "You are being ratelimited."

            case "command" | _:
                # When the rate limit is command, it will be based on the command name in a guild
                cache = self.get_set(self.cache, "guild")
                cache = self.get_set(cache, ID)
                cache = self.get_set(cache, name, {
                    "latest": [dt.datetime.now()]
                })

                # Get the latest {limit} time and check the count of the command
                latest = cache["latest"]

                # Check if the latest is >= limit
                latest = latest[0:min(limit, len(latest))]

                # Count the amount of times the command has been used
                count = len(latest)

                # Check if the first last element is within the timeout
                if (dt.datetime.now() - latest[0]).seconds <= timeout * 1000:
                    # Check if the count is >= limit
                    if count >= limit:
                        return False, "You are being ratelimited."
                    
                    # Add the latest time to the cache
                    latest.append(dt.datetime.now())
                    self.cache["guild"][ID][name]["latest"].insert(0, dt.datetime.now())
                    
                    return True, "You are not being ratelimited."
                
                else:
                    return False, "You are being ratelimited."






