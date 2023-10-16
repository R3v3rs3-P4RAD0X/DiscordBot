# File: On_Message
# Description: Handles the message event from the client.
# Author: StrangeParadox
# Version: 0.0.2

# Imports
import os
import sys
import discord
import traceback
from components import Client

async def on_message(self: Client, message: discord.Message):
    """
    Handles the message event from the client.
    """
    # Check if the message wasn't sent in a guild
    if message.channel.type != discord.ChannelType.text:
        # Return
        return
    
    # Check if the message was received from a bot
    if message.author.bot:
        # Return
        return
    
    # Get the prefix from the database
    prefix = self.env.get("PREFIX", "s!")

    # Check if the message doesn't start with the prefix
    if not message.content.startswith(prefix):
        # Return
        return
    
    # Get the command and args from the message
    command, *args = message.content.lstrip(prefix).strip().split()

    # Find the command using the command handler
    found = self.command_handler.find(command)

    # Check if the command was found
    if found:
        # Load the command
        command = self.command_handler.load(found, True if message.author.id == 472571500637978626 else False)

        # Initialize the command
        cmd = command["object"](message, args, self, {
            "ratelimiter": self.ratelimit
        })

        # Run the command
        try:
            returned = await cmd.execute()

            # Check if the instance of returned is a tuple
            if isinstance(returned, tuple):
                print(returned[0])
        
        except Exception as err:
            if message.guild.id == 741082079197921361 or message.author.id == 472571500637978626:
                # Traceback the error
                etype, evalue, e_trace = sys.exc_info()
                etrace = e_trace
      
                # Get the last traceback
                while etrace.tb_next != None:
                    etrace = etrace.tb_next

                # Get the traceback data
                line_number = etrace.tb_lineno
                file_name = etrace.tb_frame.f_code.co_filename.replace(os.getcwd(), "DiscordBot")
                error = str(evalue)
                full_error = "\n".join(traceback.format_tb(e_trace))

                # Check if I can send an embed
                if message.channel.permissions_for(message.guild.me).embed_links:
                    # Send the error message
                    await message.channel.send(
                        embed=discord.Embed(
                            title="Encountered an error.", 
                            description=f"Type: {etype.__name__}\n```py\nError: {error}\nFull Error: {full_error}\n```", 
                            color=discord.Color.red(),
                            timestamp=message.created_at,
                        )
                        .add_field(name="File", value=file_name)
                        .add_field(name="Line", value=line_number)
                        .set_author(name=message.guild.me.name, icon_url=message.guild.me.avatar.url)
                    )
                else:
                    # Send the error message
                    await message.channel.send("```py\n" + "\n".join([
                        f"Type: {etype.__name__}",
                        f"Error: {error}",
                        "\n"
                        f"File: {file_name}",
                        f"Line: {line_number}",
                    ]) + "```")
            
            self.console.log(f"Encountered an error running command: {command['name']}\nFile: {file_name}\nLine: {line_number}\nError: {error}\nFull Error: {full_error}")

    


