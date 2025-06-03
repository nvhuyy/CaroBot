import turtle
import tkinter as tk
import random
import heapq
import copy

priority_queue = []
cell_info_map = {}  # (x, y) → (score, [a, b, c, d])
recent_moves = []
priority_queue_O = []
cell_info_map_O = {}

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
def isWinn(board, symbol, numToWin=5):
    size = len(board)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # dọc, ngang, chéo chính, chéo phụ

    for i in range(size):
        for j in range(size):
            if board[i][j] != symbol:
                continue
            for dx, dy in directions:
                count = 1
                x, y = i + dx, j + dy
                while 0 <= x < size and 0 <= y < size and board[x][y] == symbol:
                    count += 1
                    if count == numToWin:
                        return True
                    x += dx
                    y += dy
    return False

def click(x, y):
    global board, ii, recent_moves

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

            recent_moves.append((intx, inty))
            if len(recent_moves) > 2:
                recent_moves.pop(0)

    # Debug in ra bàn cờ
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
    depth = 4  # Có thể giảm còn 3 nếu quá chậm

    score, move = minimax(copy.deepcopy(board), depth, True, 'X', float('-inf'), float('inf'))

    if move is None:
        # Fallback: lấy nước tốt nhất từ hàng đợi hiện tại
        pq, cell_map = initialize_priority_queue(board, my='X', enemy='O')
        move, _, _ = get_best_move_from_queue(board, pq, cell_map)

    if move:
        x, y = move
        board[x][y] = 'X'
        drawX(x, y)
        clickedSlot.append((x, y))

        if isWin():
            winWindow()
        else:
            ii = 0




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
    to_win = 5 - count_my if count_my > 0 else 5
    to_lose = 5 - count_enemy if count_enemy > 0 else 5
    to_defend = 2 - block_my if count_my > 0 else 0
    to_block = 2 - block_enemy if count_enemy > 0 else 0

    return to_win, to_lose, to_defend, to_block


def priority_level(to_win, to_lose, to_defend, to_block):
    if to_win == 1:
        return 1
    if to_lose == 1:
        return 1.2
    if to_win == 2 and to_defend == 2:
        return 1.3
    if to_win == 2 and to_defend == 1:
        return 1.4
    if to_lose < to_block and to_lose != 0:
        return 1.5
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


def attack_deffend_level(to_win, to_lose, to_defend, to_block):
    if to_win <= 0:
        return 7
    if to_win == 1:
        return 6
    if to_win == 2 and to_defend == 2:
        return 5
    if to_win == 2 and to_defend == 1:
        return 4
    if to_win <= to_defend and to_win != 0:
        return 3
    if to_defend == 2 and to_win == 3:
        return 2
    if to_defend == 2 and to_win == 4:
        return 1
    if to_lose <= 0:
        return -7
    if to_lose == 1:
        return -6
    if to_lose < to_block and to_lose != 0:
        return -5
    if to_lose == to_block and to_lose != 0:
        return -4
    if to_block == 2 and to_lose != 0:
        return -3
    if to_defend == 1 and to_lose < 4 and to_lose != 0:
        return -2
    return -1



def evaluate_all_directions(board, x, y, my='X', enemy='O'):
    directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]  # dọc, ngang, chéo chính, chéo phụ
    priorities = []

    for dx, dy in directions:
        tw, tl, td, tb = evaluate_direction(board, x, y, dx, dy, my, enemy)
        prio = priority_level(tw, tl, td, tb)
        priorities.append(prio)

    return priorities  # [a, b, c, d]

def compute_score_and_prios(board, x, y, my='X', enemy='O'):
    prios = evaluate_all_directions(board, x, y, my, enemy)
    a, b, c, d = sorted(prios)
    score = a * 1_000_000 + b * 10_000 + c * 100 + d
    return score, prios

def evaluate_all_ad(board, x, y, my='X', enemy='O'):
    directions = [ (1, 0), (0, 1), (1, 1), (1, -1) ]  # dọc, ngang, chéo chính, chéo phụ
    priorities = []

    for dx, dy in directions:
        tw, tl, td, tb = evaluate_direction(board, x, y, dx, dy, my, enemy)
        prio = attack_deffend_level(tw, tl, td, tb)
        priorities.append(prio)

    return priorities  # [a, b, c, d]
def compute_score_and_prios_ad(board, x, y, my='X', enemy='O'):
    prios = evaluate_all_ad(board, x, y, my, enemy)
    a, b, c, d = sorted(prios)
    score = a * 1_000_000 + b * 10_000 + c * 100 + d
    return score, prios


def initialize_priority_queue(board, my='X', enemy='O'):
    priority_queue = []
    cell_info_map = {}
    
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '_':
                score, prios = compute_score_and_prios(board, x, y, my, enemy)
                cell_info_map[(x, y)] = (score, prios)
                heapq.heappush(priority_queue, (score, x, y))
    
    return priority_queue, cell_info_map

def update_priority_queue(board, move_x, move_y, priority_queue, cell_info_map, my='X', enemy='O'):
    affected = set()
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        for k in range(-6, 7):
            x = move_x + k * dx
            y = move_y + k * dy
            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                if board[x][y] == '_':
                    affected.add((x, y))

    for x, y in affected:
        score, prios = compute_score_and_prios(board, x, y, my, enemy)
        cell_info_map[(x, y)] = (score, prios)
        heapq.heappush(priority_queue, (score, x, y))

def update_priority_around_recent_moves(board, recent_moves, priority_queue, cell_info_map, my='X', enemy='O'):
    for x, y in recent_moves:
        update_priority_queue(board, x, y, priority_queue, cell_info_map, my, enemy)

def get_best_move_from_queue(board, priority_queue, cell_info_map):
    while priority_queue:
        score, x, y = heapq.heappop(priority_queue)
        if (x, y) in cell_info_map and cell_info_map[(x, y)][0] == score and board[x][y] == '_':
            prios = cell_info_map[(x, y)][1]
            del cell_info_map[(x, y)]
            return (x, y), score, prios
    return None, None, None


def minimax(board, depth, maximizing_player, my_symbol, alpha, beta):
    current_symbol = my_symbol if maximizing_player else ('O' if my_symbol == 'X' else 'X')

    #  Nếu đã thắng/thua thì trả điểm ngay
    if isWinn(board, current_symbol):
        return (float('inf') if maximizing_player else float('-inf')), None

    if depth == 0:
        return evaluate(board, my_symbol), None

    pq, cell_map = initialize_priority_queue(board, my=current_symbol, enemy=('O' if current_symbol == 'X' else 'X'))

    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None
    count = 0

    while count < 4:
        move, score, prios = get_best_move_from_queue(board, pq, cell_map)
        if move is None:
            break
        x, y = move
        new_board = copy.deepcopy(board)
        new_board[x][y] = current_symbol

        # Kiểm tra thắng sau khi đặt nước đi
        if isWinn(new_board, current_symbol):
            return (float('inf') if maximizing_player else float('-inf')), (x, y)

        eval_score, _ = minimax(new_board, depth - 1, not maximizing_player, my_symbol, alpha, beta)

        if maximizing_player:
            if eval_score > best_score:
                best_score = eval_score
                best_move = (x, y)
            alpha = max(alpha, best_score)
        else:
            if eval_score < best_score:
                best_score = eval_score
                best_move = (x, y)
            beta = min(beta, best_score)

        if beta <= alpha:
            break

        count += 1

    return best_score, best_move

def evaluate(board, my_symbol):
    enemy_symbol = 'O' if my_symbol == 'X' else 'X'
    pq_enemy, map_enemy = initialize_priority_queue(board, my=enemy_symbol, enemy=my_symbol)

    move, _, _ = get_best_move_from_queue(board, pq_enemy, map_enemy)
    if move is not None:
        x, y = move
        score, _ = compute_score_and_prios_ad(board, x, y, my=enemy_symbol, enemy=my_symbol)
        return score
    return 0




if __name__ == "__main__":
    global size, winner
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
