from command import Command
import discord
import math

class Eval(Command):
    dev = True
    hidden = True

    async def run(self):
        # Check if args isn't empty
        if len(self.args) > 0:
            # Join args into a big string
            code = " ".join(self.args)

            field1 = discord.Permissions(1 << 10 | 1 << 11 | 1 << 12 | 1 << 13)
            field2 = self.perms['bot']            

            # Evaluate the code
            try:
                result = eval(code)

                # Send the result
                await self.message.channel.send(f"```py\nInput: {code}\n\nResult: {result}```")
            except Exception as e:
                # Send the error
                await self.message.channel.send(f"```py\nInput: {code}\n\nError: {e}```")