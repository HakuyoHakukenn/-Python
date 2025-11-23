import tkinter as tk
import random

class MatrixRain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("数字雨(白杨博贤)")
        self.root.configure(bg='black')
        
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        self.font_size = 14
        self.columns = self.width // self.font_size
        self.drops = [random.randint(-50, 0) for _ in range(self.columns)]
        
        self.chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz白杨博贤"
        
        self.update()
        self.root.mainloop()

    def update(self):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='black', stipple='gray25')

        for i in range(len(self.drops)):
            text = random.choice(self.chars)
            x = i * self.font_size
            y = self.drops[i] * self.font_size
            
            color_intensity = random.randint(50, 255)
            color = f'#{0:02x}{color_intensity:02x}{0:02x}'
            
            self.canvas.create_text(x, y, text=text, fill=color, font=("Consolas", self.font_size), tag="rain")
            
            if self.drops[i] * self.font_size > self.height and random.random() > 0.975:
                self.drops[i] = 0
                self.canvas.create_rectangle(x-2, 0, x+self.font_size+2, self.height, fill="black", outline="")
            
            self.drops[i] += 1
            
        if len(self.canvas.find_all()) > 3000:
            self.canvas.delete("all")

        self.root.after(30, self.update)

if __name__ == "__main__":
    MatrixRain()
