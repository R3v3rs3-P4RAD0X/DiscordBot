from command import Command

class Ping(Command):
    async def run(self):
        # Send a message to the channel
        await self.message.channel.send('Pong!')