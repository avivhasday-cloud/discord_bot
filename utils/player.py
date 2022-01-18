from youtube_dl import YoutubeDL
import discord
from discord import ClientException
from utils.logger import LOGGER
class MusicPlayer():

    def __init__(self):
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.queue = []
        self.is_playing = False

    # searching the item on youtube
    def search_youtube(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                LOGGER.info(f"Searching {item} in youtube")
                if item.startswith("http"):
                    LOGGER.info(f"{item} is URL")
                    info = ydl.extract_info(item, download=False)
                else:
                    LOGGER.info(f"{item} is search query")
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return info['formats'][0]['url'], info['title']

    def play_next(self, voice):
        if len(self.queue) > 0:
            self.is_playing = True
            # get the first url
            (url, title) = self.queue[0]
            # remove the first element as you are currently playing it
            self.queue.pop(0)
            LOGGER.info(f"Start playing {title}")
            voice.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(voice))
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, voice):
        if len(self.queue) > 0:
            try:
                self.is_playing = True
                (url, title) = self.queue[0]
                # remove the first element as you are currently playing it
                self.queue.pop(0)
                LOGGER.info(f"Start playing {title}")
                voice.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
            except ClientException as err:
                print(err)
        else:
            self.is_playing = False

