import sys, os, pepper, editor

import server as SERVER

try:
	from tkinter import *
except:
	from Tkinter import *

class StartGame:
	def selcur(self):
		self.curselworld = self.serverselect.curselection()
		self.root.destroy()
	
	def addserver(self):
		pass
	
	def delcurrent(self):
		pass
	
	def __init__(self):
		self.curselworld = ""
		self.root = Tk()
		self.root.title("Wizards Alpha: Start Game")
		self.root.geometry("400x400")
		
		self.serverselect = Listbox(self.root, width=20, height=10)
		self.selectcurbutton = Button(self.root, text="Select", command=self.selcur)
		self.addserverbutton = Button(self.root, text="Add Server", command=self.addserver)
		self.delcurbutton = Button(self.root, text="Delete", command=self.delcurrent)
		self.commandline = Entry(self.root, width=30)
		self.commandline.grid(row=0, column=0, columnspan=30)
		self.serverselect.grid(row=1, column=0, columnspan=20, rowspan=10)
		self.selectcurbutton.grid(row=1, column=25)
		self.addserverbutton.grid(row=2, column=25)
		self.delcurbutton.grid(row=3, column=25)
		
	def getconnection(self):
		self.root.mainloop()
		return self.curselworld

class App:
	def __init__(self, connection):
		self.name = editor.load('username.txt',errors=True,cf=True)
		self.curdata = ""; self.prevdata = ""
		self.root = pepper.d2GameScreen(rootgeo=(500,400),roottitle="Wizards Alpha 0.1")
		self.root.clear(pepper.GameSquare('lime green'))
		self.root.root.bind("<Key>", self.keyPress)
		self.root.root.bind("<Button>", self.buttonPress)
		self.server = SERVER.Server()
		self.data = "Login from '"+self.name+"';"; self.update()
		
	def buttonPress(self, event):
		self.curdata += "MC:'"+str(event.num)+"',"+str(event.x)+","+str(event.y)+";"
		self.update()
		
	def keyPress(self, event):
		if event.char != '':
			self.curdata += "KP:'"+event.char+"';"
		self.update()
		
	def update(self):
		if self.curdata != '':
			s = self.server.send("U:'"+self.name+"' "+self.curdata)
			print(s)
			if s == "Your already loged in.":
				print(s);quit(0)
			if s == "Your are already loged out.":
				print(s);quit(0)
			self.prevdata = editor.copy(self.curdata)
			self.curdata = ""

	
if __name__ == "__main__":
	app = App(StartGame().getconnection())
	app.root.mainloop()
	app.data = "Disconnect from '"+app.name+"';"; app.update()
