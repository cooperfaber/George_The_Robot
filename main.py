import discord
from discord.ext import commands
from discord.ext import tasks
import random
import confidential
import music
import re
import time
import file_IO

random.seed(a=None, version=2)

messageToBeSaved = "Nothing saved"


class GeorgeBot(discord.Client):
    GeorgeBot = discord.Client()
    storage = dict()
    #commands are moses, because of the 10 commdandments
    #no? biblical references aren't classy any more?
    moses = commands.Bot(command_prefix = '/')

    #command definition
    @moses.command()
    #joins voice, if message author is in channel
    async def join(message):
        if not message.author.voice:
            await message.channel.send("You aren't in a voice channel, schmuck")
        else:
            channel = message.author.voice.channel
            try:
                await channel.connect()
            except:
                pass

    @moses.command()
    #leaves voice
    async def leave(message):
        try:
            await message.voice_client.disconnect()
        except:
            pass

    @moses.command()
    #plays song
    async def play(channel, url):
        try:
            server = channel.guild
            voice_channel = server.voice_client
            #add something here to fix broken pipe
            async with channel.typing():
                filename = await music.YTDLSource.from_url("https://www.youtube.com/watch?v=8mHKHKR8x6A", loop=None)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename))
            await channel.send('**Now playing:** {}'.format(filename))
        except:
            pass
        
    @moses.command()
    #Save message
    async def save(message):
        messageToBeSaved = message

    @moses.command()
    #Repeat saved message
    async def load(message):
        message.channel.send(messageToBeSaved)



    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
        stati = [
            "Skynet Online",
            "Preparing Arnold for a presidential run"
        ]
        status = stati[random.randrange(0, (len(stati)), 1)]
        print ("Starting with status "+ status)
        game = discord.Game(status)
        await client.change_presence(status=discord.Status.online, activity=game)

    @GeorgeBot.event
    async def on_message(self, message):
        if message.content.find('good bot') >= 0:
            channel = message.channel
            await channel.send("i live to serve")
            await client.join(message)
        
        if message.content.find('voice test') >= 0:
            channel = message.channel
            await channel.send("i'm trying my robotic best")
            await client.join(message)
            await client.play(message.channel, message)

        if message.content.find('die george') >= 0:
            channel = message.channel
            await channel.send('going to die now')
            await channel.send('you have killed me, master')
            await client.leave(message)
            await client.logout()


        if message.content.find('george, learn:') >= 0:
            channel = message.channel
            await channel.send('I can learn nickname + tag pairs because I am a real boy')
            content = message.content.split(':')
            if len(content) != 2:
                raise IOError
            pair = content[1].strip()
            tag_pattern = '^[a-z]+\s(is|=)\s<@![0-9]+>$'
            str_pattern = '^[a-z]+\s(is|=)\s[a-z]+$'
            tag_match = re.fullmatch(tag_pattern, pair)
            str_match = re.fullmatch(str_pattern, pair)
            if tag_match or str_match:
                values = pair.split(' ')
                if len(values) != 3:
                   raise IOError
                name = values[0]
                tag = values[2]
                await file_IO.saveName(name,tag)
                self.storage[name] = tag
            else:
                await channel.send("I'm too smart to understand your nonsense. Please provide commands in the form of:")
                await channel.send("x = y or x is y")
                await channel.send("This is what I got from you, a stupid human:" + pair)
        
        if message.content.find('vomit') >= 0:
            channel = message.channel
            await channel.send(self.storage)
             

client = GeorgeBot()
client.run(confidential.token)