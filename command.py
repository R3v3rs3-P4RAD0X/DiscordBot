import discord
import client

class Command:
    # Help information
    desc = "No description provided."
    usage = None
    aliases = []

    # Toggles
    dev = False
    nsfw = False
    hidden = False
    disabled = False

    # Permissions
    perms = {
        "required": discord.Permissions(1 << 10 | 1 << 11)
    } 

    def __init__(self, message: discord.Message, args: [str], client: client.Client, guildConfig):
        self.message = message
        self.args = args
        self.client = client
        self.guildConfig = guildConfig

        self.perms['bot'] = self.message.channel.permissions_for(self.message.guild.me)
        self.perms["user"] = self.message.channel.permissions_for(self.message.author)


    def executable(self, other: discord.Permissions):
        if self.dev and self.message.author.id not in self.client.devs:
            return False
        
        if self.nsfw and not self.message.channel.is_nsfw():
            return False
        
        if self.disabled:
            return False
        
        return other > self.perms['required']
    
    # A function for return help information
    def help(self):
        name = self.__class__.__name__
        usage = self.guildConfig['prefix'] + (self.usage if self.usage else name)

        return {
            "name": name,
            "desc": self.desc,
            "usage": usage,
            "aliases": self.aliases
        }

    # A function for handling the sending of a message
    async def SendMessage(self, message):
        # Send the message
        await self.message.channel.send(message)

    async def SendEmbed(self, embed):
        # Send the embed
        await self.message.channel.send(embed=embed)

    # A default run method
    async def run(self):
        # Throw NotImplementedError
        raise NotImplementedError('run method not implemented')
    
    # A function for constructing an embed
    def embed(self, **kwargs):
        # Create the embed
        embed = discord.Embed()

        # Check kwargs for each field
        if 'title' in kwargs:
            # Ensure the title is a string
            if not isinstance(kwargs['title'], str):
                raise TypeError('title must be a string')
            
            # Set the title
            embed.title = kwargs['title']

        if 'description' in kwargs:
            # Ensure the description is a string
            if not isinstance(kwargs['description'], str):
                raise TypeError('description must be a string')
            
            # Set the description
            embed.description = kwargs['description']

        if 'colour' in kwargs:
            # Colour must be rgb in a tuple
            if not isinstance(kwargs['colour'], tuple):
                raise TypeError('colour must be a tuple')
            
            # Ensure the tuple has 3 items
            if len(kwargs['colour']) != 3:
                raise ValueError('colour must have 3 items')
            
            # Ensure the items are integers
            for item in kwargs['colour']:
                if not isinstance(item, int):
                    raise TypeError('colour items must be integers')
                
                # Ensure the integers are between 0 and 255
                if item < 0 or item > 255:
                    raise ValueError('colour items must be between 0 and 255')
                
            # Set the colour
            embed.colour = discord.Colour.from_rgb(kwargs['colour'][0], kwargs['colour'][1], kwargs['colour'][2])

        if 'url' in kwargs:
            # Ensure the url is a string
            if not isinstance(kwargs['url'], str):
                raise TypeError('url must be a string')
            
            # Set the url
            embed.url = kwargs['url']

        if 'author' in kwargs:
            # Ensure the author is a string
            if not isinstance(kwargs['author'], str):
                raise TypeError('author must be a string')
            
            # Set the author
            embed.set_author(name=kwargs['author'])

        if 'thumbnail' in kwargs:
            # Ensure the thumbnail is a string
            if not isinstance(kwargs['thumbnail'], str):
                raise TypeError('thumbnail must be a string')
            
            # Set the thumbnail
            embed.set_thumbnail(url=kwargs['thumbnail'])

        if 'image' in kwargs:
            # Ensure the image is a string
            if not isinstance(kwargs['image'], str):
                raise TypeError('image must be a string')
            
            # Set the image
            embed.set_image(url=kwargs['image'])

        if 'footer' in kwargs:
            # Ensure the footer is a string
            if not isinstance(kwargs['footer'], str):
                raise TypeError('footer must be a string')
            
            # Set the footer
            embed.set_footer(text=kwargs['footer'])

        if 'fields' in kwargs:
            # Ensure the fields are a list
            if not isinstance(kwargs['fields'], list):
                raise TypeError('fields must be a list')
            
            # Ensure the fields are a list of dicts
            for field in kwargs['fields']:
                if not isinstance(field, dict):
                    raise TypeError('fields must be a list of dicts')
            
            # Add the fields
            for field in kwargs['fields']:
                # Ensure the field has a name
                if 'name' not in field:
                    raise ValueError('fields must have a name')
                
                # Ensure the name is a string
                if not isinstance(field['name'], str):
                    raise TypeError('field name must be a string')
                
                # Ensure the field has a value
                if 'value' not in field:
                    raise ValueError('fields must have a value')
                
                # Ensure the value is a string
                if not isinstance(field['value'], str):
                    raise TypeError('field value must be a string')
                
                # Ensure the field has an inline value
                if 'inline' not in field:
                    kwargs['inline'] = False

                # Ensure the inline value is a boolean
                if not isinstance(field['inline'], bool):
                    raise TypeError('field inline value must be a boolean')
                
                # Add the field
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        # Return the embed
        return embed