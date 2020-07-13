import wx
from src.ui.menubar import MenuBar
from src.ui.download_list import DownloadList

class MainApplication(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)
        menubar = MenuBar(master=self)
        self.download_list = DownloadList(self)

    def update_list(self):
        self.download_list.update_ui()
        self.Refresh()
        self.Update()
        self.download_list.InitUI()
