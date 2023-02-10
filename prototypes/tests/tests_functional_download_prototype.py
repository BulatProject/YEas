import subprocess
from os import remove, rename
import os.path as path
import eyed3
import unittest
from .. import BAN_LIST, CONVERSION, URLS, WEBM, MP3, ERROR, Downloader
from pytube import YouTube


URLS = {'https://youtu.be/7PCkvCPvDXk':
            ['Meghan Trainor - All About That Bass (Official Video)',
            'Meghan Trainor - All About That Bass (Official Video)',
            'Meghan_Trainor_-_All_About_That_Bass_(Official_Video),',
            'Meghan Trainor'
            ], 
        'https://youtu.be/qMXESlny4-I':
            ['Falling In Reverse - "Watch The World Burn"',
            'Falling In Reverse - Watch The World Burn',
            'Falling_In_Reverse_-_Watch_The_World_Burn',
            'Epitaph Records'
            ],
        'https://youtu.be/lVDvetAxbiI':
            ['FEE LION - Re: (Visit) (Official Single)',
            'FEE LION - Re (Visit) (Official Single)',
            'FEE_LION_-_Re_(Visit)_(Official_Single)',
            'FEE LION'
            ],
        'https://youtu.be/BiBTpQPCMtg':
            ['LUCKY TAPES - レイディ・ブルース (Official Music Video)',
            '',
            '',
            'RALLYE LABEL'
            ]
}


class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.url = 'https://youtu.be/7PCkvCPvDXk'
        yt = YouTube(self.url)
        self.downloader = Downloader(yt)

    def test_clear_title(self):
        self.title = URLS[self.url]
        self.downloader.clear_title(self.title[0])
        self.assertEqual(self.downloader.altered_title, self.title[1])
        self.assertEqual(self.downloader.finished_title, self.title[2])

    def test_download(self):
        self.downloader.download()
        self.assertTrue(path.exists(f'songs/{self.downloader.finished_title}.webm'))

    def test_convert(self):
        self.downloader.convert()
        self.assertFalse(path.exists(f'songs/{self.downloader.finished_title}.webm'))
        self.assertTrue(path.exists(f'songs/{self.downloader.altered_title}.mp3'))

    def test_set_tags(self):
        base = eyed3.load(f'songs/{self.downloader.altered_title}.mp3')
        self.assertEqual(base.tag.title, self.title[0])
        self.assertEqual(base.tag.artist, self.title[3])


if __name__ == '__main__':
    unittest.main()
