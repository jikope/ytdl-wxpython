import wx
import wx.adv
from src.ui.dialog import AddVideoDialog
from src.ui.dialog import AddVideoDialog
from src.wrapper.json import JsonParser

APP_EXIT = 1
APP_ABOUT = 3
APP_DOWNLOAD = 4
APP_SETTING = 5

class MenuBar(wx.MenuBar):
    def __init__(self, master):
        self.Menu = wx.MenuBar()
        self.master = master
        self.add_file_menu()
        self.add_download_menu()
        self.add_about_menu()

        master.SetMenuBar(self.Menu)
        master.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        master.Bind(wx.EVT_MENU, self.OnDownload, id=APP_DOWNLOAD)
        master.Bind(wx.EVT_MENU, self.OnSetting, id=APP_SETTING)
        master.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

    def add_file_menu(self):
        file_menu = wx.Menu()

        quit_item = wx.MenuItem(file_menu, APP_EXIT, "&Quit\tCtrl+Q")


        file_menu.Append(quit_item)
        self.Menu.Append(file_menu, "&File")

    def add_download_menu(self):
        download_menu = wx.Menu()

        download_item = wx.MenuItem(download_menu, APP_DOWNLOAD, "&Download Video")
        setting_item = wx.MenuItem(download_menu, APP_SETTING, "&Setting")

        download_menu.Append(download_item)
        download_menu.Append(setting_item)
        self.Menu.Append(download_menu, "&Download")

    def add_about_menu(self):
        about_menu = wx.Menu()

        about_item = about_menu.Append(wx.ID_ABOUT, "About", "About Application")

        self.Menu.Append(about_menu, "&About")

    def OnDownload(self, e):
        cdDialog = AddVideoDialog(self.master)
        cdDialog.ShowModal()
        cdDialog.Destroy()

    def OnSetting(self, e):
        cdDialog = wx.DirDialog(self.master, message="Download Dircetory")
        if cdDialog.ShowModal() == wx.ID_OK:
            JsonParser.ChangeDownloadDir(cdDialog.GetPath())
        cdDialog.Destroy()

    def OnQuit(self, e):
        self.master.Close()

    def OnAbout(self, e):
        description = """
        ytdl-wxpython is an unofficial graphical user interface application for youtube-dl. This application is made in python using wxPython framework.
"""
        licence = """
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("ytdl-wxpython")
        info.SetVersion("1.0")
        info.SetDescription(description)
        info.SetCopyright("(C) 2020 Bima Wiratama")
        info.SetLicence(licence)
        info.AddDeveloper("Bima Wiratama")
        info.AddDocWriter("Bima Wiratama")

        wx.adv.AboutBox(info)
