#   Simple program for serializing/unserializing JSON
#
#   Author: Milos Milutinovic
#
#   License: GNU GPL

import wx, json

class Pyjson(wx.Frame):

    appVersion = '0.2.6 beta'

    def __init__(self, *args, **kwargs):
        super(Pyjson,self).__init__(*args, **kwargs)
        self.InitUI()

        self.SetSize((768,800))
        self.SetTitle('JSON Editor')
        self.Centre()
        self.Show()


    def InitUI(self):
        #menubar
        menubar = wx.MenuBar()
        #file menu
        fileMenu = wx.Menu()
        fmClose = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        #edit menu
        editMenu = wx.Menu()
        emUnserialize = editMenu.Append(wx.ID_ANY, '&Unserialize', 'Unserialize JSON')
        emSerialize = editMenu.Append(wx.ID_ANY, 'S&erialize', 'Serialize JSON')

        editMenu.AppendSeparator()
        emClear = editMenu.Append(wx.ID_ANY, '&Clear', 'Clear All')

        menubar.Append(editMenu, '&Edit')
        #help menu
        helpMenu = wx.Menu()
        hmAbout = helpMenu.Append(wx.ID_ABOUT, 'About', 'About this application')
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

        #menu bindings
        self.Bind(wx.EVT_MENU, self.OnQuit, fmClose)

        self.Bind(wx.EVT_MENU, self.unserialize, emUnserialize)
        self.Bind(wx.EVT_MENU, self.serialize, emSerialize)
        self.Bind(wx.EVT_MENU, self.clearAll, emClear)

        self.Bind(wx.EVT_MENU, self.showAbout, hmAbout)

        #toolbar
        toolbar = self.CreateToolBar()

        unserIcon = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_TOOLBAR, (16,16))
        unserTool = toolbar.AddSimpleTool(wx.ID_ANY, unserIcon, 'Unserialize', 'Unserialize JSON')

        serIcon = wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_TOOLBAR, (16,16))
        serTool = toolbar.AddSimpleTool(wx.ID_ANY, serIcon, 'Serialize', 'Serialize JSON')

        clearIcon = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_TOOLBAR, (16,16))
        clearTool = toolbar.AddSimpleTool(wx.ID_ANY, clearIcon, 'Clear', 'Clear All')

        exitIcon = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16,16))
        qTool = toolbar.AddSimpleTool(wx.ID_ANY, exitIcon, 'Quit', 'Quit Application')

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnQuit, qTool)

        self.Bind(wx.EVT_TOOL, self.unserialize, unserTool)
        self.Bind(wx.EVT_TOOL, self.serialize, serTool)
        self.Bind(wx.EVT_TOOL, self.clearAll, clearTool)

        #main area
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        inputBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inputText = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        inputBox.Add(self.inputText, proportion=1, flag=wx.EXPAND)
        vbox.Add(inputBox, proportion=1,  flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)

        vbox.Add((-1,5)) #spacer

        outputBox = wx.BoxSizer(wx.HORIZONTAL)
        self.outputText = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        outputBox.Add(self.outputText, proportion=1, flag=wx.EXPAND)
        vbox.Add(outputBox, proportion=3,  flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)

        vbox.Add((-1,10))

        panel.SetSizer(vbox)

        #status bar
        self.sb = self.CreateStatusBar()
        self.setStatusBar('Ready...')

    def unserialize(self,e):
        inputText = self.inputText.GetValue()

        if self.validate(inputText):

            parsed = json.loads(inputText) #unserialize
            #serialize, but pretty print
            unserialized = json.dumps(parsed, indent=4, sort_keys=True)

            self.outputText.Clear()
            self.outputText.SetValue(unserialized)

            self.setStatusBar('Unserialized')

        else:
            wx.MessageBox('Invalid input data', 'Warning', wx.OK | wx.ICON_EXCLAMATION)

    def serialize(self,e):
        inputText = self.outputText.GetValue()

        if self.validate(inputText):

            #convert to JSON object
            parsed = json.loads(inputText)

            #convert back to string
            serialized = json.dumps(parsed)

            self.outputText.Clear()
            self.inputText.SetValue(serialized)

            self.setStatusBar('Serialized')

        else:
            wx.MessageBox('Invalid input data', 'Warning', wx.OK | wx.ICON_EXCLAMATION)

    def validate(self,data):
        '''
            Check if valid data was passed
        '''
        if len(data) == 0:
            return False #no need to process further

        #check for valid json
        try:
            json.loads(data)
            return True;

        except ValueError as e:
            #if the exception was thrown, input data is not valid JSON
            return False

    def clearAll(self,e):
        #clear both TextCtrl
        self.inputText.Clear()
        self.outputText.Clear()

    def setStatusBar(self,status):
        self.sb.SetStatusText(status)

    def showAbout(self,e):
        description = '''JSON Editor is a program for unserializing and serializing
        JSON
        '''

        license = '''
    JSON Editor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
        '''

        info = wx.AboutDialogInfo()

        #set icon
        info.SetName('JSON Editor')
        info.SetVersion(self.appVersion)
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 Milos Milutinovic')
        info.SetWebSite('http://miloske.tk')
        info.SetLicence(license)
        info.AddDeveloper('Milos Milutinovic <milos.milutinovic@live.com>')

        wx.AboutBox(info)

    def OnQuit(self,e):
        self.Close()



app = wx.App()
Pyjson(None)
app.MainLoop()
