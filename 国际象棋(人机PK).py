import tkinter as tk
from tkinter import simpledialog
import random
import math

class ChessGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("国际象棋AI(游戏制作：白杨博贤)")
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.pack()
        
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        self.has_moved = set()
        self.selected_piece = None
        self.current_player = 'white'
        self.game_over = False
        self.ai_thinking = False
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_handler)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#F0D9B5", "#B58863"]
        
        king_pos = self.find_king(self.current_player)
        in_check = False
        if king_pos and self.is_square_attacked(king_pos, 'black' if self.current_player == 'white' else 'white'):
            in_check = True

        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                if in_check and (row, col) == king_pos:
                    color = "#FF6B6B"
                
                self.canvas.create_rectangle(
                    col * 60, row * 60, (col + 1) * 60, (row + 1) * 60,
                    fill=color, outline=""
                )
                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text(
                        col * 60 + 30, row * 60 + 30,
                        text=self.get_unicode(piece),
                        font=("Arial", 30)
                    )
        
        if self.selected_piece:
            row, col = self.selected_piece
            self.canvas.create_rectangle(
                col * 60, row * 60, (col + 1) * 60, (row + 1) * 60,
                outline="blue", width=3
            )
        
        if self.game_over:
            self.canvas.create_text(240, 240, text="游戏结束", font=("Arial", 40), fill="red")

    def get_unicode(self, piece):
        pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        return pieces.get(piece, '')

    def click_handler(self, event):
        if self.game_over or self.current_player == 'black' or self.ai_thinking:
            return
            
        col = event.x // 60
        row = event.y // 60
        if not (0 <= row < 8 and 0 <= col < 8): return

        piece = self.board[row][col]
        if piece and piece.isupper(): 
            self.selected_piece = (row, col)
            self.draw_board()
            return

        if self.selected_piece:
            if self.is_valid_move(self.selected_piece, (row, col), strict_check=True):
                self.make_move(self.selected_piece, (row, col), is_real_move=True)
                self.current_player = 'black'
                self.selected_piece = None
                self.draw_board()
                
                status = self.get_game_status('black')
                if status == 'checkmate':
                    self.game_over = True
                    self.canvas.create_text(240, 240, text="你赢了!", font=("Arial", 40), fill="green")
                elif status == 'stalemate':
                    self.game_over = True
                    self.canvas.create_text(240, 240, text="逼和", font=("Arial", 40), fill="blue")
                else:
                    self.root.after(100, self.ai_move)
            else:
                self.selected_piece = None
                self.draw_board()

    def find_king(self, player_color):
        target = 'K' if player_color == 'white' else 'k'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)
        return None

    def is_square_attacked(self, pos, attacker_color):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if not piece: continue
                
                is_white = piece.isupper()
                p_color = 'white' if is_white else 'black'
                
                if p_color == attacker_color:
                    if self.is_valid_move((r, c), pos, strict_check=False, check_attack_only=True):
                        return True
        return False

    def is_valid_move(self, start, end, strict_check=True, check_attack_only=False):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        target = self.board[r2][c2]

        if not piece: return False
        if r1 == r2 and c1 == c2: return False

        if target:
            if piece.isupper() == target.isupper():
                return False

        ptype = piece.lower()
        valid_geometry = False
        if ptype == 'p': valid_geometry = self.valid_pawn(start, end, piece, target, check_attack_only)
        elif ptype == 'r': valid_geometry = self.valid_rook(start, end)
        elif ptype == 'n': valid_geometry = self.valid_knight(start, end)
        elif ptype == 'b': valid_geometry = self.valid_bishop(start, end)
        elif ptype == 'q': valid_geometry = self.valid_queen(start, end)
        elif ptype == 'k': valid_geometry = self.valid_king(start, end, strict_check)
        
        if not valid_geometry:
            return False

        if not strict_check:
            return True

        my_color = 'white' if piece.isupper() else 'black'
        opponent = 'black' if my_color == 'white' else 'white'
        
        saved_board = [row[:] for row in self.board]
        
        self.board[r2][c2] = piece
        self.board[r1][c1] = ''
        if ptype == 'k' and abs(c1 - c2) == 2:
            if c2 > c1:
                self.board[r1][5], self.board[r1][7] = self.board[r1][7], ''
            else:
                self.board[r1][3], self.board[r1][0] = self.board[r1][0], ''

        king_pos = self.find_king(my_color)
        if not king_pos: 
            is_suicide = True
        else:
            is_suicide = self.is_square_attacked(king_pos, opponent)
        
        self.board = saved_board
        
        return not is_suicide

    def valid_pawn(self, start, end, piece, target, check_attack_only):
        r1, c1 = start
        r2, c2 = end
        direction = -1 if piece.isupper() else 1
        
        if check_attack_only:
            if r2 == r1 + direction and abs(c2 - c1) == 1:
                return True
            return False

        if c1 == c2:
            if target: return False
            if r2 == r1 + direction: return True
            if ((r1 == 6 and piece.isupper()) or (r1 == 1 and piece.islower())):
                if r2 == r1 + 2 * direction and not self.board[r1+direction][c1]:
                    return True
        elif abs(c1 - c2) == 1 and r2 == r1 + direction:
            if target: return True
        return False

    def valid_rook(self, start, end):
        if start[0] != end[0] and start[1] != end[1]: return False
        return self.is_path_clear(start, end)

    def valid_knight(self, start, end):
        return (abs(start[0]-end[0]), abs(start[1]-end[1])) in [(1,2), (2,1)]

    def valid_bishop(self, start, end):
        if abs(start[0]-end[0]) != abs(start[1]-end[1]): return False
        return self.is_path_clear(start, end)

    def valid_queen(self, start, end):
        return self.valid_rook(start, end) or self.valid_bishop(start, end)

    def valid_king(self, start, end, strict_check):
        r1, c1 = start
        r2, c2 = end
        dr, dc = abs(r1-r2), abs(c1-c2)
        
        if dr <= 1 and dc <= 1: return True
        
        if strict_check and dr == 0 and dc == 2:
            if (r1, c1) in self.has_moved: return False
            my_color = 'white' if self.board[r1][c1].isupper() else 'black'
            opponent = 'black' if my_color == 'white' else 'white'
            if self.is_square_attacked((r1, c1), opponent): return False

            if c2 > c1:
                if (r1, 7) in self.has_moved or self.board[r1][7].lower() != 'r': return False
                if self.board[r1][5] or self.board[r1][6]: return False
                if self.is_square_attacked((r1, 5), opponent): return False
                return True
            else:
                if (r1, 0) in self.has_moved or self.board[r1][0].lower() != 'r': return False
                if self.board[r1][1] or self.board[r1][2] or self.board[r1][3]: return False
                if self.is_square_attacked((r1, 3), opponent): return False
                return True
        return False

    def is_path_clear(self, start, end):
        r1, c1 = start
        r2, c2 = end
        r_step = 0 if r1 == r2 else (1 if r2 > r1 else -1)
        c_step = 0 if c1 == c2 else (1 if c2 > c1 else -1)
        curr_r, curr_c = r1 + r_step, c1 + c_step
        while (curr_r, curr_c) != (r2, c2):
            if self.board[curr_r][curr_c]: return False
            curr_r += r_step
            curr_c += c_step
        return True

    def make_move(self, start, end, is_real_move=False):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        
        if piece.lower() == 'k' and abs(c1 - c2) == 2:
            if c2 > c1:
                self.board[r1][5] = self.board[r1][7]
                self.board[r1][7] = ''
                if is_real_move: self.has_moved.add((r1, 7))
            else:
                self.board[r1][3] = self.board[r1][0]
                self.board[r1][0] = ''
                if is_real_move: self.has_moved.add((r1, 0))

        self.board[r2][c2] = piece
        self.board[r1][c1] = ''
        
        if is_real_move:
            self.has_moved.add((r1, c1))
            if piece == 'P' and r2 == 0:
                choice = simpledialog.askstring("升变", "Q, R, N, B?")
                self.board[r2][c2] = choice.upper() if choice and choice.upper() in 'RNB' else 'Q'
            elif piece == 'p' and r2 == 7:
                self.board[r2][c2] = 'q'

    def get_game_status(self, player_color):
        valid_moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p: continue
                if (player_color == 'white' and p.isupper()) or (player_color == 'black' and p.islower()):
                    for tr in range(8):
                        for tc in range(8):
                            if self.is_valid_move((r, c), (tr, tc), strict_check=True):
                                valid_moves.append(((r,c), (tr,tc)))
        
        if not valid_moves:
            king_pos = self.find_king(player_color)
            opponent = 'black' if player_color == 'white' else 'white'
            if self.is_square_attacked(king_pos, opponent):
                return 'checkmate'
            else:
                return 'stalemate'
        return 'playing'

    def run(self):
        self.root.mainloop()

PIECE_VALUES = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000}
pst_generic = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

def evaluate_board(game):
    score = 0
    for r in range(8):
        for c in range(8):
            piece = game.board[r][c]
            if not piece: continue
            val = PIECE_VALUES.get(piece.lower(), 0)
            pos_val = pst_generic[r][c] if piece.islower() else pst_generic[7-r][c]
            if piece.islower(): score += (val + pos_val)
            else: score -= (val + pos_val)
    return score

def get_ai_moves(game):
    moves = []
    for r in range(8):
        for c in range(8):
            p = game.board[r][c]
            if p and p.islower():
                for tr in range(8):
                    for tc in range(8):
                        if game.is_valid_move((r, c), (tr, tc), strict_check=True):
                            priority = 0
                            target = game.board[tr][tc]
                            if target: priority = PIECE_VALUES.get(target.lower(), 0)
                            moves.append((priority, (r, c), (tr, tc)))
    moves.sort(key=lambda x: x[0], reverse=True)
    return [ (m[1], m[2]) for m in moves ]

def minimax(game, depth, alpha, beta, is_maximizing):
    current_turn = 'black' if is_maximizing else 'white'
    status = game.get_game_status(current_turn)
    
    if status == 'checkmate':
        return -99999 if is_maximizing else 99999
    if status == 'stalemate':
        return 0
    if depth == 0:
        return evaluate_board(game)

    if is_maximizing:
        max_eval = -math.inf
        moves = get_ai_moves(game)
        for start, end in moves:
            saved_board = [row[:] for row in game.board]
            game.make_move(start, end, is_real_move=False)
            
            eval = minimax(game, depth - 1, alpha, beta, False)
            
            game.board = saved_board
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = math.inf
        moves = []
        for r in range(8):
            for c in range(8):
                p = game.board[r][c]
                if p and p.isupper():
                    for tr in range(8):
                        for tc in range(8):
                            if game.is_valid_move((r,c), (tr,tc), strict_check=True):
                                moves.append(((r,c), (tr,tc)))
        
        moves.sort(key=lambda m: PIECE_VALUES.get(game.board[m[1][0]][m[1][1]].lower(), 0) if game.board[m[1][0]][m[1][1]] else 0, reverse=True)

        for start, end in moves:
            saved_board = [row[:] for row in game.board]
            game.make_move(start, end, is_real_move=False)
            eval = minimax(game, depth - 1, alpha, beta, True)
            game.board = saved_board
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break
        return min_eval

def ai_entry(self):
    self.ai_thinking = True
    self.root.update()
    
    depth = 2
    
    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf
    
    moves = get_ai_moves(self)
    
    for start, end in moves:
        saved_board = [row[:] for row in self.board]
        self.make_move(start, end, is_real_move=False)
        
        val = minimax(self, depth - 1, alpha, beta, False)
        
        self.board = saved_board
        
        print(f"Move {start}->{end}: {val}")
        
        if val > best_value:
            best_value = val
            best_move = (start, end)
            alpha = max(alpha, val)
            
    if best_move:
        self.make_move(best_move[0], best_move[1], is_real_move=True)
        self.current_player = 'white'
        
        status = self.get_game_status('white')
        if status == 'checkmate':
            self.game_over = True
            self.draw_board()
            self.canvas.create_text(240, 240, text="你输了!", font=("Arial", 40), fill="red")
        elif status == 'stalemate':
            self.game_over = True
            self.canvas.create_text(240, 240, text="逼和", font=("Arial", 40), fill="blue")
    
    self.ai_thinking = False
    if not self.game_over:
        self.draw_board()

ChessGame.ai_move = ai_entry

if __name__ == "__main__":
    game = ChessGame()
    game.run()
