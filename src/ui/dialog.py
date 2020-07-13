import wx
from src.wrapper.downloader import Downloader, UrlInfo 

class AddVideoDialog(wx.Dialog):

    def __init__(self, master):
        wx.Dialog.__init__(self, master)

        self.InitUI()
        self.SetSize((500, 300))
        self.SetTitle("Add download item")
        self.video_info = {}
        self.master = master


    def InitUI(self):

        panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        text1 = wx.StaticText(panel, label="Enter URL")
        h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h1_sizer.AddStretchSpacer()
        h1_sizer.Add(text1, 0, wx.TOP, border=10)
        h1_sizer.AddStretchSpacer()

        self.url_input = wx.TextCtrl(panel, size=(400, 30))
        h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h2_sizer.AddStretchSpacer()
        h2_sizer.Add(self.url_input, 0, wx.ALL|wx.EXPAND, border=10)
        h2_sizer.AddStretchSpacer()

        btn1 = wx.Button(panel, 0, label="Get Info")
        h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h3_sizer.AddStretchSpacer()
        h3_sizer.Add(btn1, 0, wx.CENTER)
        h3_sizer.AddStretchSpacer()
        btn1.Bind(wx.EVT_BUTTON, self.GetInfo)

        self.video_title = wx.StaticText(panel, 0, label="Title: ")
        self.video_uploader = wx.StaticText(panel, 0, label="Uploader: ")
        quality = wx.StaticText(panel, 0, label="Quality: ")
        self.format_code = wx.ComboBox(panel, 0, size=(400, 30))
        sub_sizer = wx.GridBagSizer(3, 3)
        sub_sizer.Add(self.video_title, pos=(0,0), flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        sub_sizer.Add(self.video_uploader, pos=(1,0), flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        sub_sizer.Add(quality, pos=(2,0), flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        sub_sizer.Add(self.format_code, pos=(2,1), flag=wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        btn2 = wx.Button(panel, 0, label="Add to queue")
        h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h4_sizer.AddStretchSpacer()
        h4_sizer.Add(btn2, 0, wx.CENTER)
        h4_sizer.AddStretchSpacer()
        btn2.Bind(wx.EVT_BUTTON, self.AddToQueue)

        main_sizer.Add(h1_sizer, 0, wx.EXPAND)
        main_sizer.Add(h2_sizer, 0, wx.EXPAND)
        main_sizer.Add(h3_sizer, 0, wx.EXPAND)
        main_sizer.Add(sub_sizer, 0, wx.EXPAND)
        main_sizer.Add(h4_sizer, 0, wx.EXPAND)

        panel.SetSizer(main_sizer)


    def OnClose(self, e):
        self.Destroy()

    def GetInfo(self, e):
        self.video_info = UrlInfo.GetVideoInfo(self.url_input.GetValue())
        #test = self.video_info.start()
        #print(test)
        #self.video_info = Downloader.GetVideoInfo(self.url_input.GetValue())
        self.video_title.SetLabel("Title: "+ self.video_info['title'])
        self.video_uploader.SetLabel("Uploader: " + self.video_info['uploader'])
        self.format_code.Clear()

        format_list = []

        for i in self.video_info['formats']:
            audio = ""
            if i['asr'] == None:
                audio = " No Audio"
            else:
                audio = ""
        
            format_list.append((i['format'] + audio))

        self.format_code.Append([x for x in format_list])

    def AddToQueue(self, e):
        format_id = self.format_code.GetValue()
        format_id = format_id.split(" ")

        download_opts = {
            'status': "Paused",
            'format_id': format_id[0],
            'title': self.video_info['title'],
            'uploader': self.video_info['uploader'],
            'video_url': self.url_input.GetValue(),
        }
        UrlInfo.AddToQueue(download_opts)
        self.master.update_list()
        self.Destroy()
