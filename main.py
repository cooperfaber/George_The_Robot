import discord
from discord.ext import commands
from discord.ext import tasks
import random
import confidential
import time

random.seed(a=None, version=2)

class GeorgeBot(discord.Client):
    GeorgeBot = discord.Client()
    #commands are moses, because of the 10 commdandments
    #no? biblical references aren't classy any more?
    moses = commands.Bot(command_prefix = '/')

    #command definition
    @moses.command()
    async def join(ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @moses.command()
    async def leave(ctx):
        await ctx.voice_client.disconnect()






    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
            stati = [
                "Skynet Online",
                "Preparing Arnold for a presidential run"
            ]
            status = stati[random.randrange(0, (len(stati) - 1), 1)]
            print ("Starting with status "+ status)
            game = discord.Game(status)
            await client.change_presence(status=discord.Status.online, activity=game)

    @GeorgeBot.event
    async def on_message(self, message):
        if message.content.find('good bot') >= 0:
            channel = message.channel
            await channel.send("i live to serve")
            await client.join(message)



client = GeorgeBot()
client.run(confidential.token)