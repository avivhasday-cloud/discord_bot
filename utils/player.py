from youtube_dl import YoutubeDL
import discord
from discord import ClientException
from utils.music_queue import MusicQueue
from utils.logger import LOGGER


class MusicPlayer():

    def __init__(self):
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.music_queue = MusicQueue()
        self.is_playing = False

    def reset(self):
        self.music_queue.reset()
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
        if not self.music_queue.is_empty():
            try:
                self.is_playing = True
                # get the first url
                (url, title) = self.music_queue.get()
                if not self.music_queue.loop_queue:
                    self.music_queue.pop()
                else:
                    current_index = self.music_queue.current_track_index
                    self.music_queue.current_track_index = current_index + 1 if current_index < len(self.music_queue) -1 else 0
                LOGGER.info(f"Start playing {title}")
                voice.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS))
            except ClientException as err:
                LOGGER.error(f"{err}")
        else:
            LOGGER.info("Queue is empty!")
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, voice):
        while not voice.is_playing():
            self.play_next(voice)

