# from command import Command
# import re

# class Profile(Command):
#     usage = "profile [mention|id|name]"

#     async def run(self):
#         # Get the user
#         user = self.message.author

#         # Check if a user was mentioned
#         if len(self.message.mentions) > 0:
#             user = self.message.mentions[0]

#         # Check if an ID was provided
#         if len(self.args) > 0 and re.match(r'^\d{17,18}$', self.args[0]):
#             user = await self.client.fetch_user(int(self.args[0]))

#         # Get the user's data
#         data = self.client.database.get_user(user.id)

#         # Print the user's data
#         await self.message.channel.send(f"```json\n{data}```")