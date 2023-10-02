import client
import discord

async def on_ready(self: client.Client):
    # Print a message to the console
    self.console.log('Logged in as [bold magenta]{}[/bold magenta]'.format(self.user))

    # Set the activity
    await self.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, 
        name='for prefix "s!"'
    ))

    await self.application_info()

    self.devs = [
        self.application.owner.id
    ]