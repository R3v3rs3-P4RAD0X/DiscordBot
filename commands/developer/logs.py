# File: Logs
# Description: Gets the latest log file and paginates it in the
#              chat.
# Author: StrangeParadox
# Version: 0.0.1

# Imports
import re
import os
from components import Command

class Logs(Command):
    """
    Gets the latest log file and paginates it in the
    chat.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class.
        Set the variables.
        """
        super().__init__(*args, **kwargs)

        self.dev = True

        # A pattern for matching text
        self.pattern = r'\w+'

    async def run(self):
        """
        Runs the command.
        """
        # Get the latest log file
        logs = self.client.console.get_logs()

        # Split the logs into pages
        pages = []

        # Split the logs into chunks of 700 characters or 10 lines
        items = []

        # Check if the bot can embed_links
        embeddable = self.bot_permissions.has("embed_links")

        # Split the logs into lines
        for i in range(0, len(logs), 10):
            if len(logs[i:i+7]) > 0:
                pages.append(logs[i:i+7])

        # Loop over the pages
        for i, page in enumerate(pages):
            page = [p.rstrip("\n").replace(os.getcwd() + "/", "") for p in page]

            if embeddable:
                items.append(self.create_embed(
                    title = f"Logs | Page: {i + 1}/{len(pages)}",
                    colour = (255, 255, 255),
                    description = "```\n" + "\n".join(page) + "```",
                    footer = {
                        "text": f"Powered by {self.message.guild.me.name}",
                        "icon_url": self.message.guild.me.avatar.url
                    }
                ))

            else:
                items.append("\n".join([
                    f"Logs | Page: {i + 1}/{len(pages)}",
                    "```",
                    "\n".join(page),
                    "```"
                ]))

        # Send the paginator
        await self.paginate(items)