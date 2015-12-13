import sys, os, random, datetime, time

X = 'x'
Y = 'y'
Z = 'z'
NONE = 'none'

try:
	import tkinter as tk
except:
	import Tkinter as tk
	
class GameSquare:
	def __init__(self, color='none', outer='none', text=''):
		self.color = color
		self.outer = outer
		self.text = text
	
	def setnew(self, color=None, outer=None, text=None):
		'''
		Set new value to color, outer or text.
		'''
		if color != None:
			self.color = color
		if outer != None:
			self.outer = outer
		if text != None:
			self.text = text
	
	
class d2GameScreen:
	def c_rect(self, x1, y1, x2, y2, color="white", outer="black", text=""):
		'''
		Do worry about this.
		'''
		self.can.create_rectangle(x1, y1, x2, y2, fill=color, outline=outer)
		self.can.create_text((x2-x1)/2+x1, (y2-y1)/2+y1, text=text)
	
	def update(self):
		'''
		Call this to update the gamescreen
		'''
		self.can.delete(tk.ALL)
		for i in range(int(self.rootgeo[0]/self.rectw)):
			for j in range(int(self.rootgeo[1]/self.recth)):
				if self.gameboard[i][j].color != 'none' and self.gameboard[i][j].outer != 'none':
					self.c_rect(i*self.rectw, j*self.recth, (i+1)*self.rectw, (j+1)*self.recth, self.gameboard[i][j].color, self.gameboard[i][j].outer, self.gameboard[i][j].text)
				if self.gameboard[i][j].color != 'none' and self.gameboard[i][j].outer == 'none':
					self.c_rect(i*self.rectw, j*self.recth, (i+1)*self.rectw, (j+1)*self.recth, self.gameboard[i][j].color, text=self.gameboard[i][j].text)
		
	def updateWhile(self):
		'''
		Call this to contunuesly call update.
		Not threading implemented. You must do that your self.
		'''
		while self.quitnow != True:
			time.sleep(0.001)
			self.update()
	
	def setsquare(self, x, y, square):
		'''
		Set square of x, y to value of square.
		square is not a color, rather a GameSquare instance.
		'''
		try:
			self.gameboard[x][y] = square
		except:
			raise IndexError("The x and/or y value is out of range.")
	
	def clear(self, blocks):
		'''
		Clear gameboard with blocks, blocks is a GameSquare. 
		Does not update screen. 
		'''
		self.gameboard = [[blocks for x in range(int(self.rootgeo[0]/self.rectw))] for y in range(int(self.rootgeo[1]/self.recth))]
	
	def __init__(self, gb='', roottitle="2D GameScreen", rootgeo=(500, 500), canbgcolor="white", xview=20, yview=20):
		'''
		gb -			The gameboard, leave '' to generate gameboard with defualt GameSquare.
		roottitle -		The root title.
		rootgeo - 		A tuple with x and y pixle values for window geometry.
		canbgcolor -	Defualt canvas color. Defaults to 'white'.
		xview - 		The number of squares from top to bottom of the window, horizontaly.
		yview -			The number of squares from top to bottom of the window, verticaly.
		'''
		rectwidth = int(rootgeo[0]/xview)
		rectheight = int(rootgeo[1]/yview)
		self.quitnow = False
		self.rectw = rectwidth
		self.recth = rectheight
		self.rootgeo = rootgeo
		if gb == '':
			self.gameboard  = [[GameSquare() for x in range(int(rootgeo[0]/rectwidth))] for y in range(int(rootgeo[1]/rectheight))]
		else:
			self.gameboard = gb
		rootgeostr = str(rootgeo[0])+"x"+str(rootgeo[1])
		self.root = tk.Tk()
		self.root.title(roottitle)
		self.root.geometry(rootgeostr)
		
		self.can = tk.Canvas(self.root, width=rootgeo[0], height=rootgeo[1], bg=canbgcolor)
		self.can.pack()
		self.update()
		self.mainloop = self.root.mainloop


class GameScreen:
	def __init__(self, zview=50, yview=50, xview=50, rootgeo=(500,500), roottitle="Pepper GameScreen", gb=None):
		self.rectwidth = int(self.rootgeo[0]/xview)
		self.rectheight = int(self.rootgeo[1]/yview)
		if gb != None:
			self.gameboard = gb
		else:
			self.gameboard = [[[GameSquare() for x in range(xview)] for y in range(yview)] for z in range(zview)]
		self.camerarotationdegrees = (0.00, 0.00, 0.00)
		self.root = tk.Tk()
		self.root.title(roottitle)
		self.root.geometry(str(rootgeo[0])+'x'+str(rootgeo[1]))
		
		self.canvas = tk.Canvas(self.root, width=rootgeo[0], height=rootgeo[1], bg='white')
		self.canvas.pack()
	
	def setgameboard(self, gb):
		self.gameboard = gb
	
	def rotatecamera(self, degrees, dir='x'):
		directions = ['x','y','z']
		self.camerarotationdegrees[direction.index(dir)] += degrees
	
	def clear(self):
		self.canvas.delete(tk.ALL)
		self.gameboard = [[[GameSquare() for x in range(xview)] for y in range(yview)] for z in range(zview)]
	
	def c_square(self, x1, y1, x2, y2, depth, fill='white', outer='black'):
		self.canvas.create_polygon(x1, y1, x2, y2, fill=fill, outline=outer)
		# calculate the z1 and z2 postions
		z1 = depth
		z2 = depth
		self.canvas.create_polygon(x1, z1, x2, z2, fill=fill, outline=outer)
		self.canvas.create_polygon(y1, z1, y2, z2, fill=fill, outline=outer)
		# I might need to add more...
	
	def update(self):
		self.clear()
		for i in range(len(self.gameboard)):
			for j in range(len(self.gameboard[i])):
				for k in range(len(self.gameboard[i][j])):
					if self.gameboard[i][j][k].color != 'none' and self.gameboard[i][j][k].outer != 'none':
						self.c_square(i*self.rectwidth,
									  j*self.rectheight,
									  (i+1)*self.rectwidth,
									  (j+1)*self.rectheight,
									  self.camerarotationdegrees,
									  fill=self.gameboard[i][j][k].color,
									  outline=self.gameboard[i][j][k].outer)
					if self.gameboard[i][j][k].color != 'none' and self.gameboard[i][j][k].outer == 'none':
						self.c_square(i*self.rectwidth,
									  j*self.rectheight,
									  (i+1)*self.rectwidth,
									  (j+1)*self.rectheight,
									  self.camerarotationdegrees,
									  fill=self.gameboard[i][j][k].color)
						print(str(i)+', '+str(j)+', '+str(k))
	
	def setpoint(self, x, y, z, block):
		self.gameboard[x][y][z] = block
	
	def c_rect(self, x1, y1, x2, y2, color='white', outer='', text=''):
		self.can.create_rectangle(x1, y1, x2, y2, fill=color, outline=outer)
		self.can.create_text(x1, y1, x2, y2, text=text)
		

class Game:
	def __init__(self, dem=3, poscolor='black', pos=[0,0], xaxis=20, yaxis=20, zaxis=20, geo=(500,500), title="Pepper Game", gb=None):
		self.poscolor = poscolor
		self.dem = dem
		self.postion = pos
		if dem == 3:
			if gb == None:
				gb = [[[GameSquare() for x in range(xaxis)] for y in range(yaxis)] for z in range(zaxis)]
			self.GS = GameScreen(xview=xaxis, yview=yaxis, zview=zxis, rootgeo=geo, roottitle=title, gb=gb)
			self.GS.gameboard[4][4][4].setnew(color='red', outer='black')
			self.postion.append(0)
		if dem == 2:
			if gb == None:
				gb = [[GameSquare() for x in range(xaxis)] for y in range(yaxis)]
			self.GS = d2GameScreen(xview=xaxis, yview=yaxis, rootgeo=geo, roottitle=title, gb=gb)
			self.GS.gameboard[4][4].setnew(color='red', outer='black')
		self.gameboard = self.GS.gameboard
		self.clear = self.GS.clear
		self.root = self.GS.root
		self.update()
		self.GS.root.bind("<Key>", self.keyPressed)
		self.GS.update()
		
	def keyPressed(self, event):
		if event.char == 'w':
			if self.dem == 3:
				self.move(0,1,0)
			if self.dem == 2:
				self.move(0,1)
		if event.char == 's':
			if self.dem == 3:
				self.move(0,-1,0)
			if self.dem == 2:
				self.move(0,-1)
		if event.char == 'a':
			if self.dem == 3:
				self.move(-1,0,0)
			if self.dem == 2:
				self.move(-1,0)
		if event.char == 'd':
			if self.dem == 3:
				self.move(1,0,0)
			if self.dem == 2:
				self.move(1,0)
		if event.char == ' ':
			if self.dem == 3:
				self.move(0,0,1)
		
	def update(self):
		self.GS.update()
		if self.GS.gameboard[self.postion[0]][self.postion[1]].outer != 'none':
			self.GS.c_rect(self.postion[0]*self.GS.rectw, self.postion[1]*self.GS.recth, (self.postion[0]+1)*self.GS.rectw, (self.postion[1]+1)*self.GS.recth, self.poscolor, self.GS.gameboard[self.postion[0]][self.postion[1]].outer, self.GS.gameboard[self.postion[0]][self.postion[1]].text)
		else:
			self.GS.c_rect(self.postion[0]*self.GS.rectw, self.postion[1]*self.GS.recth, (self.postion[0]+1)*self.GS.rectw, (self.postion[1]+1)*self.GS.recth, self.poscolor, self.GS.gameboard[self.postion[0]][self.postion[1]].text)
		
	def move(self, x, y, z=None):
		self.postion[0] += x
		self.postion[1] += y
		if z != None:
			self.postion[2] += z
		self.update()
		

d3GameScreen = GameScreen

if __name__ == '__main__':
	app = Game()
	app.GS.root.mainloop()
