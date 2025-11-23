import tkinter as tk
import random

class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        self.root.wm_attributes("-transparentcolor", "white")
        
        self.width = 100
        self.height = 100
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        
        self.x = random.randint(0, self.ws - self.width)
        self.y = random.randint(0, self.hs - self.height)
        self.dx = 3
        self.dy = 3
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        self.draw_ghost()
        
        self.canvas.bind("<Double-1>", lambda e: self.root.destroy())
        
        self.update_position()
        self.root.mainloop()

    def draw_ghost(self):
        self.canvas.create_oval(10, 10, 90, 90, fill="gray", outline="gray")
        self.canvas.create_polygon(10, 50, 10, 100, 30, 80, 50, 100, 70, 80, 90, 100, 90, 50, fill="gray", outline="gray")
        
        self.canvas.create_oval(30, 35, 40, 45, fill="black")
        self.canvas.create_oval(60, 35, 70, 45, fill="black")
        
        self.canvas.create_oval(45, 55, 55, 65, fill="pink", outline="")

    def update_position(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.x <= 0 or self.x >= self.ws - self.width:
            self.dx = -self.dx
        if self.y <= 0 or self.y >= self.hs - self.height:
            self.dy = -self.dy
            
        self.root.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        
        if random.randint(0, 20) == 0:
            self.dx = random.choice([-3, -2, 2, 3])
            self.dy = random.choice([-3, -2, 2, 3])
            
        self.root.after(20, self.update_position)

if __name__ == "__main__":
    DesktopPet()
