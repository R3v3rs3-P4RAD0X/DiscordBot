# File: Permissions
# Description: a permissions handler with functions to help comparing and returning
#              missing permissions from another instance.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import discord

class Permissions:
    """
    A class that represents Discord permissions as a bitfield and provides methods to compare and manipulate them.

    Attributes:
    - VALUE (int): The bitfield value of the permissions.
    - FLAGS (dict): A dictionary of all valid permission flags and their corresponding bit values.
    - INVERSE_FLAGS (dict): A dictionary of all valid permission bit values and their corresponding flag names.
    - TOTAL (int): The maximum value of the bitfield.
    - ISSET (list[dict[str, any]]): A list of dictionaries representing the set permissions, with keys 'name', 'value', and 'log2'.

    Methods:
    - __init__(self, bitfield: int): Initializes the Permissions class with a bitfield.
    - __gt__(self, other: 'Permissions'): Checks if self has more permissions than other.
    - __lt__(self, other: 'Permissions'): Checks if self has less permissions than other.
    - __eq__(self, other: 'Permissions'): Checks if self has the same permissions as other.
    - __ge__(self, other: 'Permissions'): Checks if self has more or the same permissions as other.
    - __le__(self, other: 'Permissions'): Checks if self has less or the same permissions as other.
    - __ne__(self, other: 'Permissions'): Checks if self has different permissions to other.
    - __str__(self): Returns the permissions as a binary string.
    - __repr__(self): Returns the permissions as a binary string.
    - __int__(self): Returns the permissions as an integer.
    - __and__(self, other: 'Permissions'): Returns the permissions as a boolean.
    - __copy__(self): Returns a copy of the instance.
    - missing(self, other: 'Permissions') -> list[dict[str, any]]: Returns a list of missing permissions from other.
    """

    VALUE: int = None
    FLAGS = discord.Permissions.VALID_FLAGS
    INVERSE_FLAGS = {v: k for k, v in FLAGS.items()}
    TOTAL = 1 << 1 | sum(1 << x for x in range(2, 47))
    ISSET: list[dict[str, any]] = None

    
    def __init__(self, bitfield: int, *args: str):
        """
        Initialises the Permissions class with a bitfield.
        """
        
        if type(bitfield) == int:
            # Check if the bitfield is within the valid range
            if bitfield < 0 or bitfield > self.TOTAL:
                raise ValueError(f"Invalid bitfield: {bitfield}")
            
            self.VALUE = bitfield
        else:
            for arg in args:
                if arg not in self.FLAGS:
                    raise ValueError(f"Invalid flag: {arg}")
                
                if self.VALUE == None:
                    self.VALUE = self.FLAGS[arg]

                else:
                    self.VALUE |= self.FLAGS[arg]

        # Default the ISSET list to an empty list
        self.ISSET = []

        # Get the min value set in the bitfield
        self.LOWEST_SET = len(bin(self.VALUE)[2:]) - len(bin(self.VALUE)[2:].rstrip("0"))

        # Get the max value set in the bitfield
        self.HIGHEST_SET = len(bin(self.VALUE)[2:]) -1

        # Check which permissions are set
        for i in range(self.LOWEST_SET, self.HIGHEST_SET + 1):
            if (self.VALUE & (1 << i)) == 1 << i:
                self.ISSET.append(dict(name=self.INVERSE_FLAGS[1 << i], value=1 << i, log2=i))
                

    def __gt__(self, other: 'Permissions'):
        """
        Checks if self has more permissions than other.
        """

        return self.VALUE & ~other.VALUE
    
    def __lt__(self, other: 'Permissions'):
        """
        Checks if self has less permissions than other.
        """

        return other.VALUE & ~self.VALUE
    
    def __eq__(self, other: 'Permissions'):
        """
        Checks if self has the same permissions as other.
        """

        return self.VALUE == other.VALUE
    
    def __ge__(self, other: 'Permissions'):
        """
        Checks if self has more or the same permissions as other.
        """

        return self.VALUE & other.VALUE == self.VALUE
    
    def __le__(self, other: 'Permissions'):
        """
        Checks if self has less or the same permissions as other.
        """

        return other.VALUE & self.VALUE == other.VALUE
    
    def __ne__(self, other: 'Permissions'):
        """
        Checks if self has different permissions to other.
        """

        return self.VALUE != other.VALUE
    
    def __str__(self):
        """
        Returns the permissions as a binary string.
        """

        return bin(self.VALUE)[2:]
    
    def __repr__(self):
        """
        Returns the permissions as a binary string.
        """

        return bin(self.VALUE)[2:]
    
    def __int__(self):
        """
        Returns the permissions as an integer.
        """

        return self.VALUE
    
    def __and__(self, other: 'Permissions'):
        """
        Returns the permissions as a boolean.
        """

        return self.VALUE & other.VALUE
    
    def __copy__(self):
        """
        Returns a copy of the instance.
        """

        return Permissions(self.VALUE)
    
    def missing(self, other: 'Permissions') -> list[dict[str, any]]:
        """
        Returns a list of missing permissions from other.
        """

        return [x for x in self.ISSET if x not in other.ISSET]

    def has(self, permission: str) -> bool:
        """
        Checks if the permission is set.
        """

        if permission not in self.FLAGS:
            raise ValueError(f"Invalid flag: {permission}")

        return self.VALUE & self.FLAGS[permission] == self.FLAGS[permission]
    
    def has_all(self, *permissions: str) -> bool:
        """
        Checks if all permissions are set.
        """

        for permission in permissions:
            if permission not in self.FLAGS:
                raise ValueError(f"Invalid flag: {permission}")

            if self.VALUE & self.FLAGS[permission] != self.FLAGS[permission]:
                return False
        
        return True
    

if __name__ == '__main__':
    p1 = Permissions(1 << 10 | 1 << 11 | 1 << 12)

    print(p1.LOWEST_SET, p1.HIGHEST_SET)