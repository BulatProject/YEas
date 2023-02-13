from pytube import YouTube
import subprocess
from os import remove, rename
import os.path as path
import eyed3
from TEXTS import BAN_LIST, CONVERSION, WEBM, MP3, CONVERSION_ERROR, DOWNLOADING_ERROR


class Downloader:
    def __init__(self, yt, path):
        self.path = path
        self.yt = yt
        self.title = yt.title
        self.author = yt.author
        self.stream = self.yt.streams.filter(only_audio=True).last()
        self.clear_title(self.title)

    def clear_title(self, title):
        for symbol in BAN_LIST:
            if symbol in title:
                title = title.replace(symbol, '')
        self.altered_title = title
        self.finished_title = title.replace(" ", "_")

    def download(self):
        try:
            self.stream.download(output_path=self.path, filename=f'{self.finished_title}.webm')
        except:
            return (False, DOWNLOADING_ERROR.format(self.title, self.author))
        return (True, self)

    def convert(self):
        input_file = WEBM.format(path.join(self.path, self.finished_title))
        output_file = MP3.format(path.join(self.path, self.finished_title))
        command = CONVERSION.format(input_file, output_file)
        converting = subprocess.run(command, shell=True)
        if converting.returncode == 0:
            remove(input_file)
            return self.set_tags(output_file)
        else:
            return (False, CONVERSION_ERROR.format(self.title, self.author))

    def set_tags(self, output_file):
        base = eyed3.load(output_file)
        if ' - ' not in self.altered_title:
            base.tag.title = self.altered_title
            base.tag.artist = self.author
        else:
            base.tag.artist, base.tag.title = self.altered_title.split(' - ')
        base.tag.save()
        return self.rename_song(output_file)

    def rename_song(self, output_file):
        new_name = MP3.format(path.join(self.path, self.altered_title))
        rename(output_file, new_name)
        return (True, new_name)
