# File: Logger
# Description: Creates a file for all the logging along with printing
#              to the console.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import os
import datetime
import rich
import re
import inspect

class Logger:
    """
    Creates a file for all the logging along with printing
    to the console.
    """

    def __init__(self):
        """
        Initialize the class.
        Set the variables.
        """
        self.console = rich.get_console()
        self.pattern = r'\[[^\]]*\]'

        # Generate the current date and time in the format YYYY/MM/DD/HH-MM-SS.log
        self.file = datetime.datetime.now().strftime("logs/%Y/%m/%d/%H-%M-%S.log")
        os.makedirs(self.file.rsplit("/", 1)[0], exist_ok=True)

    def __del__(self):
        """
        Handles the deletion of the class.
        """
        pass

    def now(self):
        """
        Returns a formatted datetime object

        Format: [YYYY/MM/DD HH:MM:SS]
        """
        return datetime.datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
    
    def clean(self, line: str) -> str:
        """
        Removes any []content[/] from the line.
        """
        return re.sub(self.pattern, "", line)
        

    def log(self, message: str = "", **kwargs):
        """
        Writes to the file along with printing the error.

        Log format: [YYYY/MM/DD HH:MM:SS] (filename:line) message
        """
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename.replace(os.getcwd() + "/", "DiscordBot -> ")
        line = frame.f_lineno

        # Log the message using the rich console
        self.console.log(message, **kwargs)

        # Open the log file
        with open(self.file, "a+") as file:
            # Check if message is empty
            if len(message) == 0:
                file.write(f"{self.now()} ({filename}:{line})\n{self.now()} Empty print.\n\n")
                return
            
            # Get the word chunks
            chunks = self.to_chunks(message)

            if len(chunks) == 0:
                file.write(f"{self.now()} ({filename}:{line})\nEmpty chunk.\n\n")
                return

            # Write the filename and line number before the message
            file.write(f"{self.now()} ({filename}:{line})\n")

            # Loop over the chunks
            for chunk in chunks:
                # Write the chunk to the file
                file.write(f"{self.now()} {self.clean(chunk)}\n")
            
            file.write(f"\n")
    
    def print(self, *args, **kwargs):
        """
        Runs self.log
        """
        self.log(*args, **kwargs)

    def to_chunks(self, content: str) -> list[str]:
        """
        Converts the message content into chunks of 15 words.
        """
        # Split the content into words
        words = content.split()

        # Create a list to store the chunks
        chunks = []

        # Loop over the words
        for i in range(0, len(words), 15):
            # Append the chunk to the list
            chunks.append(" ".join(words[i:i+15]))

        # Return the chunks
        return chunks
    
    def get_logs(self) -> str:
        """
        Returns the file path.
        """
        return open(self.file).readlines()