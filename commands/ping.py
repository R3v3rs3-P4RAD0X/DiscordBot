from command import Command
import datetime

class Ping(Command):
    desc = "Pong!"
    aliases = ["pong"]

    async def run(self):
        # Check if the bot has permission to embed links
        if self.perms['bot'].embed_links:
            # Send an embed
            await self.SendEmbed(embed=self.embed(
                title="Pong! 🏓", 
                colour=(255, 255, 0)
            ))
            return
        
        # Send a message
        await self.SendMessage("Pong! 🏓")
        