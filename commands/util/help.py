from command import Command
import importlib

class Help(Command):
    aliases = ["h"]
    desc = "Shows help for all commands"

    # The run function
    async def run(self):
        # We need to get all the files in the commands directory
        output = self.client.config.FindAll('.py', 'commands')

        # Get all the files as commands
        commands = [
            self.client.config.HandleCommand(
                file.split('.')[-1]
            )
            for file in output
        ]

        # Filter out the commands that don't exist
        commands = [
            command 
            for command in commands
            if command
        ]

        fields = []

        for cls in commands:
            # Create an instance of the command
            command = cls(
                self.message,
                self.args,
                self.client,
                self.guildConfig
            )

            # Check if the command is hidden
            if command.hidden:
                continue

            # Get the help information
            help = command.help()

            # Create a string for the value
            value = "\n".join([
                "Description: " + help['desc'],
                "Usage: " + help['usage'],
                f"{'NSFW ' if command.nsfw else ''}{'DISABLED' if command.disabled else ''}{'' if command.executable(self.perms['user']) else ' (Insufficient Permissions)'}",
            ])

            # Create a new field
            field = {
                "name": f"{help['name']} ({', '.join(help['aliases'])})",
                "value": value,
                "inline": False
            }

            # Add the field to the list
            fields.append(field)

        # Check if the bot has permission to embed links
        # if self.perms['bot'].embed_links:
        #     # Send an embed
        #     await self.SendEmbed(embed=self.embed(
        #         title="**Command Help**",
        #         colour=(255, 0, 255),
        #         thumbnail=self.client.user.avatar.url,
        #         fields=fields,
        #         author=self.message.guild.me.display_name,
        #         footer=f"Requested by {self.message.author.display_name}",
        #     ))
        #     return
        
        # Send a message
        await self.SendMessage(
            "".join([
                "__**Command Help**__\n",
                "```md\n",
                "\n".join([
                    f"> {field['name']}\n{field['value']}\n"
                    for field in fields
                ]),
                "```"
            ])
        )
