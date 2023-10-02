import client
import discord

async def on_message(self: client.Client, message: discord.Message):
    # If the message is from a bot, ignore it
    if message.author.bot:
        return
    
    # Check if the message was sent in a guild
    if message.guild:
        # Using self.config, get the config for the guild
        config = self.database.get_guild(message.guild.id)

        # Check if the message starts with the prefix
        if message.content.startswith(config['prefix']):
            # Get the command and arguments
            command, *args = message.content[len(config['prefix']):].strip().split(' ')

            # Lowercase the command
            command = command.lower()

            # Check if the command is an alias
            if command in self.aliases:
                # Set the command to the alias
                command = self.aliases[command]

            # Get a set of all the commands from the aliases
            commands = set(self.aliases.values())
            
            # Loop through the commands if command not in commands
            if command not in commands:
                for cmd in commands:
                    # Using the similar function check if the command is similar
                    if (per := self.config.Similar(cmd, command)) >= 70:
                        # Set the command to the similar command
                        command = cmd

                        # Check if the bot can send a message
                        if message.channel.permissions_for(message.guild.me).send_messages and per <= 75:
                            # Send a message
                            resp = await message.channel.send(f'> Selected command: **{command.title()}** as similarity match of {per}%')

                            # Delete the message after 5 seconds
                            await resp.delete(delay=5)

                        # Break out of the loop
                        break


            if Command := self.config.HandleCommand(command):
                command = Command(message, args, self, config)

                # Check if the command has a run method
                if run := getattr(command, 'run', False):
                    # Check if the run function is callable
                    if callable(run):
                        # Get member permissions
                        member_permissions = message.channel.permissions_for(message.author)

                        # Get the bot's permissions
                        bot_permissions = message.channel.permissions_for(message.guild.me)

                        # Check if the member and the bot has the required permissions
                        if command.executable(member_permissions) and command.executable(bot_permissions):
                            try:
                                # Run the command
                                await run()

                            except NotImplementedError as ni:
                                # Log the error in format Command: Error
                                self.console.log(f'{command.__class__.__name__}: [red]{ni}[/red]')