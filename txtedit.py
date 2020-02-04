import wx,json
from os import path,mkdir 

class File:
	def __init__(self,name = 'untitled.txt',dirname='',isSaved = False):
		try:
			mkdir('./assets')
		except:
			pass
		try:
			mkdir('./temp')
		self.fileName = name
		self.dirName = dirname
		self.path = path.join(self.dirName,self.fileName)
		self.isSaved = isSaved
	# @property
	# def fileName(self):
		# return self.__fileName
	# @fileName.setter
	# def fileName(self,x):
		# self.__fileName = x
	
	# @property
	# def path(self):
		# return self.__path 
	# @path.setter
	# def path(self,x):
		# self.__path = x
	
	
class MyWindow(wx.Frame,File):
	def __init__(self,parent,title):
		#initialising baseclass 
		wx.Frame.__init__(self,parent,title=title,size=(800,600))
		File.__init__(self)
		#Creating Multiline Textbox
		self.control = wx.TextCtrl(self,style =wx.TE_MULTILINE)
		
		self.title = title
		
		#Creates StatusBar 
		self.CreateStatusBar()
		
		#Create Menu which holds menu items such as new,save,open etc.
		filemenu = wx.Menu()
		
		#Creates New option
		menuNew = filemenu.Append(wx.ID_NEW,'&New','Creates new file')
		#filemenu.AppendSeparator()
		
		#Creates Open option
		menuOpen = filemenu.Append(wx.ID_OPEN,'&Open','Opens your Previous work')
		#filemenu.AppendSeparator()
		
		#Creates Save option
		menuSave = filemenu.Append(wx.ID_SAVE,'&Save','Saves your current work in file')
		#filemenu.AppendSeparator()
		
		#Create Saveas option 
		menuSaveas = filemenu.Append(wx.ID_SAVEAS,'&Save as','Save your work with differnt name or place')
		
		#Creates About option 
		menuAbout = filemenu.Append(wx.ID_ABOUT,'&About','Information about the program')
		#filemenu.AppendSeparator()
		
		#creates Exit option
		menuExit = filemenu.Append(wx.ID_EXIT,'&Exit',"Terminate the program")
		
		#Genrates Menubar add our file menu in it
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,'&File')
		self.SetMenuBar(menuBar)
		
		#Binding Events to all options
		self.Bind(wx.EVT_MENU,self.OnNew,menuNew)
		self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
		self.Bind(wx.EVT_MENU,self.OnSave,menuSave)
		self.Bind(wx.EVT_MENU,self.OnSaveas,menuSaveas),
		self.Bind(wx.EVT_MENU, self.OnAbout,menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit,menuExit)
		
		
		self.Show(True)
		
	def saveState(self):
		with open('./state','r') as f:
			data = f.read()
		if data != '':
			data = json.loads(data+'}')
			if self.path in data:
				data[self.path]={'fileName':self.fileName,'dirName':self.dirName,'isSaved':self.isSaved,'conFileName':'temp.'+self.fileName}
				string = json.dumps(data)
				with open('./state','w') as f:
					f.write(string[:-1])
				with open(('./temp/temp.'+self.fileName),'w') as f:
					f.write(self.control.GetValue())
			else:
				string = json.dumps({self.path:{'fileName':self.fileName,'dirName':self.dirName,'isSaved':self.isSaved,'conFileName':('temp.'+self.fileName)}})
				with open('./state','a') as f:
					f.write(','+string[1:-1])
				with open(('./temp/temp.'+self.fileName[:-4]),'w') as f:
					f.write(self.control.GetValue())
		else:
			string = json.dumps({self.path:{'fileName':self.fileName,'dirName':self.dirName,'isSaved':self.isSaved,'conFileName':'temp.'+self.fileName}})
			with open('./state','a') as f:
				f.write('{"0":"0"')
				f.write(','+string[1:-1])
			with open(('./temp/temp.'+self.fileName),'w') as f:
				f.write(self.control.GetValue())
	
	
	def OnNew(self,e):
		self.saveState()
		File.__init__(self)
		self.SetTitle(self.title)
		self.control.SetValue('')
		
	def OnOpen(self,e):
		dlg = wx.FileDialog(self,'Choose a file','','',"TEXT files (.txt)|*.txt",wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.saveState()
			File.__init__(self,dlg.GetFilename(),dlg.GetDirectory(),True)
			with open(self.path,'r') as f:
				s = f.read()
				self.control.SetValue(s)
				self.SetTitle(' '+self.fileName+' - '+self.title)
		dlg.Destroy()
			
	def OnSave(self,e):
		if self.isSaved:
			self.SetTitle(' '+self.fileName+' - '+self.title)
			print(self.path)
			with open(self.path,'w')as f:
				f.write(self.control.GetValue())
		else:
			dlg = wx.FileDialog(self,'choose a directory','','',"TEXT files (*.txt)|*.txt",wx.FD_SAVEwx.FD_OVERWRITE_PROMPT)
			if dlg.ShowModal() == wx.ID_OK:
				self.saveState()
				File.__init__(dlg.GetFilename(),dlg.GetDirectory(),True)
				self.SetTitle(' '+self.fileName+' - '+self.title)
				with open(self.path,'w') as f:
					f.write(self.control.GetValue())
			dlg.Destroy()
			
	def OnSaveas(self,e):
		dlg = wx.FileDialog(self,'choose a directory',self.dirName,self.fileName,style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			self.saveState()
			File.__init__(self,dlg.GetFilename(),dlg.GetDirectory(),True)
			self.SetTitle(' '+self.fileName+' - '+self.title)
			with open(self.path,'w') as f:
				f.write(self.control.GetValue())
		dlg.Destroy()
 	
	def OnAbout(self,e):
		dlg = wx.MessageDialog(self,'A Small TE','About',wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
	def OnExit(self,e):
		self.saveState()
		self.Close(True)
app = wx.App(False)
frame = MyWindow(None,"SuperEditor v0.01")
app.MainLoop()