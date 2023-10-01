import discord

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.console = kwargs.get('console', None)
        self.config = kwargs.get('config', None)
        self.database = kwargs.get('database', None)

    # Overwrite the on_ready method
    async def on_ready(self):
        # Print a message to the console
        self.console.print('Logged in as [bold red]{}[/bold red]'.format(self.user))

        # Set the activity
        await self.change_presence(activity=discord.Game('Hello World!'))

    # Overwrite the on_message method
    async def on_message(self, message):
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
                command, *args = message.content[len(config['prefix']):].split(' ')

                if Command := self.config.HandleCommand(command):
                    command = Command(message, args, self)

                    # Check if the command has a run method
                    if run := getattr(command, 'run', False):
                        # Check if the run function is callable
                        if callable(run):
                            # Run the command
                            await run()
                