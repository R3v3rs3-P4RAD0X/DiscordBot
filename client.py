import discord

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.console = kwargs.get('console', None)
        self.config = kwargs.get('config', None)
        # self.database = kwargs.get('database', None)

        self.aliases = self.config.HandleCommandAliases()
