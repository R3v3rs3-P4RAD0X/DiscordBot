from command import Command


class Purge(Command):
    usage = "purge <amount>"

    async def run(self):
        # Check if the user has manage_messages permission
        if not self.perms['user'].manage_messages:
            resp = await self.SendMessage("You don't have permission to purge messages!")
            await resp.delete(delay=5)
            return
        
        # Check if the bot has manage_messages permission
        if not self.perms['bot'].manage_messages:
            resp = await self.SendMessage("I don't have permission to purge messages!")
            await resp.delete(delay=5)
            return
        
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
        
