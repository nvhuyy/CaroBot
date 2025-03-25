import turtle
import tkinter as tk

global numToWin # số quân liên tiếp để thắng
global ii # để luân phiên đánh quân
ii = 0

def isWin():
	global winner
	directions = [(1,-1), (1,0), (1,1), (0,1)] # 4 hướng để ktra numToWin dấu liên tiếp
	for i,j in clickedSlot:
		for dx,dy in directions:
			count = 1
			x, y = i+dx, j+dy
			while 0<=x<size and 0<=y<size and board[x][y]==board[i][j]: # cột x hàng y
				count += 1
				x += dx
				y += dy
				if count == numToWin :
					winner = board[i][j]
					print("winner is", winner)
					return True
	return False
			
def click(x,y):
	global board
	global ii
	if x>=0 and y>=0 :
		intx,inty = int(x),int(y)     	
		if 0<=intx<=size-1 and 0<=inty<=size-1 :
			if (intx,inty) in clickedSlot:
				return  
			clickedSlot.append((intx,inty))
			if ii == 0 :
				board[intx][inty] = 'O'
				drawO(intx,inty)
				ii = 1
			else: 
				board[intx][inty] = 'X'
				drawX(intx,inty)
				ii = 0
	print(clickedSlot)
	for j in range(len(board)):
		for i in range(len(board)):
			print(f"{board[i][j]}|", end="")
		print()
	print()
	if isWin() :
		winWindow()
	
def drawX(x,y):
	t = turtle.Turtle()
	t.pu()
	t.goto(x+0.2,y+0.2)
	t.pd()
	t.color("red")
	t.pensize(5)
	t.goto(x+0.8,y+0.8)
	t.pu()
	t.goto(x+0.8,y+0.2)
	t.pd()
	t.goto(x+0.2,y+0.8)
	t.pu()
	t.ht()
	
def drawO(x,y):
	t = turtle.Turtle()
	t.pu()
	t.goto(x+0.5,y+0.2)
	t.pd()
	t.color("blue")
	t.pensize(5)
	t.circle(0.3)
	t.pu()
	t.ht()

def winWindow():
	global winner
	root = tk.Tk()
	root.geometry("250x40+550+350") # widthxheight+x+y
	root.title("Who won?")
	tk.Label(root, text=f"{winner} won").pack()
	root.mainloop()
	
def init(size):
	global clickedSlot
	clickedSlot = [] # chứa toạ độ các ô đã click
	global board 
	board = [['_']*size for _ in range(size)]
	
	screen = turtle.Screen()
	screen.setup(800, 640)
	screen.bgcolor("light blue")
	screen.title("CARO")
	screen.tracer(0)
	screen.update()
	turtle.update()
	screen.setworldcoordinates(-1,size+1,size+1,-1)

    # vẽ bàn cờ
	border = turtle.Turtle()
	border.pensize(4)
	#border.speed(9)
	border.pu()
	for i in range(0,size+1):
		border.goto(i,0)
		border.pd()
		border.goto(i,size)
		border.pu()
	for i in range(0,size+1):
		border.goto(0,i)
		border.pd()
		border.goto(size,i)
		border.pu()
	border.ht()
	
	screen.onclick(click)
	screen.listen()
	screen.mainloop()
	
def closeInputWindow(event=None):
	global size, numToWin
	size = int(entry.get())
	numToWin = int(entry1.get())
	root.destroy()

if __name__ == "__main__" :
	global size, winner

    # vẽ cửa sổ nhập input
	root = tk.Tk()
	root.geometry("250x110+550+350")
	root.title("Input")
	tk.Label(root, text="Size of board:").pack()
	entry = tk.Entry(root)
	entry.pack()
	tk.Label(root, text="Number of consecutive pieces to win:").pack()
	entry1 = tk.Entry(root)
	entry1.pack()
	tk.Button(root, text="OK", command=closeInputWindow).pack()
	root.mainloop()

	if numToWin > size :
		print("Error")
	else:
		init(size)