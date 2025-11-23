import tkinter as tk
import random

class Ball:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 20)
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)
        self.color = random.choice(['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'])
        self.gravity = 0.5
        self.friction = 0.8
        self.floor = h

    def update(self, w):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        
        if self.x + self.radius > w:
            self.x = w - self.radius
            self.vx *= -self.friction
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -self.friction
            
        if self.y + self.radius > self.floor:
            self.y = self.floor - self.radius
            self.vy *= -self.friction
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -self.friction

class PhysicsSim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("物理弹球 (鼠标左击生成)白杨博贤")
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        
        self.balls = []
        
        self.canvas.bind("<Button-1>", self.add_ball)
        self.canvas.bind("<B1-Motion>", self.add_ball)
        
        self.update()
        self.root.mainloop()

    def add_ball(self, event):
        self.balls.append(Ball(event.x, event.y, self.height))

    def update(self):
        self.canvas.delete("all")
        
        for b in self.balls:
            b.update(self.width)
            self.canvas.create_oval(b.x-b.radius, b.y-b.radius, 
                                  b.x+b.radius, b.y+b.radius, 
                                  fill=b.color, outline="black")
            
        if len(self.balls) > 100:
            self.balls.pop(0)
            
        self.root.after(20, self.update)

if __name__ == "__main__":
    PhysicsSim()
