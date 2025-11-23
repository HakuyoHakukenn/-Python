import tkinter as tk
import random

class Star:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.reset()

    def reset(self):
        self.x = random.randint(-self.w, self.w)
        self.y = random.randint(-self.h, self.h)
        self.z = random.randint(100, self.w)
        
    def update(self):
        self.z -= 10
        if self.z < 1:
            self.reset()

class Starfield:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("粒子效果(白杨博贤)")
        self.root.configure(bg='black')
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.stars = [Star(self.width, self.height) for _ in range(400)]
        self.cx = self.width // 2
        self.cy = self.height // 2
        
        self.animate()
        self.root.mainloop()

    def animate(self):
        self.canvas.delete("all")
        
        for s in self.stars:
            s.update()
            
            factor = 200.0 / s.z
            sx = int(s.x * factor + self.cx)
            sy = int(s.y * factor + self.cy)
            
            r = int((1 - s.z / self.width) * 5)
            if r < 1: r = 1
            
            if 0 <= sx < self.width and 0 <= sy < self.height:
                color_val = int((1 - s.z / self.width) * 255)
                if color_val < 0: color_val = 0
                if color_val > 255: color_val = 255
                color = f'#{color_val:02x}{color_val:02x}{color_val:02x}'
                
                self.canvas.create_oval(sx-r, sy-r, sx+r, sy+r, fill=color, outline="")
                
        self.root.after(16, self.animate)

if __name__ == "__main__":
    Starfield()
