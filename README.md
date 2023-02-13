Packages used:
python-telegram-bot v20.1
ffmpeg version 5.1.2
Pytube version: 12.1.2

This code could be used to create a telegram bot, which would be able to download single audiofiles from Youtube videos or multiple ones from playlists via link.

Using the code without adjustments:

This app is divided into 5 modules:

main.py
get_mp3.py
prepare_text.py
check_availability.py
TEXTS.py

There is one extra file, that is used to store telegram token, but it is not present in files for security reasons.


main.py module contains telegram api, is responsible for receiving messages and sending the answers back, on top of doing the first filtering of received messages and distributing tasks to other modules. Deletes downloaded file after is was sent to user.

prepare_text.py is used to divide message texts, clean them from spaces and check if message satisfies the criteria to proceed next. Most functions used in preparations to download songs from playlists. 

check_availability.py looks if url is correct and gets response code from it to be sure that access is available.

get_mp3.py cleres all symbols that can cause an error in ffmpeg library (and strips files from useless "(Official Video)" and similar texts). Then it converts webm-file into an mp3 one, sets IP3 tags and deletes webm-file.