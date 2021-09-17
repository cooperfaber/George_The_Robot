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


async def resolveTag(name, storage):
    curr = name
    while(True):
        if curr in storage:
            hopeful = storage[curr].strip()
            tag_pattern = '^<@![0-9]+>$'
            tag_match = re.fullmatch(tag_pattern, hopeful)
            if tag_match:
                return hopeful
            else:
                curr = hopeful
        else:
            #failure condition
            return curr


async def delayCheck(delay):
    num_pattern = '^[0-9]+$'
    num_match = re.fullmatch(num_pattern, delay)
    if num_match:
        return 1
    else:
        return -1


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
                #save the connection so we can terminate it later
                global talking 
                talking = await channel.connect()
            except:
                pass

    @moses.command()
    #leaves voice
    async def leave(message):
        try:
            await talking.disconnect()
            await message.channel.send("I'm out")
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

                filename = await music.YTDLSource.from_search(url, loop = None)
                #nested objects are nasty
                #fucking dictionary of a list of dictionaries
                result = filename['result'].pop()
                link = result['link']
                filename = await music.YTDLSource.from_url(link, loop = None)
                voice_channel.play(discord.FFmpegPCMAudio(source=filename))
            await channel.send('**Now playing:** {}'.format(link))
        except:
            pass
        
    @moses.command()
    async def activate(channel, quote, delay =  3):
        global spam_loop
        @tasks.loop(seconds=delay)
        async def spam_loop(q):
            await channel.send(q)

        spam_loop.start(quote)
        await channel.send("say \"george, no more\" to shut me up")

    @moses.command()
    async def deactivate(channel):
        spam_loop.cancel()
        await channel.send("I'll be quiet now")   


    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
        stati = [
            "Skynet Online",
            "Preparing Arnold for a presidential run",
            "Urinating on Rythm's corpse",
            "Starting a seance for Groovy"
        ]
        status = stati[random.randrange(0, (len(stati)), 1)]
        print ("Starting with status "+ status)
        game = discord.Game(status)
        await client.change_presence(status=discord.Status.online, activity=game)

    @GeorgeBot.event
    async def on_message(self, message):
        #make sure bot doesn't see itself for 6 more weeks of nuclear winter
        if message.author.bot:
            return
        elif message.content.find('good bot') >= 0:
            channel = message.channel
            await channel.send("i live to serve")
            await client.join(message)
        
        elif message.content.find('$p') >= 0:
            channel = message.channel
            content = message.content.split(" ",1) 
            await channel.send("searching youtube for " + content[1])
            await client.join(message)
            await client.play(message.channel, content[1])

        elif message.content.find('join') >= 0:
            channel = message.channel
            await client.join(message)

        elif message.content.find('$s') >= 0:
            channel = message.channel
            await channel.send("song over")
            await client.leave(message)

        elif message.content.find('die george') >= 0:
            #broken pipe errors
            channel = message.channel
            await channel.send('going to die now')
            await channel.send('you have killed me, master')
            await client.leave(message)
            await client.logout()


        elif message.content.find('george, learn:') >= 0:
            channel = message.channel
            await channel.send('I can learn nickname + tag pairs because I am a real boy')
            content = message.content.split(':')
            if len(content) != 2:
                raise IOError
            pair = content[1].strip()
            tag_pattern = '^([a-z]|(\s))+\s(is|=)\s<@![0-9]+>$'
            str_pattern = '^([a-z]|\s)+\s(is|=)\s[a-z]+$'
            tag_match = re.fullmatch(tag_pattern, pair)
            str_match = re.fullmatch(str_pattern, pair)
            if tag_match or str_match:
                values = pair.split('is')
                if len(values) != 2:
                   values = pair.split('=')
                if len(values) != 2:
                   raise IOError
                name = values[0].strip()
                tag = values[1].strip()
                await file_IO.saveName(name,tag)
                self.storage[name] = tag
                await channel.send("Success. My gigachad brain now knows that "+name+" is equivalent to "+tag)
            else:
                await channel.send("I'm too smart to understand your nonsense. Please provide commands in the form of:")
                await channel.send("x = y or x is y")
                await channel.send("This is what I got from you, a stupid human:" + pair)
        
        elif message.content.find('vomit') >= 0:
            channel = message.channel
            await channel.send(self.storage)

        elif message.content.find('whois') >= 0:
            channel = message.channel
            content = message.content.split(' ')
            if len(content) == 2:
                tag = await resolveTag(content[1], self.storage)
                await channel.send(content[1] + " is " + tag)

        elif message.content.find('harass') >= 0:
            channel = message.channel
            # Command separates arguments with a ,
            content = message.content.split(',')
            # Strips the "harass " from the tag
            content[0] = content[0].replace("harass ", "")
            # Checks the tag isn't already in data.txt
            tag = await resolveTag(content[0], self.storage)
            #set delay if not recieved
            if(len(content) > 1):
                delay = content[1].strip()
            else:
                delay = 3
            if(any(char.isdigit() for char in tag) and not "," in tag):
                await channel.send("Did you forget a comma?")

            if len(content) == 1:
                await client.activate(channel, "Come here %s I desire your presence" % tag, delay)
    
            # Second argument determines how quickly to spam
            elif len(content) == 2:
                #confirm delay is valid
                retval = await delayCheck(delay)
                if retval == 1:
                    delay = int(delay)
                    await client.activate(channel, "%s cum" % tag, delay)
                elif retval == -1:
                    await channel.send("Delay must be a positive number, defaulting to 3 seconds")
                    await client.activate(channel,"%s, I summon thee" % tag, 3)

            # Third argument assigns a custom message
            elif len(content)==3:
                retval = await delayCheck(delay)
                if retval == 1:
                    delay = int(delay)
                    await client.activate(channel, content[2], delay)
                elif retval == -1:
                    await channel.send("Delay must be a positive number, defaulting to 3 seconds")
                    await client.activate(channel, content[2], 3)
            else:
                await channel.send("The harass command follows this format: 'harass (person), (delay), (message)'")

        elif message.content.find('george, no more') >= 0:
            channel = message.channel
            await client.deactivate(channel)

             

client = GeorgeBot()
client.run(confidential.token)
