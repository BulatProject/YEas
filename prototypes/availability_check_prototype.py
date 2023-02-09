import requests

URLS = ['https://youtu.be/7PCkvCPvDXk', 
        'https://youtu.be/1oMgxa32A7g', 
        'https://www.youtube.com/watch?v=7-x3uD5z1bQ&list=PLZ1oGv-Tyew2v3zjJNX5E1PxU3WPFKbmM&index=23&ab_channel=HarryStylesVEVO', 
        'https://www.youtube.com/watch?v=DRHTr6wl3Q4&ab_channel=DoraSalvatore', 
        'https://www.youtube.com/watch?v=DRHTr6wl3Q4']
LINKS = ['https://youtu.be/', 'https://www.youtube.com/watch?', 'youtu.be/', 'youtube.com/watch?']
CLEAN_LINK = f'Ссылка на видео должна начинаться как один из примеров:\n"{LINKS[0]}"\n"{LINKS[1]}"\n"{LINKS[2]}"\n"{LINKS[3]}"'

class Checker:
    def __init__(self, url):
        fine_link = url.startswith(LINKS[0]) or url.startswith(LINKS[1]) or url.startswith(LINKS[2]) or url.startswith(LINKS[3])
        if fine_link:
            self.url = url
        else:
            self.url = False

    def check_status_code(self):
        if self.url:
            try:
                response = requests.get(self.url)
            except:
                return "Ресурс недоступен."
            if response.status_code == 200:
                return True
            else:
                return f'Ошибка в ссылке или доступ к видео ограничен. Код ошибки - {response.status_code}'
        else:
            return f"Ссылка не соответстует требованиям:\n{CLEAN_LINK}"


# For tests.
for url in URLS:
    test = Checker(url)
    test.check_status_code()