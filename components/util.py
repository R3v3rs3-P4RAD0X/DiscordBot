# File: Util
# Description: A bunch of functions and constants for config/utility purposes.
# Author: StrangeParadox
# Version: 0.0.1

# Imports


class Util:
    """
    Static class with utility methods and constants.
    """

    @staticmethod
    def read_key_val_file(file: str) -> dict:
        """
        Reads a key-value file and returns a dictionary of the contents.

        :param file: The path of the file to read.
        :type file: str
        :return: A dictionary containing the key-value pairs from the file.
        :rtype: dict
        :raises ValueError: If the file contains an invalid line.
        """

        # Define the dictionary
        result = {}

        # Open the file
        with open(file, "r") as f:
            # Read the file
            lines = f.readlines()

            # Loop over the lines
            for line in lines:
                # Strip the line
                line = line.strip()

                # Check if the line is empty or a comment
                if line == "" or line.startswith("#"):
                    continue

                # Check if the line doesn't have a key
                if "=" not in line or line.startswith("="):
                    raise ValueError(f"Invalid line: {line}")
                
                # Split the line
                key, value = line.split("=", 1)

                # Strip the key and value
                key = key.strip()
                value = value.strip()

                # Check if the key is empty
                if key == "":
                    raise ValueError(f"Invalid line: {line}")
                
                # Add the key-value pair to the dictionary
                result[key] = value

        # Return the dictionary
        return result
    
    @staticmethod
    def write_key_val_file(data: dict, file: str) -> None:
        """
        Writes a key-value file from a dictionary.

        :param data: The dictionary to write.
        :type data: dict
        :param file: The path of the file to write.
        :type file: str
        """

        # Open the file
        with open(file, "w") as f:
            # Loop over the dictionary
            for key, value in data.items():
                # Write the key-value pair
                f.write(f"{key}={value}\n")

    @staticmethod
    def get_first_of_type(data: list, type: type) -> any:
        """
        Returns the first element of the specified type in a list.

        :param data: The list to search.
        :type data: list
        :param type: The type of element to search for.
        :type type: type
        :return: The first element of the specified type, or None if not found.
        :rtype: Any
        """

        # Loop over the list
        for item in data:
            # Check if the item is of the specified type
            if isinstance(item, type):
                return item
        
        # Return None
        return None
    
    @staticmethod
    def get_all_of_type(data: list, type: type) -> list:
        """
        Returns all elements of the specified type in a list.

        :param data: The list to search.
        :type data: list
        :param type: The type of element to search for.
        :type type: type
        :return: A list of all elements of the specified type.
        :rtype: list
        """

        # Define the list
        result = []

        # Loop over the list
        for item in data:
            # Check if the item is of the specified type
            if isinstance(item, type):
                result.append(item)
        
        # Return the list
        return result
