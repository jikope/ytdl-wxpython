from pathlib import Path
import json

class JsonParser():
    def __init__(self):
        pass

    @staticmethod
    def CheckFileExist(file_path):
        if Path(file_path).is_file():
            return True
        else:
            return False

    @staticmethod
    def GetDownloadDir():
        download_dir = str(Path.home()) + "/Downloads"
        if JsonParser.CheckFileExist('ytdl.conf'):
            print("success")
        else:
            print("creating config file")
            with open('ytdl.conf', 'w') as conf_file:
                conf_file = conf_file.write(download_dir)

        with open('ytdl.conf', 'r') as conf:
            config_file = conf.read()
        return config_file 
    
    @staticmethod
    def GetCacheFile():
        data = {
            'download_list': []
        }
        if JsonParser.CheckFileExist('ytdl.json'):
            print("success")
        else:
            print("creating cache file")
            with open('ytdl.json', 'w') as f:
                json.dump(data, f)

        cache_file = 'ytdl.json'
        return cache_file

    @staticmethod
    def ChangeDownloadDir(download_dir):
        with open('ytdl.conf', 'w') as f:
            f.write(download_dir)

    @staticmethod
    def WriteToJson(data, filename):
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)

    @staticmethod
    def ReadFromJson(filename):
        with open(filename, 'r') as jsonfile:
            return json.load(jsonfile)

