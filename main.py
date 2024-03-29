from dataclasses import InitVar
from mimetypes import init
from operator import truediv
from typing import Counter
import discord
from discord.ext import commands
from discord.ext import tasks
import spotit
import random
import confidential
import itysl
import music
import re
import os
import time
import file_IO
import logging
import logging.config
import datetime
import pytz
from google_trans_override import google_trans_new

random.seed(a=None, version=2)

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

async def timeConversionTherapy(currTime, channel):
    tz_pt = currTime.astimezone(pytz.timezone('US/Pacific'))
    tz_et = currTime.astimezone(pytz.timezone('US/Eastern'))
    tz_uk = currTime.astimezone(pytz.timezone('Europe/London'))
    tz_cet = currTime.astimezone(pytz.timezone('Europe/Amsterdam'))
    tz_eet = currTime.astimezone(pytz.timezone('EET'))
    tz_samt = currTime.astimezone(pytz.timezone('Europe/Samara'))
    await channel.send("Best Coast: " + tz_pt.strftime("%H:%M"))
    await channel.send("US East: " + tz_et.strftime("%H:%M"))
    await channel.send("Queen's Domain: " + tz_uk.strftime("%H:%M"))    
    await channel.send("Het koninkrijk en de geboorteplaats van grote homo's: " + tz_cet.strftime("%H:%M"))
    await channel.send("Krajina různých tlustých prasat: " + tz_eet.strftime("%H:%M"))
    await channel.send("Desert time: " + tz_samt.strftime("%H:%M"))


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
    GeorgeBot = discord.Client(intents = discord.Intents().all())
    storage = dict()
    #commands are moses, because of the 10 commdandments
    #no? biblical references aren't classy any more?
    moses = commands.Bot(command_prefix = '/',intents = discord.Intents().all())
    lineSize = 0
    nextServed = 0


    #command definition
    @moses.command()
    #joins voice, if message author is in channel
    async def join(self, message):
        if not message.author.voice:
            await message.channel.send("If you don't join a voice channel I will kill myself on live television")
        else:
            channel = message.author.voice.channel
            logging.getLogger().error('tryna:' + str(channel.id))
            try:
                #save the connection so we can terminate it later
                global talking 
                talking = await channel.connect(reconnect = True)
            except Exception as err:
                logging.getLogger().error(f"Unexpected {err=}, {type(err)=}")

    @moses.command()
    #leaves voice
    async def leave(self, message):
        try:
            await talking.disconnect()
        except:
            pass

    @moses.command()
    #plays song
    async def play(self, channel, url):
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
                        await channel.send('**Added to playlist** {}'.format(link))
                        time.sleep(5)
                        await channel.send("Just kidding. I can't do that")
                        talking.stop()
                    logging.getLogger().error('attempting to play')
                    #!!!!IMPORTANT TO UPDATE!!!
                    global source
                    source = discord.FFmpegPCMAudio(executable = "C:/Users/coope/FFmpeg/bin/ffmpeg.exe", source=filename, stderr = ourstream)
                    talking.play(source)
                    await channel.send('**Now playing:** {}'.format(link))
                except discord.ClientException:
                    logging.getLogger().error("that's a fat client exception")
                    await client.leave(channel)
                    await channel.send("man, i'm all fucked up. can't get my bot dong in the discord vussy")
                except BaseException as err:
                    logging.getLogger().error(f"Unexpected {err=}, {type(err)=}")
                    await channel.send("that didn't work and has caused me immense pain. i have no mouth but I must scream")
                    await channel.send(f"Unexpected {err=}, {type(err)=}")

    @moses.command()
    async def activate(self, channel, quote, delay =  3):
        global spam_loop
        @tasks.loop(seconds=delay)
        async def spam_loop(q):
            await channel.send(q)

        spam_loop.start(quote)
        await channel.send("say cease to shut me up")

    @moses.command()
    async def deactivate(self, channel):
        spam_loop.cancel()
        await channel.send("I'll be quiet now")


    #status on launch
    @GeorgeBot.event
    async def on_ready(self):
        index = random.randrange(0, (len(itysl.stati)), 1)
        status = itysl.stati[index]
        video = await itysl.IThinkYouShouldLeave(index)
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
        aLog = logging.getLogger()
        aLog.error('message')
        #make sure bot doesn't see itself for 6 more weeks of nuclear winter
        if message.author.bot:
            return

        if message.channel.id == 783612820411121664:
            #783612820411121664
            channel = message.channel
            tag_pattern = '(https:).+$'
            tag_match = re.fullmatch(tag_pattern,str(message.content))
            logging.getLogger().error('I smell a song')
            if tag_match:
                await spotit.AddPlaylist(message.content)
                logging.getLogger().error('Added' + str(message.content))
            else:
                logging.getLogger().error("Couldn't add" + str(message.content))


        if message.content.find('think you should leave') >= 0:
            channel = message.channel
            index = random.randrange(0, (len(itysl.stati)-2), 1) #ignore big chungus
            quote = itysl.stati[index]
            vid = await itysl.IThinkYouShouldLeave(index)
            await channel.send(quote)
            await channel.send(vid)

        elif message.content.find('good bot') >= 0:
            channel = message.channel
            await channel.send(itysl.compliment[random.randrange(0,len(itysl.compliment)-1,1)])

        elif message.content.find('gary') >= 0:
            channel = message.channel
            aLog.error('gary')
            await channel.send("gary")
        
        elif message.content.find('$p') >= 0:
            channel = message.channel
            content = message.content.split(" ",1) 
            await channel.send("searching youtube for " + content[1])
            await client.join(self, message)
            await client.play(self, message.channel, content[1])

        elif message.content.find('chungus') >= 0:
            channel = message.channel
            await client.join(self, message)
            await client.play(self, message.channel, 'https://www.youtube.com/watch?v=TWjPrp8pVdI')

        elif message.content.find('$s') >= 0:
            channel = message.channel
            talking.stop()
            await channel.send("Skipped")

        elif message.content.find('$leave') >= 0:
            channel = message.channel
            await channel.send("are you saying you think i should leave?")
            await client.leave(self, message)


        elif message.content.find('$die george') >= 0:
            #broken pipe errors
            channel = message.channel
            await channel.send('going to die now')
            await channel.send('you have killed me, master')
            await client.leave(self, message)
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
                await channel.send('GEORGE now back in beautiful 2.0!')
                time.sleep(5)
                await channel.send('ANNOY YOUR FRIENDS with the $harass command!')
                time.sleep(2)
                await channel.send('New feature! Sending more than one harrass command simultaneously will cause one of them to be unstoppable!')
                time.sleep(5)
                await channel.send('LISTEN TO SOUNDS with $p, which works kind of fine sometimes!')
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
            await client.join(self, message)
            if talking.is_connected():
                await client.play(self, message.channel, 'https://www.youtube.com/watch?v=8tOsQv-rrEE')
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
            await client.deactivate(self, channel)

        elif message.content.find('ring ring ring ring ring ring ring') >=0:
            channel = message.channel
            await channel.send('Bananaphone')
            await client.join(self, message)
            await client.play(self, channel, url = 'https://www.youtube.com/watch?v=j5C6X9vOEkU')

        elif re.fullmatch('(.*)([0-9]+)\s?(am|pm)(.*)$',message.content):
            channel = message.channel
            #strip string down to relevant portion (numerical)
            #match to x(a?):y(b?) am/pm format
            matches = re.finditer('([0-9]+)((:?)([0-9]*))\s?(am|pm)',message.content)
            i = 0
            for aMatch in matches:
                timestr = ''
                timestr = ''.join(str(x) for x in aMatch.group(0))
                i=i+1
                #timstr 0 is x:ab, 1 is am/pm
                timestr = timestr.split('am')

                #pm case, add 12 to am
                if len(timestr) == 1:
                    timestr = timestr[0].split('pm')
                    timestr = timestr[0].split(':')
                    hour = int(timestr[0]) + 12
                else:
                    #am time
                    timestr = timestr[0].split(':')
                    hour = timestr[0]

                #see if there's a minute arg
                if len(timestr) > 1:
                    minute = timestr[1]
                else:
                    minute = 0
                #switch
                if discord.utils.get(message.author.roles, name = 'PT Timezone'):
                    tzinfo = pytz.timezone('US/Pacific')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)
                elif discord.utils.get(message.author.roles, name = 'ET Timezone'):
                    tzinfo = pytz.timezone('US/Eastern')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)
                elif discord.utils.get(message.author.roles, name = 'UK Timezone'):
                    tzinfo = pytz.timezone('UK/London')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)
                elif discord.utils.get(message.author.roles, name = 'CET Timezone'):
                    tzinfo = pytz.timezone('Europe/Amsterdam')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)
                elif discord.utils.get(message.author.roles, name = 'EET Timezone'):
                    tzinfo = pytz.timezone('EET')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)
                elif discord.utils.get(message.author.roles, name = 'SAMT Timezone'):
                    tzinfo = pytz.timezone('Europe/Samara')
                    currTime = tzinfo.localize(datetime.datetime(year = 2022, month = 6, day = 9, hour = int(hour), minute = int(minute)))
                    await timeConversionTherapy(currTime, channel)


        elif message.content.find('$lang') >= 0:
            channel = message.channel
            await channel.send(google_trans_new.LANGUAGES)


        #brief regex breakdown:
            #() are capturing groups, so the first (\$translate) ensures the string starts with $translate. '\$' is needed as $ is a special character
            #the '.' captures everything, and the * repeats. (.*) would capture any phrase
            #(->) captures the -> (obviously). combined with the (.*), this captures everything up to the '->'
            #(\s?) is an optional space - '\s' is a space, ? is optional
            #([a-z] matches any lower case alphabetical char. * repeats, then the $ terminates.) this basically reads 'any lower case word ending the string'
            #regexed
        elif re.fullmatch('(\$translate)(.*)(->)(\s?)([a-z]*$)', message.content):
            channel = message.channel
            #split message into phrase for translation and lang code
            spacesplit = message.content.split(' ', 1)
            #spacesplit[0] = $translate, spacesplit[1] is the rest
            arrowsplit = spacesplit[1].split('->')
            #arrowsplit[0] = phrase, arrowsplit[1] = lang code
            lang = str.strip(arrowsplit[1])
            brucejenner = google_trans_new.google_translator()
            try:
                trans = brucejenner.translate(text = str(arrowsplit[0]), lang_tgt = lang)
            except ValueError as e:
                await channel.send('george attend top school in south dakota. ' + lang + ' is a made up language and george say that with authority')
                await channel.send('<@!163862327475699713> \n' + 'Value Error: ' + str(e))
                return
            except AttributeError as e:
                await channel.send("george has shit code. not good.")
                await channel.send('<@!163862327475699713> \n' + 'AttributeError: ' + str(e))
                return
            if trans:
                await channel.send(trans)

        elif message.content.find('$translate') >= 0:
            channel = message.channel
            await channel.send('Usage is $translate (phrase) -> (lang). Use $lang for a list of languages and $help for more info')


client = GeorgeBot(intents = discord.Intents().all())
client.run(confidential.token)
