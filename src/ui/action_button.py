import wx

ACTION_START = 1
ACTION_PAUSE = 2
ACTION_DELETE = 3

class ActionButton(wx.Menu):
    def __init__(self, parent, obj):
        super(ActionButton, self).__init__()

        self.parent = parent
        self.obj = obj

        start = wx.MenuItem(self, ACTION_START, "&Start")
        pause = wx.MenuItem(self, ACTION_PAUSE, "&Pause")
        delete = wx.MenuItem(self, ACTION_DELETE, "&Delete")

        self.Bind(wx.EVT_MENU, self.OnStart, id=ACTION_START)
        self.Bind(wx.EVT_MENU, self.OnPause, id=ACTION_PAUSE)
        self.Bind(wx.EVT_MENU, self.OnDelete, id=ACTION_DELETE)

        self.Append(start)
        self.Append(pause)
        self.Append(delete)

    def OnStart(self, e):
        for item in self.parent.data["download_list"]:

            if item["title"] == self.obj['title'].GetLabel() and item['status'] != 'Completed':
                self.parent.CreateThread(item['video_url'], item['format_id'], self.obj)
                break

            elif item["title"] == self.obj['title'].GetLabel() and item['status'] == 'Completed':
                wx.MessageBox('Item already downloaded', 'Info', wx.OK | wx.ICON_INFORMATION)
                break
            else:
                print("test")


    def OnPause(self, e):
        self.parent.CleanUp(self.obj)

    def OnDelete(self, e):
        self.parent.remove_item(self.obj)
