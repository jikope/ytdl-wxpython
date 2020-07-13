from __future__ import unicode_literals
import youtube_dl
import subprocess
import wx
from src.wrapper.json import JsonParser
from threading import Thread


class Downloader(Thread):
    def __init__(self, url, format_id=None, obj=None, master=None):
        Thread.__init__(self)
        self.format_id =format_id 
        self.url = url
        self.obj = obj 
        self.master = master

    def run(self):
        self.DownloadUrl()

    def DownloadUrl(self):
        file_path = JsonParser.GetDownloadDir() + "/%(title)s.%(ext)s"

        info = preexec = None
        cmd = ['/usr/bin/youtube-dl', '-f', self.format_id,  '--newline', self.url, '-o', file_path]
        self.proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=preexec,
            startupinfo=info,
        )
        counter = 0
        wx.CallAfter(self.obj['status'].SetLabel, "Downloading")
        while True:
            line = self.proc.stdout.readline()
            if not line:
                break
            if counter < 5:
                counter += 1
                continue
            #the real code does filtering here
            raw = str(line.rstrip()).split(" ")
            if 'in' in raw:
                wx.CallAfter(self.obj['status'].SetLabel, "Completed")
                self.CleanUp()
                break
            raw.reverse()
            raw.remove('ETA')
            raw.remove('at')
            raw.remove('of')
            raw.pop()
            wx.CallAfter(self.obj['speed'].SetLabel, raw[1])
            wx.CallAfter(self.obj['percent'].SetLabel, raw[3])
            wx.CallAfter(self.obj['size'].SetLabel, raw[2])

    def CleanUp(self):
        cache_file = JsonParser.GetCacheFile()
        data = JsonParser.ReadFromJson(cache_file)
        for x in data['download_list']:
            if x['video_url'] == self.url:
                x['status'] = "Completed"

        JsonParser.WriteToJson(data, cache_file)
        counter = 0
        for thread in self.master.running_thread:
            if thread["object"] == self.obj:
                self.master.running_thread.pop(counter)
            counter += 1

class UrlInfo():
    def __init__(self):
        pass
    @staticmethod
    def GetVideoInfo(video_url):
        video_info = youtube_dl.YoutubeDL()
        video_info = video_info.extract_info(url=video_url, download=False)

        return video_info

    @staticmethod
    def AddToQueue(opts):
        file_path = JsonParser.GetCacheFile()

        data = JsonParser.ReadFromJson(file_path)
        temp = data['download_list']
        temp.append(opts)

        JsonParser.WriteToJson(data, file_path)

