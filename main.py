import wx 
from src.main import MainApplication

if __name__ == '__main__':
    app = wx.App() 
    window = MainApplication(None, id=wx.ID_ANY, title="ytdl-wxPython", size=(1000, 500))
    window.Show(True) 
    app.MainLoop()
