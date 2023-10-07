from command import Command
import importlib


class Help(Command):
    aliases = ["h"]
    desc = "Shows help for all commands"
    usage = "help [command]"

    # The run function
    async def run(self):
        # We need to get all the files in the commands directory
        output = self.client.config.FindAll(".py", "commands")

        # Get all the files as commands
        commands = [
            self.client.config.HandleCommand(file.split(".")[-1]) for file in output
        ]

        # Filter out the commands that don't exist
        commands = [command for command in commands if command]

        fields = []

        for cls in commands:
            # Create an instance of the command
            command = cls(self.message, self.args, self.client, self.guildConfig)

            # Check if the command is hidden
            if command.hidden:
                continue

            # Get the help information
            help = command.help()

            # Create a string for the value
            value = "\n".join(
                [
                    "Description: " + help["desc"],
                    "Usage: " + help["usage"],
                    "Aliases: " + ", ".join(help["aliases"]),
                    f"{'NSFW ' if command.nsfw else ''}{'DISABLED' if command.disabled else ''}{'' if command.executable(self.perms['user']) else ' (Insufficient Permissions)'}",
                ]
            )

            # Create a new field
            field = {"name": f"{help['name']}", "value": value, "inline": False}

            # Add the field to the list
            fields.append(field)

        # Send a message
        await self.SendMessage(
            "".join(
                [
                    "__**Command Help**__\n",
                    "```md\n",
                    "\n".join(
                        [f"> {field['name']}\n{field['value']}\n" for field in fields]
                    ),
                    "\n",
                    "<> = Required\n",
                    "[] = Optional\n",
                    "For command specfic help, use `help [command]` disabled\n" "```",
                ]
            )
        )
