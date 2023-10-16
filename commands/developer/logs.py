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

        def split_logs(logs):
            subgroups = [[]]

            for log in logs:
                stripped_log = log.strip()  # Strip leading and trailing whitespace
                print(stripped_log, len(stripped_log))
                if stripped_log:
                    subgroups[-1].append(log.rstrip("\n"))

                if not stripped_log and subgroups[-1]:
                    subgroups.append([])

            # Remove any empty subgroups
            subgroups = [subgroup for subgroup in subgroups if subgroup]

            return subgroups

        subgroups = split_logs(logs)

        # Now 'subgroups' contains lists of logs grouped by non-empty lines
        # We need to split each subgroup into pages
        # A page will be a total of 10 lines, if the 10th line isn't the last element of the subgroup skip that subgroup until the next one
        for subgroup in subgroups:
            # Split the subgroup into pages
            pages.extend([subgroup[i:i+10] for i in range(0, len(subgroup), 10)])

        # Group pages by 5 pages
        pages = [pages[i:i+5] for i in range(0, len(pages), 10)]

        # Create a list of items
        items = []

        # Bot permissions has embed links
        embed = self.bot_permissions.has("embed_links")

        # Loop through the pages
        for i, page in enumerate(pages):
            for j, p in enumerate(page):
                page[j] = "\n".join(p)

            # If embeddable create an embed
            if embed:
                items.append(self.create_embed(
                    title = f"Logs | Page {i+1}/{len(pages)}",
                    description = "\n".join(["```", "\n".join(p for p in page), "```"]),
                    colour = (255, 255, 255),
                    footer = {
                        "text": "Use the buttons to navigate through the pages."
                    },
                    author = {
                        "name": self.message.guild.me.name,
                        "icon_url": self.message.guild.me.avatar.url
                    }
                ))

            else:
                # Create a string
                items.append("\n".join([
                    f"Page {i+1}/{len(pages)}",
                    "```",
                    "\n".join(page),
                    "```"
                ]))
        
        # # Send the embeds
        await self.paginate(items)