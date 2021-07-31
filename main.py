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








    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
            stati = [
                "Skynet Online",
                "Preparing Arnold for a presidential run"
            ]
            num = stati[random.randrange(0, (len(stati) - 1), 1)]
            print ("Starting with status "+ num)
            game = discord.Game(num)
            await client.change_presence(status=discord.Status.online, activity=game)


client = GeorgeBot()
client.run(confidential.token)