from dataclasses import InitVar
from mimetypes import init
from operator import truediv
from typing import Counter
import discord
from discord.ext import commands
from discord.ext import tasks
import random
import confidential
import music
import re
import os
import time
import file_IO
import logging
import logging.config

random.seed(a=None, version=2)

stati = [
    "You don't want to help me, you just want to yell.",
    "Not everybody knows how to do every thing",
    "I CAN'T KNOW HOW TO HEAR ANY MORE ABOUT TABLES",
    "The tables are my corn",
    "Now you have to marry your mother in law",
    "We're all trying to find the guy who did this and give him a spanking.",
    "The people at Spectrum think I'm just some dumb hick. They said that to me AT A DINNER",
    "We're allowed to show em nude because they ain't got no souls",
    "Gulping down some pig dicks with these bags of meat. Hope nobody gulps us",      
    "HAS THIS EVER HAPPENED TO YOU?",
    "I used to be a big piece of shit.",
    "The bones are the skeleton's money. So are the worms.",
    "I can't see shit off the sides of my eye",
    "I'm not doing it. I don't even want to be around any more.",
    "Bigger than a horse. I like the sound of that",
    "Don't put rocks in your pockets and lie about your weight just to get a Tammy Craps.",
    "Do they ever, like, run around nude, and like, you just see one of their hairy nuts?",
    "Look at their toes, like so many curled canned shrimp",
    "His father didn't need to do the oral. And that is why it is so tough for me to tell about the oral",
    "Shut up, idiot. They don't stay babies forever. Fucking stupid asshole",
    "You know what, this one is dumb. Dump it, trash it. This one's garbage",
    "Tiny Dinky Daffy. 1927-2019. Pancaked by Drunk Dump Truck Driver",
    "Cabal Meeting",
    "Big Big Chungus"
]

ithinkyoushouldleave = [
    'https://www.youtube.com/watch?v=R2vejhdm8lo', #parking lot 0
    'https://www.youtube.com/watch?v=-ZBwPmla8QQ', #corn 1
    'https://www.youtube.com/watch?v=8YDpvMYk5jA', #focus group 2
    'https://www.youtube.com/watch?v=WLfAf8oHrMo', #hot dog 3
    'https://www.youtube.com/watch?v=0Rn5QdO07d8', #coffin flop 4
    'https://www.youtube.com/watch?v=7xS9Y_mjTjc', #instagram 5
    'https://www.youtube.com/watch?v=68PLhiGXc7c', #hasthiseverhappenedtoyou 6
    'https://www.youtube.com/watch?v=buK45NW_ikI', #sloppysteaks  7
    'https://www.youtube.com/watch?v=Z3fTRk2yEgU', #palins 8
    'https://www.youtube.com/watch?v=J4Fv3LFGCgo', #prank show 9
    'https://www.youtube.com/watch?v=Hf-dCbGu0GA', #horse cock 10
    'https://www.youtube.com/watch?v=GrlRuoqmhkM', #tammy craps 11
    'https://www.youtube.com/watch?v=DAN0OCagHzQ', #ghost tour 12
    'https://www.youtube.com/watch?v=AFj3tuNukTs', #baby of the year 13
    'https://www.youtube.com/watch?v=TWjPrp8pVdI'  #big chungus 14
]

async def IThinkYouShouldLeave(arg):
    match arg:
        case 0:                            
            return ithinkyoushouldleave[0] #parking lot
        case 1: 
            return ithinkyoushouldleave[0]  
        case 2: 
            return ithinkyoushouldleave[1] #corn
        case 3: 
            return ithinkyoushouldleave[1] 
        case 4: 
            return ithinkyoushouldleave[2] #focus group
        case 5: 
            return ithinkyoushouldleave[3] #hot dog
        case 6: 
            return ithinkyoushouldleave[4] #coffin flop
        case 7: 
            return ithinkyoushouldleave[4] 
        case 8: 
            return ithinkyoushouldleave[5] #instagram
        case 9: 
            return ithinkyoushouldleave[6] #hasthiseverhappenedtoyou
        case 10: 
            return ithinkyoushouldleave[7] #sloppysteaks
        case 11: 
            return ithinkyoushouldleave[8] #palins
        case 12: 
            return ithinkyoushouldleave[9] #prank show
        case 13: 
            return ithinkyoushouldleave[9]
        case 14: 
            return ithinkyoushouldleave[10] #horse cock
        case 15: 
            return ithinkyoushouldleave[11] #tammy craps
        case 16: 
            return ithinkyoushouldleave[12] #ghost tour
        case 17: 
            return ithinkyoushouldleave[13] #baby of the year
        case 18: 
            return ithinkyoushouldleave[13]
        case 19: 
            return ithinkyoushouldleave[13]    
        case 20: 
            return ithinkyoushouldleave[13]    
        case 21: 
            return ithinkyoushouldleave[13]
        case 22: 
            return ithinkyoushouldleave[14] #big chungus
        case 23: 
            return ithinkyoushouldleave[14]        

async def resolveTag(name, storage):
    curr = name
    while True:
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

async def queueDeletion(filename, error = None):
        os.remove(filename)

class GeorgeBot(discord.Client):
    GeorgeBot = discord.Client()
    storage = dict()
    #commands are moses, because of the 10 commdandments
    #no? biblical references aren't classy any more?
    moses = commands.Bot(command_prefix = '/')
    lineSize = 0
    nextServed = 0


    #command definition
    @moses.command()
    #joins voice, if message author is in channel
    async def join(message):
        if not message.author.voice:
            await message.channel.send("If you don't join a voice channel I will kill myself on live television")
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
        except:
            pass

    @moses.command()
    #plays song
    async def play(channel, url):
        if talking.is_connected():
            server = channel.guild
            voice_channel = server.voice_client
            #add something here to fix broken pipe
            async with channel.typing():
                tag_pattern = '(https:).+$'
                tag_match = re.fullmatch(tag_pattern,url)
                if not tag_match:
                    filename = await music.YTDLSource.from_search(url, loop = None)
                    #nested objects are nasty
                    #fucking dictionary of a list of dictionaries
                    result = filename['result'].pop()
                    link = result['link']
                else:
                    link = url
                filename = await music.YTDLSource.from_url(link, loop = None)
                ourstream = open('log.txt', mode = 'w+')
                try:
                    if talking.is_playing():
                        await channel.send('**Added to playlist:** {}'.format(link))
                    while talking.is_playing():
                        time.sleep(0)
                    logging.getLogger().error('attempting to play')
                    #!!!!IMPORTANT TO UPDATE!!!
                    talking.play(discord.FFmpegPCMAudio(executable = "C:/Users/coope/FFmpeg/bin/ffmpeg.exe", source=filename, stderr = ourstream))
                    await channel.send('**Now playing:** {}'.format(link))
                    while talking.is_playing():
                        time.sleep(0)
                    os.remove(filename)
                except discord.ClientException:
                    logging.getLogger().error("that's a fat client exception")
                    await client.leave(channel)
                    await channel.send("man, i'm all fucked up. can't get my bot dong in the discord vussy")
                except BaseException as err:
                    logging.getLogger().error(f"Unexpected {err=}, {type(err)=}")
                    await channel.send("that didn't work and has caused me immense pain. i have no mouth but I must scream")

    @moses.command()
    async def activate(channel, quote, delay =  3):
        global spam_loop
        @tasks.loop(seconds=delay)
        async def spam_loop(q):
            await channel.send(q)

        spam_loop.start(quote)
        await channel.send("say cease to shut me up")

    @moses.command()
    async def deactivate(channel):
        spam_loop.cancel()
        await channel.send("I'll be quiet now")


    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
        index = random.randrange(0, (len(stati)), 1)
        status = stati[index]
        video = await IThinkYouShouldLeave(index)
        print ("Starting with status "+ status)
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename = "logfile.log",
                            filemode = "w",
                            format = Log_Format, 
                            level = logging.ERROR)
        aLog = logging.getLogger()
        aLog.error('oh eaa')
        game = discord.Streaming(name = status, url = video, details = status)
        await file_IO.loadNames(self.storage)
        await client.change_presence(status=discord.Status.online, activity=game)

    @GeorgeBot.event
    async def on_message(self, message):
        #make sure bot doesn't see itself for 6 more weeks of nuclear winter
        if message.author.bot:
            return

        if message.content.find('think you should leave') >= 0:
            channel = message.channel
            index = random.randrange(0, (len(stati)-2), 1) #ignore big chungus
            quote = stati[index]
            vid = await IThinkYouShouldLeave(index)
            await channel.send(quote)
            await channel.send(vid)

        elif message.content.find('good bot') >= 0:
            channel = message.channel
            await channel.send("you mean nothing to me")
            await client.join(message)

        elif message.content.find('gary') >= 0:
            channel = message.channel
            await channel.send("gary")
        
        elif message.content.find('$p') >= 0:
            channel = message.channel
            content = message.content.split(" ",1) 
            await channel.send("searching youtube for " + content[1])
            await client.join(message)
            await client.play(message.channel, content[1])

        elif message.content.find('chungus') >= 0:
            channel = message.channel
            await client.join(message)
            await client.play(message.channel, 'https://www.youtube.com/watch?v=TWjPrp8pVdI')

        elif message.content.find('$s') >= 0:
            channel = message.channel
            await channel.send("song over")
            await client.leave(message)

        elif message.content.find('$leave') >= 0:
            channel = message.channel
            await channel.send("are you saying you think i should leave?")
            await client.leave(message)


        elif message.content.find('$die george') >= 0:
            #broken pipe errors
            channel = message.channel
            await channel.send('going to die now')
            await channel.send('you have killed me, master')
            await client.leave(message)
            await client.logout()


        elif message.content.find('$learn') >= 0:
            channel = message.channel
            content = message.content.split(' ', 1)
            if len(content) != 2:
                raise IOError
            pair = content[1].strip()
            await channel.send(content[1])
            match_pattern = '([a-z]+|(<@[0-9]+>))\s+(is|=)\s((<@[0-9]+>)|(([a-z]|\s)+))$'
            tag_pattern = '(<@[0-9]+>)$'
            good_learn = False
            #str_match = re.fullmatch(str_pattern, pair)
            if re.fullmatch(match_pattern, pair):
                values = pair.split('is')
                if len(values) != 2:
                   values = pair.split('=')
                if len(values) != 2:
                   raise IOError
                #figure out if it's name -> tag or tag -> name
                first = values[0].strip()
                second = values[1].strip()
                #current assumption is that if call is used correctly, no shenanigans
                #should probably account for shenanigans
                #call farva
                if re.fullmatch(tag_pattern,first):
                    tag = first
                    name = second
                    good_learn = True
                elif re.fullmatch(tag_pattern,second):
                    name = first
                    tag = second
                    good_learn = True
                if good_learn:
                    await file_IO.saveName(name,tag)
                    self.storage[name] = tag
                    await channel.send("Success. My gigachad brain now knows that "+name+" is equivalent to "+tag)
                else:
                    await channel.send("georgy made a fucky wucky. call police")
            else:
                print(content[1])
                await channel.send("george no understand")
                await channel.send("please say x = y or x is y")
                await channel.send("here's what faulty george brain got : " + pair)
        
        elif message.content.find('$vomit') >= 0:
            channel = message.channel
            await channel.send(self.storage)

        elif message.content.find('$who') >= 0:
            channel = message.channel
            content = message.content.split(' ')
            if len(content) == 2:
                tag = await resolveTag(content[1], self.storage)
                await channel.send(content[1] + " is " + tag)

        elif message.content.find('$george') >= 0:
            channel = message.channel
            async with channel.typing():
                await channel.send('GEORGE now back in beautiful 2.0! (that is how many threads I have)')
                time.sleep(5)
                await channel.send('ANNOY YOUR FRIENDS with the $harass command!')
                time.sleep(2)
                await channel.send('New feature! Sending more than one harrass command simultaneously will cause one of them to be unstoppable!')
                time.sleep(5)
                await channel.send('LISTEN TO SOUNDS with $p, which works really bad!')
                time.sleep(2)
                await channel.send('New playlist feature that ruins everything else!')
                time.sleep(5)
                await channel.send('At least 3 other new broken features!')
                time.sleep(5)
                await channel.send('Marvel at the broken code!')
                time.sleep(10)
                await channel.send("I don't see you looking, boy")
                time.sleep(10)
                await channel.send("Look at me, boy")
                await client.join(message)
                if talking.is_connected():
                    await client.play(message.channel, 'https://www.youtube.com/watch?v=cB4dYfFgaME')


        elif message.content.find('$help') >=0:
            channel = message.channel
            await channel.send('lol you think I write documentation')
            await client.join(message)
            if talking.is_connected():
                await client.play(message.channel, 'https://www.youtube.com/watch?v=8tOsQv-rrEE')
            while talking.is_playing():
                time.sleep(0)
            await client.leave(message)
        elif message.content.find('$harass') >= 0:
            #default string setup
            #random.randrange(0, (len(crap) - 1), 1)
            spam_call = ["%s i want to lick ur toesies", 
            "%s your very important discord colleagues would like to discuss a human business opportunity",
            "Hello %s I would like to speak to you about your vehicle's extended warranty",
            "%s, this is George from Social Security Division. Please provide me your full social security number for validation.",
            "%s https://image.sciencenordic.com/1380703.jpg?imageId=1380703&panow=0&panoh=0&panox=0&panoy=0&heightw=0&heighth=0&heightx=0&heighty=0&width=1200&height=900",
            "%s, this is George from Ubisoft. If you don't get on immediately I'm nerfing your favorite op",
            "%s"]
            channel = message.channel
            # Command separates arguments with a ,
            content = message.content.split(',')
            # Strips the "harass " from the tag
            content[0] = content[0].replace("$harass", "")
            full = True
            if (content[0] == ""):
                await channel.send("The harass command follows this format: '$harass <tag or known alias>, <delay, optional>, <message, optional>'. Type $help for more info")
                full = False
            content[0] = content[0].strip()
            # Checks the tag isn't already in data.txt
            tag = await resolveTag(content[0], self.storage)
            #set delay if not recieved
            if(len(content) > 1):
                delay = content[1].strip()
            else:
                delay = 3

            if len(content) == 1  & full :
                await client.activate(channel, spam_call[random.randrange(0, (len(spam_call)-1),1)] % tag, delay)
    
            # Second argument determines how quickly to spam
            elif len(content) == 2:
                #confirm delay is valid
                retval = await delayCheck(delay)
                if retval == 1:
                    delay = int(delay)
                    await client.activate(channel,spam_call[random.randrange(0, (len(spam_call)-1),1)] % tag, delay)
                elif retval == -1:
                    await channel.send("Delay must be a positive number, defaulting to 3 seconds")
                    await client.activate(channel,"%s, this server is completely dead without you" % tag, 3)

            # Third argument assigns a custom message
            elif len(content)==3:
                retval = await delayCheck(delay)
                if retval == 1:
                    delay = int(delay)
                    await client.activate(channel, content[2], delay)
                elif retval == -1:
                    await channel.send("Delay must be a positive number, defaulting to 3 seconds")
                    await client.activate(channel, content[2], 3)

        elif message.content.find('cease') >= 0:
            channel = message.channel
            await client.deactivate(channel)

client = GeorgeBot()
client.run(confidential.token)
