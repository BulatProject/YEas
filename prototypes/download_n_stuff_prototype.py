from pytube import YouTube
import subprocess
from os import rename as rename
from os import remove as remove
import os.path as path
import eyed3

DIRECTORY = 'D:\\Programs\\My\\YEasy\\test_downloads'
CONVERSION = "ffmpeg -i {} -codec:a libmp3lame -qscale:a 2 {}"
URLS = ['https://youtu.be/7PCkvCPvDXk', 'https://youtu.be/1oMgxa32A7g', 'https://www.youtube.com/watch?v=7-x3uD5z1bQ&list=PLZ1oGv-Tyew2v3zjJNX5E1PxU3WPFKbmM&index=23&ab_channel=HarryStylesVEVO', 'https://www.youtube.com/watch?v=DRHTr6wl3Q4']

yt = YouTube(URLS[1])
title = yt.title
author = yt.author 
stream = yt.streams.filter(only_audio=True).last()
stream.download(output_path=DIRECTORY, filename=f'{title[:2]}.webm')

path_temp = path.join(DIRECTORY, title[:2])

input_file = f"{path_temp}.webm"
output_file = f"{path_temp}.mp3"

command = CONVERSION.format(input_file, output_file)

p = subprocess.run(command, shell=True)

base = eyed3.load(output_file)
base.tag.title = title
base.tag.artist = author
base.tag.save()

rename(output_file, f"{path.join(DIRECTORY, title)}.mp3")


if p.returncode == 0:
    remove(input_file)

#TODO Добавить обход возраста, проверку на доступность.