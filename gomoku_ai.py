def is_bounded(board, y_end, x_end, length, d_y, d_x):
    sides_blocked = 0
    
    if board[y_end][x_end] == "b":
        for i in range(length):
            if board[y_end - i*d_y][x_end - i*d_x] != "b":
                return "Not a continuous sequence of the same colour" 

        if ((y_end - d_y * (length-1) in (0, len(board) - 1)) and d_y != 0) or \
        ((x_end - d_x * (length-1) in (0, len(board) - 1)) and d_x != 0):
            sides_blocked += 1
        elif board[y_end - d_y * length][x_end - d_x * length] == "w":
            sides_blocked += 1
        elif board[y_end - d_y * length][x_end - d_x * length] == "b":
            return "Sequence not of correct length"
            
        if ((y_end in (0, len(board) - 1)) and d_y != 0) or ((x_end in (0, len(board) - 1)) and d_x != 0):
            sides_blocked += 1
        elif board[y_end + d_y][x_end + d_x] == "w":
            sides_blocked += 1
        elif board[y_end + d_y][x_end + d_x] == "b":
            return "Sequence not of correct length"
            
    if board[y_end][x_end] == "w":
        for i in range(length):
            if board[y_end - i*d_y][x_end - i*d_x] != "w":
                return "Not a continuous sequence of the same colour" 

        if ((y_end - d_y * (length-1) in (0, len(board) - 1)) and d_y != 0) or \
        ((x_end - d_x * (length-1) in (0, len(board) - 1)) and d_x != 0):
            sides_blocked += 1
        elif board[y_end - d_y * length][x_end - d_x * length] == "b":
            sides_blocked += 1
        elif board[y_end - d_y * length][x_end - d_x * length] == "w":
            return "Sequence not of correct length"
            
        if ((y_end in (0, len(board) - 1)) and d_y != 0) or ((x_end in (0, len(board) - 1)) and d_x != 0):
            sides_blocked += 1
        elif board[y_end + d_y][x_end + d_x] == "b":
            sides_blocked += 1
        elif board[y_end + d_y][x_end + d_x] == "w":
            return "Sequence not of correct length"


    if sides_blocked == 0:
        return "OPEN"
    if sides_blocked == 1:
        return "SEMIOPEN"
    if sides_blocked == 2:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    y = y_start + d_y * (length-1)
    x = x_start + d_x * (length-1)
    if y > len(board) - 1 or x > len(board) - 1:
        return 0, 0
        
    open_seq_count, semi_open_seq_count = 0, 0
    while y <= len(board) - 1 and x <= len(board) - 1 and x >= 0:
        if board[y][x] == col:
            if ((y == len(board) - 1) and (d_y == 1)) or ((x == len(board) - 1) and (d_x == 1)) or \
            ((x == 0) and (d_x == -1)) :
                if is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1

            elif board[y + d_y][x + d_x] != col:
                if is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
        y += d_y
        x += d_x
    
        
    return open_seq_count, semi_open_seq_count
        
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]
    for j in range(len(board)):
        open_seq_count += detect_row(board, col, j, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, j, 0, length, 1, 1)[1]
    for k in range(len(board)):
        open_seq_count += detect_row(board, col, 0, k, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, k, length, 1, 0)[1]
    for l in range(1, len(board)):
        open_seq_count += detect_row(board, col, 0, l, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, 0, l, length, 1, 1)[1]
    for m in range(len(board)):
        open_seq_count += detect_row(board, col, 0, m, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, m, length, 1, -1)[1]
    for n in range(1, len(board)):
        open_seq_count += detect_row(board, col, n, len(board) - 1, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, n, len(board) - 1, length, 1, -1)[1]


    return open_seq_count, semi_open_seq_count

def board_count(board):
    b_count = 0
    w_count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "b":
                b_count += 1
            if board[i][j] == "w":
                w_count += 1
    return b_count, w_count
    
def get_move(board, col):
    board_height = len(board)
    board_width = len(board[0])
    b_count, w_count = board_count(board)
    if col == "b":
        best_score = -1000000000
        if is_empty(board) or (w_count == 1 and b_count == 0):
            if board[board_height // 2][board_width // 2] == " ":
                return board_height // 2, board_width // 2
            else:
                return board_height // 2 - 1, board_width // 2 - 1
                
        
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "b"
                    if is_win(board) == "Black won":
                        return y, x
                    board[y][x] = " "

        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "w"                
                    if is_win(board) == "White won":
                        board[y][x] = " "
                        return y, x 
                    board[y][x] = " "
                    
        if detect_rows(board, "b", 4)[0] == 0:
            for y in range(len(board)):
                for x in range(len(board)):
                    if board[y][x] == " ":
                        board[y][x] = "b"
                        if detect_rows(board, "b", 4)[0] > 0:
                            board[y][x] = " "
                            return y, x 
                        board[y][x] = " "
                        
        if detect_rows(board, "w", 4)[0] == 0:
            for y in range(len(board)):
                for x in range(len(board)):
                    if board[y][x] == " ":
                        board[y][x] = "w"
                        if detect_rows(board, "w", 4)[0] > 0:
                            board[y][x] = " "
                            return y, x 
                        board[y][x] = " "
    
                        
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "b"
                    if score_black(board) > best_score:
                        best_score = score_black(board)
                        move_y, move_x = y, x
                    board[y][x] = " "
        return move_y, move_x
        
    if col == "w":
        best_score = -1000000000
        
        if is_empty(board) or (w_count == 0 and b_count == 1):
            if board[board_height // 2][board_width // 2] == " ":
                return board_height // 2, board_width // 2
                
            else:
                return board_height // 2 - 1, board_width // 2 - 1
        
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "w"
                    if is_win(board) == "White won":
                        return y, x
                    board[y][x] = " "
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "b"                
                    if is_win(board) == "Black won":
                        board[y][x] = " "
                        return y, x 
                    board[y][x] = " "
                    
        if detect_rows(board, "w", 4)[0] == 0:
            for y in range(len(board)):
                for x in range(len(board)):
                    if board[y][x] == " ":
                        board[y][x] = "w"
                        if detect_rows(board, "w", 4)[0] > 0:
                            board[y][x] = " "
                            return y, x 
                        board[y][x] = " "
                        
        if detect_rows(board, "b", 4)[0] == 0:
            for y in range(len(board)):
                for x in range(len(board)):
                    if board[y][x] == " ":
                        board[y][x] = "b"
                        if detect_rows(board, "b", 4)[0] > 0:
                            board[y][x] = " "
                            return y, x 
                        board[y][x] = " " 
    
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x] == " ":
                    board[y][x] = "w"
                    if score_white(board) > best_score:
                        best_score = score_white(board)
                        move_y, move_x = y, x
                    board[y][x] = " "
        return move_y, move_x
        

def score_white(board):
    MAX_SCORE = 1000000
    
    open_w = {}
    semi_open_w = {}
    open_b = {}
    semi_open_b = {}
    
    for i in range(2, 6):
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        
    
    if open_w[5] >= 1 or semi_open_w[5] >= 1:
        return MAX_SCORE
    
    elif open_b[5] >= 1 or semi_open_b[5] >= 1:
        return -MAX_SCORE
        
    score = (-50000 * (open_b[4] + semi_open_b[4])+ 
            6000  * open_w[4]                     + 
            50   * semi_open_w[4]                + 
            -1000  * open_b[3]                    + 
            -30   * semi_open_b[3]               + 
            50   * open_w[3]                     + 
            9   * semi_open_w[3]                +  
            10 * open_w[2] + semi_open_w[2] - 10 * open_b[2] - semi_open_b[2])
    if semi_open_w[4] > 1:
        score += 4000
    if open_w[3] > 1:
        score += 300
    return score
   
def score_black(board):
    MAX_SCORE = 1000000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    score = (-50000 * (open_w[4] + semi_open_w[4])+ 
            6000  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -1000  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            9   * semi_open_b[3]                +  
            10 * open_b[2] + semi_open_b[2] - 10 * open_w[2] - semi_open_w[2])
            
    if semi_open_b[4] > 1:
        score += 4000
    if open_b[3] > 1:
        score += 300
    return score
        

def win_check_line(board, y_start, x_start, d_y, d_x):
    i = 0
    black_count, white_count = 0, 0
    while (y_start + i*d_y) <= len(board) - 1 and (x_start + i*d_x) <= len(board) - 1 and \
    (x_start + i*d_x) >= 0:
        if board[y_start + i*d_y][x_start + i*d_x] == "b":
            if white_count == 5:
                return "White won"
            white_count = 0
            black_count += 1
        if board[y_start + i*d_y][x_start + i*d_x] == "w":
            if black_count == 5:
                return "Black won"
            black_count = 0
            white_count += 1
        if board[y_start + i*d_y][x_start + i*d_x] == " ":
            if black_count == 5:
                return "Black won"
            if white_count == 5:
                return "White won"
            black_count, white_count = 0, 0
        
        if ((y_start + i*d_y == len(board) - 1) and (d_y == 1)) or ((x_start + i*d_x == len(board) - 1) and (d_x == 1)) or \
        ((x_start + i*d_x == 0) and (d_x == -1)) :
            if black_count == 5:
                return "Black won"
            if white_count == 5:
                return "White won"
        i += 1
    return "No win here"
  
  
def is_win(board):
    for i in range(len(board)):
        if win_check_line(board, i, 0, 0, 1) != "No win here":
            return win_check_line(board, i, 0, 0, 1)
    for j in range(len(board)):
        if win_check_line(board, j, 0, 1, 1) != "No win here":
            return win_check_line(board, j, 0, 1, 1)
    for k in range(len(board)):
        if win_check_line(board, 0, k, 1, 0) != "No win here":
            return win_check_line(board, 0, k, 1, 0)
    for l in range(1, len(board)):
        if win_check_line(board, 0, l, 1, 1) != "No win here":
            return win_check_line(board, 0, l, 1, 1)
    for m in range(len(board)):
        if win_check_line(board, 0, m, 1, -1) != "No win here":
            return win_check_line(board, 0, m, 1, -1)
    for n in range(1, len(board)):
        if win_check_line(board, n, len(board) - 1, 1, -1) != "No win here":
            return win_check_line(board, n, len(board) - 1, 1, -1)
      
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                return "Continue playing" 
    return "Draw"

