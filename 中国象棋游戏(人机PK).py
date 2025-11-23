import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import math
import time

class ChineseChess:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("中国象棋(游戏制作:白杨博贤)")
        
        self.cell_size = 60
        self.r_size = 26
        self.margin = 60
        
        self.board_width = 8 * self.cell_size
        self.board_height = 9 * self.cell_size
        
        canvas_w = self.board_width + 2 * self.margin
        canvas_h = self.board_height + 2 * self.margin
        
        self.canvas = tk.Canvas(self.root, width=canvas_w, height=canvas_h, bg="#DEB887")
        self.canvas.pack()

        self.status_label = tk.Label(self.root, text="准备就绪", font=("Arial", 12), bg="#f0f0f0", width=60)
        self.status_label.pack(pady=5)

        menubar = tk.Menu(self.root)
        
        gamemenu = tk.Menu(menubar, tearoff=0)
        gamemenu.add_command(label="人机对战 (你执红)", command=lambda: self.reset_game("HvA"))
        gamemenu.add_command(label="AI 互殴 (观战)", command=lambda: self.reset_game("AvA"))
        menubar.add_cascade(label="游戏模式", menu=gamemenu)
        
        diffmenu = tk.Menu(menubar, tearoff=0)
        diffmenu.add_radiobutton(label="入门 (深度2)", command=lambda: self.set_difficulty(2))
        diffmenu.add_radiobutton(label="业余 (深度3)", command=lambda: self.set_difficulty(3))
        diffmenu.add_radiobutton(label="大师 (深度4)", command=lambda: self.set_difficulty(4))
        menubar.add_cascade(label="难度设置", menu=diffmenu)
        
        self.root.config(menu=menubar)
        
        self.board = []
        self.current_player = 'red'
        self.game_over = False
        self.ai_thinking = False
        self.mode = "HvA"
        self.selected_pos = None
        self.search_depth = 2
        self.history = []

        self.init_board_data()
        self.draw_board_grid()
        self.draw_pieces()
        
        self.canvas.bind("<Button-1>", self.click_handler)

    def set_difficulty(self, d):
        self.search_depth = d
        names = {2:"入门", 3:"业余", 4:"大师"}
        self.status_label.config(text=f"难度已切换为: {names[d]}")

    def init_board_data(self):
        self.board = [
            ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
            ['',  '',  '',  '',  '',  '',  '',  '',  ''],
            ['',  'c', '',  '',  '',  '',  '',  'c', ''],
            ['p', '',  'p', '',  'p', '',  'p', '',  'p'],
            ['',  '',  '',  '',  '',  '',  '',  '',  ''],
            ['',  '',  '',  '',  '',  '',  '',  '',  ''],
            ['P', '',  'P', '',  'P', '',  'P', '',  'P'],
            ['',  'C', '',  '',  '',  '',  '',  'C', ''],
            ['',  '',  '',  '',  '',  '',  '',  '',  ''],
            ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
        ]
        self.history = []

    def reset_game(self, mode):
        self.init_board_data()
        self.current_player = 'red'
        self.game_over = False
        self.selected_pos = None
        self.mode = mode
        self.draw_pieces()
        self.status_label.config(text=f"模式: {'人机' if mode=='HvA' else 'AI互殴'} - 红方回合")
        
        if self.mode == "AvA":
            self.root.after(500, self.run_ai)

    def get_canvas_xy(self, row, col):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        return x, y

    def get_grid_rc(self, x, y):
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)
        if 0 <= col <= 8 and 0 <= row <= 9:
            return row, col
        return None, None

    def draw_board_grid(self):
        self.canvas.delete("grid")
        for r in range(10):
            y = self.margin + r * self.cell_size
            self.canvas.create_line(self.margin, y, self.margin + 8 * self.cell_size, y, width=2, tags="grid")
        for c in range(9):
            x = self.margin + c * self.cell_size
            self.canvas.create_line(x, self.margin, x, self.margin + 4 * self.cell_size, width=2, tags="grid")
            self.canvas.create_line(x, self.margin + 5 * self.cell_size, x, self.margin + 9 * self.cell_size, width=2, tags="grid")
        
        lx, rx = self.margin, self.margin + 8 * self.cell_size
        ty, by = self.margin + 4 * self.cell_size, self.margin + 5 * self.cell_size
        self.canvas.create_line(lx, ty, lx, by, width=2, tags="grid")
        self.canvas.create_line(rx, ty, rx, by, width=2, tags="grid")
        
        bx1, by1 = self.get_canvas_xy(0, 3)
        bx2, by2 = self.get_canvas_xy(2, 5)
        self.canvas.create_line(bx1, by1, bx2, by2, width=2, tags="grid")
        bx3, by3 = self.get_canvas_xy(0, 5)
        bx4, by4 = self.get_canvas_xy(2, 3)
        self.canvas.create_line(bx3, by3, bx4, by4, width=2, tags="grid")
        
        rx1, ry1 = self.get_canvas_xy(9, 3)
        rx2, ry2 = self.get_canvas_xy(7, 5)
        self.canvas.create_line(rx1, ry1, rx2, ry2, width=2, tags="grid")
        rx3, ry3 = self.get_canvas_xy(9, 5)
        rx4, ry4 = self.get_canvas_xy(7, 3)
        self.canvas.create_line(rx3, ry3, rx4, ry4, width=2, tags="grid")
        
        cx, cy = self.margin + 4 * self.cell_size, self.margin + 4.5 * self.cell_size
        self.canvas.create_text(cx - 100, cy, text="楚  河", font=("Kaiti", 32), fill="#5C4033", tags="grid")
        self.canvas.create_text(cx + 100, cy, text="汉  界", font=("Kaiti", 32), fill="#5C4033", tags="grid")

    def draw_pieces(self):
        self.canvas.delete("piece")
        name_map = {
            'R': '车', 'N': '马', 'B': '相', 'A': '仕', 'K': '帅', 'C': '炮', 'P': '兵',
            'r': '车', 'n': '马', 'b': '象', 'a': '士', 'k': '将', 'c': '炮', 'p': '卒'
        }
        
        for r in range(10):
            for c in range(9):
                p = self.board[r][c]
                if p:
                    x, y = self.get_canvas_xy(r, c)
                    is_red = p.isupper()
                    outer_color = "#5C3317" if not is_red else "#8B0000"
                    text_color = "red" if is_red else "black"
                    
                    self.canvas.create_oval(x - 28, y - 28, x + 28, y + 28, fill="#888888", outline="", tags="piece")
                    self.canvas.create_oval(x - 26, y - 26, x + 26, y + 26, fill="#FDF5E6", outline=outer_color, width=3, tags="piece")
                    self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22, outline=outer_color, width=1, tags="piece")
                    self.canvas.create_text(x, y - 2, text=name_map[p], font=("LiSu", 24, "bold"), fill=text_color, tags="piece")
                    
                    if self.selected_pos == (r, c):
                        self.canvas.create_rectangle(x - 30, y - 30, x + 30, y + 30, outline="#00FF00", width=3, tags="piece")

    def click_handler(self, event):
        if self.mode == "AvA": return
        if self.game_over or self.ai_thinking: return
        
        row, col = self.get_grid_rc(event.x, event.y)
        if row is None: return
        
        clicked_p = self.board[row][col]
        
        if self.selected_pos:
            if (row, col) == self.selected_pos:
                self.selected_pos = None
                self.draw_pieces()
                return
            
            if self.is_valid_move(self.selected_pos, (row, col)):
                self.make_move(self.selected_pos, (row, col))
                self.post_move_action()
            else:
                if clicked_p and clicked_p.isupper():
                    self.selected_pos = (row, col)
                    self.draw_pieces()
        else:
            if clicked_p and clicked_p.isupper():
                self.selected_pos = (row, col)
                self.draw_pieces()

    def post_move_action(self):
        self.draw_pieces()
        if self.check_win(): return
        
        self.current_player = 'black' if self.current_player == 'red' else 'red'
        
        p_name = "你" if (self.mode=="HvA" and self.current_player=='red') else "AI"
        c_name = "红方" if self.current_player=='red' else "黑方"
        self.status_label.config(text=f"{c_name} ({p_name}) 思考中...")
        
        if self.mode == "HvA" and self.current_player == 'black':
            self.root.after(100, self.run_ai)
        elif self.mode == "AvA":
            self.root.after(300, self.run_ai)

    def check_win(self):
        rk, bk = False, False
        for r in range(10):
            for c in range(9):
                if self.board[r][c] == 'K': rk = True
                if self.board[r][c] == 'k': bk = True
        if not rk:
            self.game_over = True
            self.status_label.config(text="黑方获胜！")
            messagebox.showinfo("结局", "黑方获胜！")
            return True
        elif not bk:
            self.game_over = True
            self.status_label.config(text="红方获胜！")
            messagebox.showinfo("结局", "红方获胜！")
            return True
        return False

    def is_valid_move(self, start, end):
        r1, c1 = start
        r2, c2 = end
        piece = self.board[r1][c1]
        target = self.board[r2][c2]
        
        if not piece: return False
        if start == end: return False
        if target and (piece.isupper() == target.isupper()): return False
        
        pt = piece.lower()
        
        if pt == 'k':
            if piece.isupper():
                if not (7 <= r2 <= 9 and 3 <= c2 <= 5): return False
            else:
                if not (0 <= r2 <= 2 and 3 <= c2 <= 5): return False
            if abs(r1-r2) + abs(c1-c2) != 1: return False
            
        elif pt == 'a':
            if piece.isupper():
                if not (7 <= r2 <= 9 and 3 <= c2 <= 5): return False
            else:
                if not (0 <= r2 <= 2 and 3 <= c2 <= 5): return False
            if abs(r1-r2) != 1 or abs(c1-c2) != 1: return False
            
        elif pt == 'b':
            if piece.isupper():
                if r2 < 5: return False
            else:
                if r2 > 4: return False
            if abs(r1-r2) != 2 or abs(c1-c2) != 2: return False
            if self.board[(r1+r2)//2][(c1+c2)//2]: return False
            
        elif pt == 'n':
            dr, dc = abs(r1-r2), abs(c1-c2)
            if not ((dr==2 and dc==1) or (dr==1 and dc==2)): return False
            if dr == 2:
                if self.board[(r1+r2)//2][c1]: return False
            else:
                if self.board[r1][(c1+c2)//2]: return False
                
        elif pt == 'r':
            if r1 != r2 and c1 != c2: return False
            if self.count_between(start, end) != 0: return False
            
        elif pt == 'c':
            if r1 != r2 and c1 != c2: return False
            cnt = self.count_between(start, end)
            if target:
                if cnt != 1: return False
            else:
                if cnt != 0: return False
        
        elif pt == 'p':
            if piece.isupper():
                if r2 > r1: return False
                if r1 >= 5:
                    if r1-r2!=1 or c1!=c2: return False
                else:
                    if abs(r1-r2)+abs(c1-c2) != 1: return False
            else:
                if r2 < r1: return False
                if r1 <= 4:
                    if r2-r1!=1 or c1!=c2: return False
                else:
                    if abs(r1-r2)+abs(c1-c2) != 1: return False
        
        tmp_board = [row[:] for row in self.board]
        tmp_board[r2][c2] = tmp_board[r1][c1]
        tmp_board[r1][c1] = ''
        if self.is_facing_kings(tmp_board): return False
        
        return True

    def count_between(self, start, end):
        r1, c1 = start
        r2, c2 = end
        cnt = 0
        if r1 == r2:
            mn, mx = min(c1, c2), max(c1, c2)
            for c in range(mn+1, mx):
                if self.board[r1][c]: cnt += 1
        else:
            mn, mx = min(r1, r2), max(r1, r2)
            for r in range(mn+1, mx):
                if self.board[r][c1]: cnt += 1
        return cnt

    def is_facing_kings(self, b):
        rk, bk = None, None
        for r in range(10):
            for c in range(9):
                if b[r][c] == 'K': rk = (r, c)
                if b[r][c] == 'k': bk = (r, c)
        if not rk or not bk: return False
        if rk[1] != bk[1]: return False
        for r in range(bk[0]+1, rk[0]):
            if b[r][rk[1]]: return False
        return True

    def make_move(self, start, end):
        r1, c1 = start
        r2, c2 = end
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = ''
        
        sig = str(self.board) + self.current_player
        self.history.append(sig)
        if len(self.history) > 12:
            self.history.pop(0)

    def run_ai(self):
        self.ai_thinking = True
        self.root.update()
        
        depth = self.search_depth
        is_red = (self.current_player == 'red')
        
        best_move = self.minimax_root(depth, is_red)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
            self.post_move_action()
        else:
            self.game_over = True
            winner = "黑方" if is_red else "红方"
            self.status_label.config(text=f"无路可走，{winner}获胜")
            messagebox.showinfo("结局", f"{winner}获胜")
        
        self.ai_thinking = False

    def get_piece_val(self, p, r, c):
        base = {'k':10000, 'r':900, 'n':450, 'c':450, 'b':200, 'a':200, 'p':100}
        val = base.get(p.lower(), 0)
        if p.lower() == 'p':
            if p.isupper():
                if r < 5: val += 100
                if r < 5 and (c==3 or c==5): val += 20
            else:
                if r > 4: val += 100
                if r > 4 and (c==3 or c==5): val += 20
        return val

    def evaluate(self):
        score = 0
        score += random.randint(-10, 10)
        for r in range(10):
            for c in range(9):
                p = self.board[r][c]
                if not p: continue
                val = self.get_piece_val(p, r, c)
                if p.isupper(): score += val
                else: score -= val
        return score

    def get_all_moves(self, is_red):
        moves = []
        for r in range(10):
            for c in range(9):
                p = self.board[r][c]
                if not p: continue
                if (is_red and p.isupper()) or (not is_red and p.islower()):
                    targets = self.gen_moves(r, c, p)
                    for tr, tc in targets:
                        if self.is_valid_move((r,c), (tr,tc)):
                            priority = 0
                            target = self.board[tr][tc]
                            if target: priority = self.get_piece_val(target, tr, tc)
                            moves.append((priority, (r,c), (tr,tc)))
        moves.sort(key=lambda x: x[0], reverse=True)
        return [ (m[1], m[2]) for m in moves ]

    def gen_moves(self, r, c, p):
        m = []
        pt = p.lower()
        if pt == 'k':
            deltas = [(0,1),(0,-1),(1,0),(-1,0)]
            for dr, dc in deltas:
                nr, nc = r+dr, c+dc
                if 0<=nr<=9 and 0<=nc<=8: m.append((nr,nc))
        elif pt == 'a':
            deltas = [(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr, dc in deltas:
                nr, nc = r+dr, c+dc
                if 0<=nr<=9 and 0<=nc<=8: m.append((nr,nc))
        elif pt == 'b':
            deltas = [(2,2),(2,-2),(-2,2),(-2,-2)]
            for dr, dc in deltas:
                nr, nc = r+dr, c+dc
                if 0<=nr<=9 and 0<=nc<=8: m.append((nr,nc))
        elif pt == 'n':
            deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr, dc in deltas:
                nr, nc = r+dr, c+dc
                if 0<=nr<=9 and 0<=nc<=8: m.append((nr,nc))
        elif pt == 'r' or pt == 'c':
            for i in range(c+1, 9):
                m.append((r, i))
                if self.board[r][i]: break
            for i in range(c-1, -1, -1):
                m.append((r, i))
                if self.board[r][i]: break
            for i in range(r+1, 10):
                m.append((i, c))
                if self.board[i][c]: break
            for i in range(r-1, -1, -1):
                m.append((i, c))
                if self.board[i][c]: break
            if pt == 'c':
                pass 
        elif pt == 'p':
            deltas = [(0,1),(0,-1),(1,0),(-1,0)]
            for dr, dc in deltas:
                nr, nc = r+dr, c+dc
                if 0<=nr<=9 and 0<=nc<=8: m.append((nr,nc))
        return m

    def minimax_root(self, depth, is_red):
        moves = self.get_all_moves(is_red)
        best_val = -999999 if is_red else 999999
        best_move = None
        
        alpha = -999999
        beta = 999999
        
        for start, end in moves:
            p = self.board[start[0]][start[1]]
            t = self.board[end[0]][end[1]]
            self.make_move(start, end)
            
            sig = str(self.board) + ('black' if is_red else 'red')
            rep = 0
            if self.history.count(sig) > 1:
                rep = -500 if is_red else 500

            val = self.minimax(depth - 1, alpha, beta, not is_red)
            val += rep
            
            print(f"Move {start}->{end}: {val}")
            
            self.board[start[0]][start[1]] = p
            self.board[end[0]][end[1]] = t
            self.history.pop()
            
            if is_red:
                if val > best_val:
                    best_val = val
                    best_move = (start, end)
                alpha = max(alpha, val)
            else:
                if val < best_val:
                    best_val = val
                    best_move = (start, end)
                beta = min(beta, val)
                
        return best_move

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return self.evaluate()
            
        if is_maximizing:
            max_eval = -999999
            moves = self.get_all_moves(True)
            for start, end in moves:
                p = self.board[start[0]][start[1]]
                t = self.board[end[0]][end[1]]
                self.make_move(start, end)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board[start[0]][start[1]] = p
                self.board[end[0]][end[1]] = t
                self.history.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = 999999
            moves = self.get_all_moves(False)
            for start, end in moves:
                p = self.board[start[0]][start[1]]
                t = self.board[end[0]][end[1]]
                self.make_move(start, end)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board[start[0]][start[1]] = p
                self.board[end[0]][end[1]] = t
                self.history.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

if __name__ == "__main__":
    app = ChineseChess()
    app.root.mainloop()
