from command import Command
import importlib

class Help(Command):
    aliases = ["h"]
    dev = True

    # The run function
    async def run(self):
        # We need to get all the files in the commands directory
        output = self.client.config.WalkDirectory('commands', '.py')

        # Loop through the output
        for file in output:
            print(file)

            # Work In Progess
