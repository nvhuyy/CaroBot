import turtle
import tkinter as tk
import random

global numToWin
global ii
ii = 0

def isWin():
    global winner
    directions = [(1, -1), (1, 0), (1, 1), (0, 1)]
    for i, j in clickedSlot:
        for dx, dy in directions:
            count = 1
            x, y = i + dx, j + dy
            while 0 <= x < size and 0 <= y < size and board[x][y] == board[i][j]:
                count += 1
                x += dx
                y += dy
                if count == numToWin:
                    winner = board[i][j]
                    print("winner is", winner)
                    return True
    return False

def click(x, y):
    global board, ii
    if x >= 0 and y >= 0:
        intx, inty = int(x), int(y)
        if 0 <= intx < size and 0 <= inty < size:
            if (intx, inty) in clickedSlot:
                return
            clickedSlot.append((intx, inty))
            if ii == 0:
                board[intx][inty] = 'O'
                drawO(intx, inty)
                ii = 1
            else:
                board[intx][inty] = 'X'
                drawX(intx, inty)
                ii = 0        

    for j in range(len(board)):
        for i in range(len(board)):
            print(f"{board[i][j]}|", end="")
        print()
    print()

    if isWin():
        winWindow()
        return

    if ii == 1:
        botMove()
        evaluateBoard(board)
        turtle.update()

def drawX(x, y):
    t = turtle.Turtle()
    t.pu()
    t.goto(x + 0.2, y + 0.2)
    t.pd()
    t.color("red")
    t.pensize(5)
    t.goto(x + 0.8, y + 0.8)
    t.pu()
    t.goto(x + 0.8, y + 0.2)
    t.pd()
    t.goto(x + 0.2, y + 0.8)
    t.pu()
    t.ht()

def drawO(x, y):
    t = turtle.Turtle()
    t.pu()
    t.goto(x + 0.5, y + 0.2)
    t.pd()
    t.color("blue")
    t.pensize(5)
    t.circle(0.3)
    t.pu()
    t.ht()

def winWindow():
    global winner
    root = tk.Tk()
    root.geometry("250x40+550+350")
    root.title("Who won?")
    tk.Label(root, text=f"{winner} won").pack()
    root.mainloop()

def init(size):
    global clickedSlot
    clickedSlot = []
    global board
    board = [['_'] * size for _ in range(size)]

    screen = turtle.Screen()
    screen.setup(800, 640)
    screen.bgcolor("light blue")
    screen.title("CARO")
    screen.tracer(0)
    screen.update()
    turtle.update()
    screen.setworldcoordinates(-1, size + 1, size + 1, -1)

    border = turtle.Turtle()
    border.pensize(4)
    border.pu()
    for i in range(0, size + 1):
        border.goto(i, 0)
        border.pd()
        border.goto(i, size)
        border.pu()
    for i in range(0, size + 1):
        border.goto(0, i)
        border.pd()
        border.goto(size, i)
        border.pu()
    border.ht()

    screen.onclick(click)
    screen.listen()
    screen.mainloop()

def closeInputWindow(event=None):
    global size
    size = int(entry.get())
    root.destroy()

def randomBotMove():
    global ii
    empty_slots = [(i, j) for i in range(size) for j in range(size) if board[i][j] == '_']
    if not empty_slots:
        return
    move = random.choice(empty_slots)
    clickedSlot.append(move)
    i, j = move
    board[i][j] = 'X'
    drawX(i, j)
    ii = 0

    if isWin():
        winWindow()

def botMove():
    global ii
    best_cell, _, _ = find_best_move(board, my='X', enemy='O')
    if best_cell:
        i, j = best_cell
        board[i][j] = 'X'
        clickedSlot.append((i, j))
        drawX(i, j)

        if isWin():
            winWindow()
            return

        ii = 0  # chuyển lượt về người chơi


def evaluate_direction(board, x, y, dx, dy, my='X', enemy='O'):
    count_my = 0
    count_enemy = 0
    block_my = 0
    block_enemy = 0

    # ----- Kiểm tra hướng của 'my' -----
    # Phía trái
    i, j = x - dx, y - dy
    blocked = False
    while 0 <= i < len(board) and 0 <= j < len(board[0]):
        if board[i][j] == my:
            count_my += 1
        elif board[i][j] == enemy:
            block_my += 1
            blocked = True
            break
        else:
            break
        i -= dx
        j -= dy
    if not blocked and not (0 <= i < len(board) and 0 <= j < len(board[0])):
        block_my += 1  # bị chặn bởi tường

    # Phía phải
    i, j = x + dx, y + dy
    blocked = False
    while 0 <= i < len(board) and 0 <= j < len(board[0]):
        if board[i][j] == my:
            count_my += 1
        elif board[i][j] == enemy:
            block_my += 1
            blocked = True
            break
        else:
            break
        i += dx
        j += dy
    if not blocked and not (0 <= i < len(board) and 0 <= j < len(board[0])):
        block_my += 1

    # ----- Kiểm tra hướng của 'enemy' -----
    # Phía trái
    i, j = x - dx, y - dy
    blocked = False
    while 0 <= i < len(board) and 0 <= j < len(board[0]):
        if board[i][j] == enemy:
            count_enemy += 1
        elif board[i][j] == my:
            block_enemy += 1
            blocked = True
            break
        else:
            break
        i -= dx
        j -= dy
    if not blocked and not (0 <= i < len(board) and 0 <= j < len(board[0])):
        block_enemy += 1

    # Phía phải
    i, j = x + dx, y + dy
    blocked = False
    while 0 <= i < len(board) and 0 <= j < len(board[0]):
        if board[i][j] == enemy:
            count_enemy += 1
        elif board[i][j] == my:
            block_enemy += 1
            blocked = True
            break
        else:
            break
        i += dx
        j += dy
    if not blocked and not (0 <= i < len(board) and 0 <= j < len(board[0])):
        block_enemy += 1

    # ----- Tính các chỉ số -----
    to_win = 5 - count_my if count_my > 0 else 0
    to_lose = 5 - count_enemy if count_enemy > 0 else 0
    to_defend = 2 - block_my if count_my > 0 else 0
    to_block = 2 - block_enemy if count_enemy > 0 else 0

    return to_win, to_lose, to_defend, to_block


def priority_level(to_win, to_lose, to_defend, to_block):
    if to_win == 1:
        return 1
    if to_lose == 1:
        return 1.1
    if to_lose < to_block and to_lose != 0:
        return 1.2
    if to_lose == to_block and to_lose != 0:
        return 2
    if to_win <= to_defend and to_win != 0:
        return 3
    if to_defend == 2 and to_win == 3:
        return 3.2
    if to_defend == 2 and to_win == 4:
        return 4
    if to_block == 2 and to_lose != 0:
        return 5
    if to_defend == 1 and to_lose < 4 and to_lose != 0:
        return 6
    return 7

def get_best_direction(board, x, y, my='X', enemy='O'):
    directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]  # dọc, ngang, chéo chính, chéo phụ
    best = None
    best_priority = 8  # khởi đầu cao hơn mức thấp nhất
    best_info = None

    for dx, dy in directions:
        tw, tl, td, tb = evaluate_direction(board, x, y, dx, dy, my, enemy)
        prio = priority_level(tw, tl, td, tb)

        if prio < best_priority:
            best = (dx, dy)
            best_priority = prio
            best_info = (tw, tl, td, tb)

    return best, best_info, best_priority

def evaluate_all_directions(board, x, y, my='X', enemy='O'):
    directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]  # dọc, ngang, chéo chính, chéo phụ
    priorities = []

    for dx, dy in directions:
        tw, tl, td, tb = evaluate_direction(board, x, y, dx, dy, my, enemy)
        prio = priority_level(tw, tl, td, tb)
        priorities.append(prio)

    return priorities  # [a, b, c, d]

def find_best_move(board, my='X', enemy='O'):
    best_cell = None
    best_score = float('inf')
    best_prios = None

    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '_':
                prios = evaluate_all_directions(board, x, y, my, enemy)
                a, b, c, d = sorted(prios)  # sắp xếp để a là hướng tốt nhất
                score = a * 1_000_000 + b * 10_000 + c * 100 + d

                if score < best_score:
                    best_score = score
                    best_cell = (x, y)
                    best_prios = (a, b, c, d)

    return best_cell, best_score, best_prios



def evaluateBoard(board):
    cell, score, prios = find_best_move(board)
    if cell:
        x, y = cell
        print(f"\n=> O tot nhat: ({x}, {y}) voi diem: {score}")
        print(f"  Cac muc do uu tien: {prios}")
    else:
        print("Khong co nuoc di hop le.")



if __name__ == "__main__":
    global size, winner, numToWin
    numToWin = 5  # Mặc định số quân để thắng là 5

    root = tk.Tk()
    root.geometry("250x70+550+350")
    root.title("Input")
    tk.Label(root, text="Size of board:").pack()
    entry = tk.Entry(root)
    entry.pack()
    tk.Button(root, text="OK", command=closeInputWindow).pack()
    root.mainloop()

    if numToWin > size:
        print("Error")
    else:
        init(size)
