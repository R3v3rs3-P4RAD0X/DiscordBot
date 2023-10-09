from command import Command
import json


class Help(Command):
    aliases = ["h"]
    desc = "Shows help for all commands"
    usage = "help [command]"

    # The run function
    async def run(self):
        # We need to get all the files in the commands directory
        output = self.client.config.FindAll(".py", "commands")

        # Categories
        CommandCategories = {}

        # Loop through the files
        for file in output:
            # Get the command
            command = self.client.config.HandleCommand(file.split(".")[-1])(
                self.message, 
                self.args, 
                self.client, 
                self.guildConfig
            )

            # Check if the command exists
            if not command:
                continue

            # Check if the command is hidden
            if command.hidden:
                continue

            # Get the help information
            help = command.help()

            # Get the category from the file path, remove commands. and see if there is any other categories  # noqa: E501
            *categories, name = file.split(".")

            if len(categories) > 1:
                # Remove the commands folder
                categories.pop(0)

                # Join the categories
                category = " ".join(categories)

                # Check if the category exists
                if category not in CommandCategories:
                    CommandCategories[category] = []

                # Add the command to the category
                CommandCategories[category].append(help)

            else:
                # Check if the category exists
                if 'General' not in CommandCategories:
                    CommandCategories['General'] = []

                # Add the command to the category
                CommandCategories['General'].append(help)

        description = []

        # Loop through the categories
        for category, commands in CommandCategories.items():
            # Add the category to the description
            descDict = {
                "name": category.title(),
                "value": []
            }

            # Loop through the commands
            for command in commands:
                # Add the command to the description
                descDict['value'].append(f"{command['name']} - {command['usage']}")
            
            descDict['value'].append('')

            # Join the value by a new line
            descDict['value'] = '\n'.join(descDict['value'])

            # Add a new line
            description.append(descDict)

        # Check if the bot can embed_links
        if self.perms['bot'].embed_links:
            # Construct the embed
            embed = self.embed(
                title="__**Help**__",
                fields = description,
                colour=(255, 0, 255),
                footer=f"Requested by {self.message.author.name}",
                author=self.client.user.name,
            )

            # Send the embed
            await self.SendEmbed(embed)

            return
        
        # Otherwise send a normal message
        # Reformat the description
        description = '\n'.join([f"**{category['name']}**\n{category['value']}" for category in description])

        # Send the message
        await self.SendMessage(f"__**Help**__\n{description}")