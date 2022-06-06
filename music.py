import youtube_dl
import discord
import asyncio
from youtube_dl.utils import date_formats
from youtubesearchpython.__future__ import *


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        info = ytdl.extract_info(url, download=False)
        I_URL = info['formats'][0]['url']
        return I_URL

    @classmethod
    async def from_search(cls, url, *, loop=None, stream = False):
        loop = loop or asyncio.get_event_loop()
        videosSearch = VideosSearch(url, limit = 1)
        videosResult = await videosSearch.next()
        return videosResult
