import wx
import wx.lib.scrolledpanel as scrolledpanel
from src.ui.action_button import ActionButton
from src.wrapper.json import JsonParser
from src.wrapper.downloader import Downloader

class DownloadList(scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        scrolledpanel.ScrolledPanel.__init__(self, parent)

        self.master = parent
        self.running_thread = []

        self.InitUI()

    def InitUI(self):
        self.item_list = []
        self.object_list = []

        self.Update()
        cache = JsonParser.GetCacheFile()
        self.data = JsonParser.ReadFromJson(cache)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(len(self.data["download_list"]), 6, 0, 7)
        fgSizer1.AddGrowableCol(0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        counter = 0
        for item in self.data["download_list"]:
            item_dict = {
                "title": None,
                "speed": None,
                "status": None,
                "percent": None,
                "size": None,
            }

            Title = wx.StaticText(
                self, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0
            )
            Title.Wrap(-1)

            item_dict["title"] = Title
            self.object_list.append(Title)
            fgSizer1.Add(Title, 0, wx.ALL, 5)

            Speed = wx.StaticText(
                self, wx.ID_ANY, "", wx.DefaultPosition, (100, 20), 0
            )
            Speed.Wrap(-1)

            self.object_list.append(Speed)
            item_dict["speed"] = Speed 
            fgSizer1.Add(Speed, 0, wx.ALL, 5)

            Status = wx.StaticText(
                self, wx.ID_ANY, item['status'], wx.DefaultPosition, (100, 20), 0
            )
            Status.Wrap(-1)

            self.object_list.append(Status)
            item_dict["status"] = Status
            fgSizer1.Add(Status, 0, wx.ALL, 5)

            percent = wx.StaticText(
                self, wx.ID_ANY, u"", wx.DefaultPosition, (50,20), 0
            )
            percent.Wrap(-1)
            item_dict["percent"] = percent 
            self.object_list.append(percent)
            fgSizer1.Add(percent, 0, wx.ALL, 5)

            size = wx.StaticText(
                self, wx.ID_ANY, u"", wx.DefaultPosition, (50,20), 0
            )
            size.Wrap(-1)
            item_dict["size"] = size 
            self.object_list.append(size)
            fgSizer1.Add(size, 0, wx.ALL, 5)

            m_button2 = wx.Button(
                self, wx.ID_ANY, u"Action", wx.DefaultPosition, wx.DefaultSize, 0
            )
            m_button2.Bind(
                wx.EVT_BUTTON,
                lambda event, obj=item_dict: self.popup_action(event, obj),
            )

            self.object_list.append(m_button2)
            fgSizer1.Add(m_button2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

            self.item_list.append(item_dict)
            counter += 1

        self.SetSizer(fgSizer1)
        self.SetupScrolling()
        self.Layout()

    def popup_action(self, e, obj):
        self.PopupMenu(ActionButton(self, obj))

    def CreateThread(self, video_url, format_id, obj):
        download_thread = Downloader(video_url, format_id=format_id, obj=obj, master=self)
        self.running_thread.append({"thread": download_thread, "object": obj})
        download_thread.start()

    def CleanUp(self, obj):
        counter = 0
        for thread in self.running_thread:
            if thread["object"] == obj:
                obj['status'].SetLabel("Paused")
                thread["thread"].proc.terminate()
                thread["thread"].join()
                self.running_thread.pop(counter)
            counter += 1

    def remove_item(self, obj):
        cache_file = JsonParser.GetCacheFile()
        data = JsonParser.ReadFromJson(cache_file)
        for d in range(len(data['download_list'])):
            if data['download_list'][d]["title"] == obj['title'].GetLabel():
                data['download_list'].pop(d)
                break

        JsonParser.WriteToJson(data, cache_file)
        self.master.update_list()

    def update_ui(self):
        for item in self.object_list:
            item.Destroy()
