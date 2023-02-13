import requests
from pytube import YouTube
from TEXTS import  EXAMPLES, CLEAN_LINK, ERRORS


class Checker:
    def __init__(self, url):
        if len(url) < 131:
            for example in EXAMPLES:
                if url.startswith(example):
                    self.base_check = (True, url)
                    break;
            else:
                self.base_check = (False, ERRORS[2])
        else:
            self.base_check = (False, ERRORS[2])

    def check_status_code(self, url):
        try:
            response = requests.get(url)
        except:
            return (False, ERRORS[0])
        if response.status_code != 200:
            return (False, ERRORS[1].format(self.url, response.status_code))
        return (True, url)

    def check_access(self, url):
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).last()
        except:
            return (False, ERRORS[3].format(url))
        return (True, yt)
