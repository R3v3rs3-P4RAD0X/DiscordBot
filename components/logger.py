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
        filepath = frame.f_code.co_filename
        filename = filepath.split("/")[-1]
        line = frame.f_lineno
        
        # Construct a filestr
        filestr = f"{filename}:{line}"

        # Get the console dimensions
        dimensions = self.console.size

        # Define the content to print
        content = f"{self.now()} {message}"

        spacing = dimensions.width - \
            (len(self.now()) + \
            len(filestr) + \
            len(self.clean(message))) -1

        # Log the message using the rich console
        rich.print(f"{content}{' ' * spacing}{filestr}")

        # Open the log file
        with open(self.file, "a+") as file:
            # Check if message is empty
            if len(message) == 0:
                file.write(f"{self.now()} ({filename}:{line}) Empty print.\n")
                return
            
            # Get the word chunks
            chunks = self.to_chunks(message)

            if len(chunks) == 0:
                file.write(f"{self.now()} ({filename}:{line}) Empty chunk.\n")
                return

            # Loop over the chunks
            for chunk in chunks:
                # Write the chunk to the file
                file.write(f"{self.now()} ({filestr}) {self.clean(chunk)}\n")
    
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