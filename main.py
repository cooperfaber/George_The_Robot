import discord
from discord.ext import commands
from discord.ext import tasks
import random
import confidential
import music
import time

random.seed(a=None, version=2)

class GeorgeBot(discord.Client):
    GeorgeBot = discord.Client()
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
        #try:
        server = channel.guild
        voice_channel = server.voice_client
        async with channel.typing():
            filename = await music.YTDLSource.from_url("https://www.youtube.com/watch?v=8mHKHKR8x6A", loop=None)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await channel.send('**Now playing:** {}'.format(filename))
        #except:
        #    pass




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
            



client = GeorgeBot()
client.run(confidential.token)