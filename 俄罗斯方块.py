import tkinter as tk
import random

class Tetris:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("俄罗斯方块(游戏制作:白杨博贤)")
        self.width = 300
        self.height = 600
        self.cell_size = 30
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 0], [1, 1, 1]]
        ]
        
        self.colors = ['cyan', 'yellow', 'orange', 'blue', 'green', 'red', 'purple']
        
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.score = 0
        self.game_over = False
        
        self.root.bind("<Left>", lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))
        self.root.bind("<Down>", lambda e: self.move(0, 1))
        self.root.bind("<Up>", lambda e: self.rotate())
        
        self.new_piece()
        self.run()
        self.root.mainloop()

    def new_piece(self):
        self.current_shape = random.choice(self.shapes)
        self.current_color = random.choice(self.colors)
        self.cur_x = 3
        self.cur_y = 0
        
        if self.check_collision(self.current_shape, self.cur_x, self.cur_y):
            self.game_over = True

    def check_collision(self, shape, offset_x, offset_y):
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                if cell:
                    if cx + offset_x < 0 or cx + offset_x >= 10 or cy + offset_y >= 20:
                        return True
                    if cy + offset_y >= 0 and self.grid[cy + offset_y][cx + offset_x]:
                        return True
        return False

    def rotate(self):
        if self.game_over: return
        new_shape = list(zip(*self.current_shape[::-1]))
        if not self.check_collision(new_shape, self.cur_x, self.cur_y):
            self.current_shape = new_shape
            self.draw()

    def move(self, dx, dy):
        if self.game_over: return
        if not self.check_collision(self.current_shape, self.cur_x + dx, self.cur_y + dy):
            self.cur_x += dx
            self.cur_y += dy
            self.draw()
        elif dy > 0:
            self.freeze()

    def freeze(self):
        for cy, row in enumerate(self.current_shape):
            for cx, cell in enumerate(row):
                if cell:
                    self.grid[cy + self.cur_y][cx + self.cur_x] = self.current_color
        self.clear_lines()
        self.new_piece()
        self.draw()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(c == 0 for c in row)]
        lines_cleared = 20 - len(new_grid)
        self.score += lines_cleared * 100
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(10)])
        self.grid = new_grid

    def draw(self):
        self.canvas.delete("all")
        
        for y in range(20):
            for x in range(10):
                if self.grid[y][x]:
                    self.draw_cell(x, y, self.grid[y][x])
                    
        if not self.game_over:
            for cy, row in enumerate(self.current_shape):
                for cx, cell in enumerate(row):
                    if cell:
                        self.draw_cell(cx + self.cur_x, cy + self.cur_y, self.current_color)
        
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", fill="white", anchor="nw")
        
        if self.game_over:
            self.canvas.create_text(150, 300, text="GAME OVER", fill="white", font=("Arial", 30))

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(x*30, y*30, x*30+30, y*30+30, fill=color, outline="white")

    def run(self):
        if not self.game_over:
            self.move(0, 1)
            self.root.after(500, self.run)

if __name__ == "__main__":
    Tetris()
