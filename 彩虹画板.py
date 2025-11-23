import tkinter as tk
import colorsys

class RainbowPaint:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("彩虹画板 (右键清空)白杨博贤")
        
        self.width = 800
        self.height = 600
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        self.hue = 0.0
        self.prev_x = None
        self.prev_y = None
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Button-3>", self.clear)
        
        self.root.mainloop()

    def paint(self, event):
        x, y = event.x, event.y
        
        rgb = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        color = "#%02x%02x%02x" % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        
        if self.prev_x and self.prev_y:
            self.canvas.create_line(self.prev_x, self.prev_y, x, y, 
                                  fill=color, width=5, capstyle=tk.ROUND, smooth=True)
        
        self.prev_x = x
        self.prev_y = y
        
        self.hue += 0.01
        if self.hue > 1.0:
            self.hue = 0.0

    def reset(self, event):
        self.prev_x = None
        self.prev_y = None

    def clear(self, event):
        self.canvas.delete("all")

if __name__ == "__main__":
    RainbowPaint()
