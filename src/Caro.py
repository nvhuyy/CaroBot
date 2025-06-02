import turtle 
import tkinter as tk
#import random

AI = 'O'
HUMAN = 'X'
EMPTY = '_'
MAX_DEPTH = 3
XP = HUMAN # X_PIECE
OP = AI

global numToWin, size, winner, board, clickedSlot, level
global recent_move # only for Minimax
recent_move = [(-1, -1), (-1, -1)]  # last move of human and AI

def is_board_full() :
    global board
    return len(clickedSlot) == size*size
   
def isWin(player):
    directions = [(1,-1), (1,0), (1,1), (0,1)]
    for i,j in clickedSlot:
        if board[i][j]==player:
            for dx,dy in directions:
                count = 1
                x, y = i+dx, j+dy
                while 0<=x<size and 0<=y<size and board[x][y]==board[i][j] :
                    count += 1
                    x += dx
                    y += dy
                    if count == numToWin :
                        return True
    return False
       
## AI using Minimax

def evaluate(board, turn):
    x, o = evaluate_for_x_o(board, turn)
    return x-o

def evaluate_for_x_o(board, turn):

    if isWin(XP):
        return float('inf'), 0 # vô cực - 0
    elif isWin(OP):
        return 0, float('inf') # 0 - vô cực
    elif is_board_full():
        return 0, 0

    eval_x = 0
    eval_o = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for d in directions:
        x, o = calc_eval_by_direction(board, turn, d)
        eval_x += x
        eval_o += o
    return eval_x, eval_o

def calc_eval_by_direction(board, turn, direction):

    explored = set() # tạo tập rỗng các ô đã đánh
    eval_x = 0
    eval_o = 0
    for row in range(size):
        for column in range(size):
            if ((row, column) in explored) or (board[row][column] == EMPTY):
                continue # xét luôn ô tiếp
            chain = find_chain(board, (row, column), direction)
            for pos in chain['chain']:
                explored.add(pos)
            if board[row][column] == XP:
                eval_x += calculation_chain(len(chain['before']), len(chain['chain']), len(chain['after']), turn==XP)
            else:
                eval_o += calculation_chain(len(chain['before']), len(chain['chain']), len(chain['after']), turn==OP)
    return eval_x, eval_o

def calculation_chain(before:int, chain:int, after:int, is_current_turn:bool)  ->int|float:
    if (before + chain + after) < numToWin:
        return 0

    # 1 left 1 win
    if chain == numToWin -1:
        if (before + chain) >= numToWin and (after+chain) >= numToWin:
            return 10**9 if is_current_turn else 10**8
        else:
            # Sửa điểm này cho HUMAN cao lên để AI ưu tiên chặn
            return 10**9 if is_current_turn else 10**5

    # 2 left to win
    elif chain == numToWin - 2:
        if (before + chain) >= numToWin and (after+chain) >= numToWin:
            return 10**7 if is_current_turn else 10**6
        else:
            return 10**4 if is_current_turn else 10**3

    # other
    if (before + chain) >= numToWin and (after + chain) >= numToWin:
        return 100*chain
    else:
        return 50 * chain

def find_chain(board, position:tuple[int, int], direction:tuple[int, int])  ->dict[str, list[tuple[int, int]]]:
    result =  {"before":[], "chain":[position], "after":[]}
    piece = board[position[0]][position[1]]

    d = direction
    d_ = (-d[0], -d[1])

    # di theo huong d
    end = position # diem ket thuc
    r, c = position
    r += d[0]
    c += d[1]
    while (0 <= r < size and 0 <= c < size) and board[r][c] == piece:
        result['chain'].append((r, c))
        end = (r, c)
        r += d[0]
        c += d[1]

    # di theo huong d_
    r, c = position
    start = position # diem bat dau
    r += d_[0]
    c += d_[1]
    while (0 <= r < size and 0 <= c < size) and board[r][c] == piece:
        result['chain'].append((r, c))
        start = (r, c)
        r += d_[0]
        c += d_[1]

    # before: di tu start , di theo d_
    r, c = start
    r += d_[0]
    c += d_[1]
    while (0 <= r < size and 0 <= c < size) and (board[r][c] == piece or board[r][c] == EMPTY):
        result['before'].append((r, c))
        r += d_[0]
        c += d_[1]
        if len(result['before']) == numToWin:
            break

    # after: di tu end, di theo d
    r, c = end
    r += d[0]
    c += d[1]
    while (0 <= r < size and 0 <= c < size) and (board[r][c] == piece or board[r][c] == EMPTY):
        result['after'].append((r, c))
        r += d[0]
        c += d[1]
        if len(result['after']) == numToWin:
            break

    return result


def find_valid_moves(board) -> list[tuple[int, int]]:
    '''empty_moves = set()
    for row in range(size):
        for col in range(size):
            if board[row][col] == EMPTY:
                empty_moves.add((row, col))
    if len(empty_moves) == size ** 2:
        return list(empty_moves)'''

    #all_moves = set() # toàn bộ ô trống
    in_range = set() # các ô trống trong phạm vi, không bị lặp
    radius = [_ for _ in range(-1, 1+1)]

    valid_moves = list()
    for coord in recent_move:
        row, col = coord
        for dr in radius:
            for dc in radius:
                p = (row + dr, col + dc)
                if (0 <= p[0] < size and 0 <= p[1] < size) \
                            and board[p[0]][p[1]] == EMPTY:
                    valid_moves.append(p)
                    in_range.add(p)
    for row in range(size):
        for col in range(size):
            if board[row][col] == EMPTY: # nếu ô trung tâm trống thì next
                #all_moves.add((row, col))
                continue
            # nếu ô trung tâm không trống thì xét trong phạm vi hình vuông 3x3
            for dr in radius:
                for dc in radius:
                    p = (row + dr, col + dc)
                    if (0 <= p[0] < size and 0 <= p[1] < size) \
                                and board[p[0]][p[1]] == EMPTY:
                        in_range.add(p)
    if not in_range:
        return [(size//2, size//2)]

    #out_range = all_moves - in_range # các ô trống còn lại
    valid_moves.extend(list(in_range))
    #moves_2 = random.sample(list(out_range), min(10, len(out_range)))
    return valid_moves #moves_1 + moves_2


def minimax(board, current_turn: str, depth_limit: int,
            alpha: int | float = float('-inf'),
            beta: int | float = float('inf'))  -> tuple[int | float, int]:
    
    global clickedSlot
    if depth_limit == 0 or isWin(AI) or isWin(HUMAN) or is_board_full():
        return evaluate(board, current_turn), depth_limit

    # x turn => find max eval
    if current_turn == XP:
        best_eval = float('-inf')
        best_depth = 0
        for move in find_valid_moves(board):
            board[move[0]][move[1]] = current_turn
            clickedSlot.append((move[0], move[1]))
            current_eval, current_depth = minimax(board, OP, depth_limit - 1, alpha, beta)
            board[move[0]][move[1]] = EMPTY
            clickedSlot.remove((move[0], move[1]))
            if (best_eval < current_eval) or (best_eval == current_eval and best_depth < current_depth):
                best_eval = current_eval
                best_depth = current_depth
            alpha = max(alpha, best_eval)

            if beta <= alpha:
                break
        return best_eval, best_depth

    # o turn =< find min eval
    else:
        best_eval = float('inf')
        best_depth = 0
        for move in find_valid_moves(board):
            board[move[0]][move[1]] = current_turn
            clickedSlot.append((move[0], move[1]))
            current_eval, current_depth = minimax(board, XP, depth_limit - 1, alpha, beta)
            board[move[0]][move[1]] = EMPTY
            clickedSlot.remove((move[0], move[1]))
            if (best_eval > current_eval) or (best_eval == current_eval and best_depth < current_depth):
                best_eval = current_eval
                best_depth = current_depth
            beta = min(beta, best_eval)

            if beta <= alpha:
                break
        return best_eval, best_depth


def decide_move(board, current_turn: str, depth)  -> tuple[int, int]:

    moves = find_valid_moves(board)
    #random.shuffle(moves)
    best_move = moves[0]
    best_eval = float('-inf') if current_turn == XP else float("inf")
    best_depth = 0
    opponent = OP if current_turn == XP else XP

    for move in moves:
        board[move[0]][move[1]] = current_turn
        clickedSlot.append((move[0], move[1]))
        current_eval, current_depth = minimax(board, opponent, depth - 1)
        clickedSlot.remove((move[0], move[1]))
        board[move[0]][move[1]] = EMPTY

        # x turn => find max eval
        if current_turn == XP:
            if (best_eval < current_eval) or (best_eval == current_eval and best_depth < current_depth):
                best_eval = current_eval
                best_depth = current_depth
                best_move = move
        # o turn => find min eval
        else:
            if (best_eval > current_eval) or (best_eval == current_eval and best_depth < current_depth):
                best_eval = current_eval
                best_depth = current_depth
                best_move = move
    return best_move

## AI using Greedy

def is_in(board, x, y):
    return 0 <= y < len(board) and 0 <= x < len(board)
    
def march(board,x,y,dx,dy,length):
    '''tìm vị trí xa nhất theo hướng dy,dx trong khoảng length'''
    yf = y + length*dy 
    xf = x + length*dx
    # chừng nào yf,xf không có trong board
    while not is_in(board,xf,yf):
        yf -= dy
        xf -= dx
    return xf,yf
    
def possible_moves(board):  
    '''trả về danh sách các ô có thể đánh trog ranh giới các ô đã đánh phạm vi 3 đơn vị'''
    #mảng taken lưu giá trị của người chơi và của máy trên bàn cờ -vtri đã click
    taken = [] # mảng các (i,j)
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
    # cord: lưu các vị trí không đi 
    cord = {} # dic chứa các (,):bool

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != EMPTY:
                taken.append((i,j))
    ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với nước đã có trên bàn cờ)'''
    for direction in directions:
        dx, dy = direction #
        for coord in taken: #xét các ô đã click
            x,y = coord # đã click
            for length in [1,2,3,4]:
                move = march(board,x,y,dx,dy,length) # ô xa nhất theo dy,dx cách 1 khoảg length
                if move not in taken and move not in cord:#nếu chưa click và chưa lưu 
                    cord[move]=False #false là chưa đi
    return cord


def sum_sumcol_values(sumcol):
    '''hợp nhất điểm của mỗi hướng, loại bỏ yếu tố hướng'''
    for key in sumcol: #duyệt mỗi loại điểm số
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values()) # casting bool->int
        else:
            sumcol[key] = sum(sumcol[key].values()) #tổg số lần đạt key theo mọi hướg sumcol[key][,]
            

def score_ready(scorecol): # scorecol là dic chứa các (,):[], scorecol==scores
    # Khởi tạo hệ thống điểm
    sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}} #dic con chứa các (,):int
    for key in scorecol: # e.g: (0,1)
        for score in scorecol[key]: # int, xét điểm các chuỗi 5 có trog hướng key
            if key in sumcol[score]: #(,) in {}, nếu đã lưu hướng này từ trc
                sumcol[score][key] += 1 # tăng số chuỗi có điểm là score 
            else:
                sumcol[score][key] = 1 # dic[5][(0,1)] : int, khởi tạo
    return sumcol


def score_of_list(lis,col):
    '''số quân col trog khối 5 ô, các quân ko cần lien tiep '''
    blank = lis.count(EMPTY)
    filled = lis.count(col)

    if blank + filled < 5: #nếu có chứa quân địch
        return -1
    elif blank == 5:
        return 0
    else:
        return filled

                
def row_to_list(board,x,y,dx,dy,xf,yf):
    '''
    trả về list của y,x từ yf,xf '''
    row = [] #list
    while y != yf + dy or x !=xf + dx:
        row.append(board[x][y])
        y += dy
        x += dx
    return row

def score_of_row(board,cordi,dx,dy,cordf,col):
    '''trả về một list với mỗi phần tử là điểm của 5 ô ltiep (tính bởi score_of_list) trong 9 ô
    '''
    colscores = []
    x,y = cordi
    xf,yf = cordf
    row = row_to_list(board,x,y,dx,dy,xf,yf)
    for start in range(len(row)-4):# 0->len(row)-5
        score = score_of_list(row[start:start+5],col)
        colscores.append(score)
    return colscores
     
     
def score_of_col_one(board,col,x,y):
    '''trả lại điểm số của color tại y,x theo 4 hướng,
    key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ'''
    scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}

    scores[(0,1)].extend(score_of_row(board,march(board,x,y,0,-1,4), 0, 1,march(board,x,y,0,1,4), col)) #nối thêm mảg 1 chiều vào mảg 1 chiều

    scores[(1,0)].extend(score_of_row(board,march(board,x,y,-1,0,4), 1, 0,march(board,x,y,1,0,4), col))

    scores[(1,1)].extend(score_of_row(board,march(board,x,y,-1,-1,4), 1, 1,march(board,x,y,1,1,4), col))

    scores[(-1,1)].extend(score_of_row(board,march(board,x,y,-1,1,4), 1,-1,march(board,x,y,1,-1,4), col))
    return score_ready(scores) #return sumcol
    
    
def TF34score(score3,score4):
    '''
    trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp) --hướg t1 có chuỗi 4 hướg t2 có ít nhất 2 chuỗi 3 thì true
    '''
    for key4 in score4: #mỗi hướng
        if score4[key4] >=1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >=2:
                        return True
    return False
     
     
def winning_situation(sumcol):
    '''trả lại tình huống chắc chắn sẽ chiến thắng, sumcol dạng như:
    {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}  # theo hướng (0,1) có 4 chuỗi độ dài 1
    1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
    -1 là rơi vào trạng thái tồi, cần phòng thủ
    '''#sumcol là dic có các value là dic
    if 1 in sumcol[5].values(): #nếu có hướng có 1 chuỗi độ dài 5
        return 5
    elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2): #nếu có 2 hướng có chuỗi 4 hoặc 1 hướng mà 2 chuỗi
        return 4
    elif TF34score(sumcol[3],sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(),reverse = True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2: #nếu chuỗi 3 có >=2 hướg và 2 hướg nhiều chuỗi 3 nhất có >=2 chuỗi
            return 3
    return 0  

        
def stupid_score(board,col,anticol,x,y):
    ''' điểm của trạng thái bàn cờ khi đánh vào ô x,y '''
    global colors
    M = 1000 #magic number: 1000, 4, 8, 16
    res,adv, dis = 0, 0, 0

    #tấn công
    board[x][y]=col # giả sử nếu mình đánh
    #draw_stone(x,y,colors[col])
    sumcol = score_of_col_one(board,col,x,y) # key là số điểm, value là (key là hướg, value là số lần)  
    a = winning_situation(sumcol)
    adv += a * M #ưu tiên hơn
    sum_sumcol_values(sumcol) #hợp nhất sumcol
    #{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
    adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]

    #phòng thủ
    board[x][y]=anticol #nếu mình đánh (chặn) vào ô địch dễ thắg
    sumanticol = score_of_col_one(board,anticol,x,y)  
    d = winning_situation(sumanticol)
    dis += d * (M-100) #ưu tiên tấn côg
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

    res = adv + dis #địch càg dễ thắg mà mk chặn thì điểm of nc đi này càg cao
    board[x][y]=EMPTY #reset
    return res    

def find_best_move():
    global board
    moves = possible_moves(board)
    best_score = -float('inf')
    best_move = (-1, -1)
    #for i in range(size):
        #for j in range(size):
    for move in moves:
        i,j = move
        '''
        if board[i][j] == EMPTY:
            board[i][j] = AI
            clickedSlot.append((i,j))
            score = minimax(i,j,1, False, -float('inf'), float('inf')) #depth=1
            board[i][j] = EMPTY
            clickedSlot.remove((i,j)) #trả về trạng thái ban đầu
            if score > best_score:
                best_score = score #update best_score
                best_move = (i, j)
        '''
        
        score = stupid_score(board, AI, HUMAN, i, j)
        if score>best_score:
            best_score = score
            best_move = (i,j)
        
    return best_move


## click event handler
def click(y,x):
    global board, winner
    if x>=0 and y>=0 :
        intx,inty = int(x),int(y)
        if 0<=intx<=size-1 and 0<=inty<=size-1 and (intx, inty) not in clickedSlot:
            clickedSlot.append((intx,inty))
            recent_move[1] = (intx, inty)
            board[intx][inty] = HUMAN
            drawX(intx,inty)
            turtle.update()
            print(f"Human: {(intx, inty)}")
            if isWin(HUMAN):
                winner = HUMAN
                print("winner is ", winner)
                winWindow()
                return
            if level == 1:
                AI_move = decide_move(board, AI, MAX_DEPTH)
            else:
                AI_move = find_best_move()
            AI_x = AI_move[0]
            AI_y = AI_move[1]
            if AI_x >=0 and AI_y >= 0 and (AI_x, AI_y) not in clickedSlot:
                drawO(AI_x, AI_y)
                turtle.update()
                recent_move[0] = (AI_x, AI_y)
                board[AI_x][AI_y] = AI
                clickedSlot.append((AI_x,AI_y))
                print(f"AI: {(AI_x,AI_y)}")
                if isWin(AI):
                    winner = AI
                    print("winner is ", winner)
                    winWindow()
                    return
    if is_board_full() :
        print("DRAW")
        drawWnd();
   

def drawX(y,x):
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

def drawO(y,x):
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
    root.title("Who wins?")
    tk.Label(root, text=f"{winner} wins").pack()
    root.mainloop()

def drawWnd():
    root = tk.Tk()
    root.geometry("250x40+550+350") # widthxheight+x+y
    root.title("Who wins?")
    tk.Label(root, text="Draw").pack()
    root.mainloop()

def init(size):
    global clickedSlot
    clickedSlot = []
    global board
    board = [['_']*size for _ in range(size)]
    screen = turtle.Screen()
    screen.setup(800, 640) # 400, 320)
    screen.bgcolor("light blue")
    screen.title("CARO")
    screen.tracer(0)
    screen.update()
    turtle.update()
    screen.setworldcoordinates(-1,size+1,size+1,-1)
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
    global size, numToWin, level
    size = int(size_entry.get())
    numToWin = 5
    level = int(level_entry.get())
    root.destroy()


if __name__ == "__main__" :
    root = tk.Tk()
    root.geometry("250x110+550+350")
    root.title("Input")
    tk.Label(root, text="Size of board:").pack()
    size_entry = tk.Entry(root)
    size_entry.pack()
    tk.Label(root, text="Level (1 or 2):").pack()
    level_entry = tk.Entry(root)
    level_entry.pack()
    tk.Button(root, text="OK", command=closeInputWindow).pack()
    root.mainloop()
    
    if numToWin > size :
        print("Error")
    else:
        init(size)