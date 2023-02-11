from pytube import YouTube
import subprocess
from os import remove, rename
import os.path as path
import eyed3

BAN_LIST = ['/', '\\', ':', '*', '?', '<', '>', '|', '"', "'"]
CONVERSION = r"ffmpeg -i {} -codec:a libmp3lame -qscale:a 2 {}"
WEBM = r'{}.webm'
MP3 = r"{}.mp3"
CONVERSION_ERROR = r'Произошла ошибка при конвертации в mp3 песни {} канала {}'
DOWNLOADING_ERROR = r'Произошла ошибка при скачивании файла. Видео: {} канала {}.'

class Downloader:
    def __init__(self, yt):
        self.yt = yt
        self.title = yt.title
        self.author = yt.author
        self.stream = self.yt.streams.filter(only_audio=True).last()
        self.clear_title(self.title)

    def clear_title(self, title):
        altered_title = ''
        for symbol in BAN_LIST:
            if symbol in title:
                altered_title = title.replace(symbol, '')
        self.altered_title = altered_title
        self.finished_title = altered_title.replace(" ", "_")

    def download(self):
        try:
            self.stream.download(output_path='songs', filename=f'{self.finished_title}.webm')
        except:
            return DOWNLOADING_ERROR.format(self.title, self.author)

    def convert(self):
        input_file = WEBM.format(path.join('songs', self.finished_title))
        output_file = MP3.format(path.join('songs', self.finished_title))
        command = CONVERSION.format(input_file, output_file)
        converting = subprocess.run(command, shell=True)
        if converting.returncode == 0:
            remove(input_file)
            self.set_tags(output_file)
        else:
            return CONVERSION_ERROR.format(self.title, self.author)

    def set_tags(self, output_file):
        base = eyed3.load(output_file)
        base.tag.title = self.title
        base.tag.artist = self.author
        base.tag.save()
        self.rename_song(output_file)

    def rename_song(self, output_file):
        new_name = MP3.format(path.join('songs', self.altered_title))
        rename(output_file, new_name)
        return new_name
