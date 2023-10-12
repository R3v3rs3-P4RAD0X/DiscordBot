from command import Command
import discord

class Purge(Command):
    usage = "purge <amount>"

    perms = {
        'required': discord.Permissions(1 << 10 | 1 << 11 | 1 << 13),
    }

    async def run(self):
        # Check if args length is >= 1
        if len(self.args) >= 1:
            # Get the amount to purge
            amount = self.client.config.FilterFirstType(self.args, int, lambda x: x > 0)

            # Check if the amount is None or False
            if amount is None or amount is False:
                amount = 25

            # Check if the amount is greater than 100
            if amount > 100:
                amount = 100

        # If amount is None or False
        else:
            amount = 25

        # Purge the messages
        await self.message.channel.purge(limit=amount)

        # Send a message
        resp = await self.SendMessage(f"Purged {amount} messages!")

        # Delete the message after 5 seconds
        await resp.delete(delay=5)
        
