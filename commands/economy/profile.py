from command import Command
import re


class Profile(Command):
    usage = "profile [mention|id]"

    async def run(self):
        # Get the user
        user = self.message.author

        # Check if a user was mentioned
        if len(self.message.mentions) > 0:
            user = self.message.mentions[0]

        # Check if an ID was provided
        if len(self.args) > 0 and re.match(r"^\d{17,18}$", self.args[0]):
            user = await self.client.fetch_user(int(self.args[0]))

        # Get the user's data
        userData = self.client.database.GetUser(user.id)

        # Get the user's profile
        profile = userData.economy

        # Check if the bot can embed links
        if self.perms["bot"].embed_links:
            thumbnail = user.avatar.url if user.avatar else user.default_avatar.url

            await self.SendEmbed(
                self.embed(
                    title=f"{user.name}'s Profile",
                    description=f"**Balance:** £{profile.balance}\n**Bank:** £{profile.bank}\n**Total:** £{profile.balance + profile.bank}",
                    colour=(255, 0, 255),
                    thumbnail=thumbnail,
                    footer=f"Requested by {self.message.author.name}",
                    author=self.client.user.name,
                )
            )

        # Otherwise, send a normal message
        else:
            await self.SendMessage(
                f"**{user.name}'s Profile**\n**Balance:** £{profile.balance}\n**Bank:** £{profile.bank}\n**Total:** £{profile.balance + profile.bank}"
            )
