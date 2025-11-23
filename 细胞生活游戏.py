import tkinter as tk
import random

class GameOfLife:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("细胞生活游戏 (空格:暂停/开始, R:随机, C:清空, 鼠标:绘图)  游戏制作:白杨博贤")
        
        self.width = 800
        self.height = 600
        self.cell_size = 10
        self.cols = self.width // self.cell_size
        self.rows = self.height // self.cell_size
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.running = False
        
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_click)
        self.root.bind("<space>", self.toggle_run)
        self.root.bind("<c>", self.clear_grid)
        self.root.bind("<r>", self.random_grid)
        
        self.random_grid()
        self.update()
        self.root.mainloop()

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    x1 = c * self.cell_size
                    y1 = r * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#00FF00", outline="gray")

    def update(self):
        if self.running:
            new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    state = self.grid[r][c]
                    neighbors = self.count_neighbors(r, c)
                    
                    if state == 0 and neighbors == 3:
                        new_grid[r][c] = 1
                    elif state == 1 and (neighbors < 2 or neighbors > 3):
                        new_grid[r][c] = 0
                    else:
                        new_grid[r][c] = state
            self.grid = new_grid
            self.draw_grid()
        
        self.root.after(100, self.update)

    def count_neighbors(self, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                nr, nc = r + i, c + j
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    count += self.grid[nr][nc]
        return count

    def handle_click(self, event):
        c = event.x // self.cell_size
        r = event.y // self.cell_size
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = 1
            self.draw_grid()

    def toggle_run(self, event=None):
        self.running = not self.running

    def clear_grid(self, event=None):
        self.running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def random_grid(self, event=None):
        self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

if __name__ == "__main__":
    GameOfLife()
