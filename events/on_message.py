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

            # Check if the command is an alias
            if command in self.aliases:
                # Set the command to the alias
                command = self.aliases[command]

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