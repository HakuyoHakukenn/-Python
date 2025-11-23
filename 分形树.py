import turtle
import random

def draw_tree(branch_len, t):
    if branch_len > 5:
        if branch_len < 20:
            t.color("green")
        else:
            t.color("brown")
        
        t.pensize(branch_len / 10)
        t.forward(branch_len)
        
        angle = random.randint(15, 45)
        sub_len = random.uniform(0.6, 0.8)
        
        t.right(angle)
        draw_tree(branch_len * sub_len, t)
        
        t.left(angle * 2)
        draw_tree(branch_len * sub_len, t)
        
        t.right(angle)
        t.backward(branch_len)

def main():
    t = turtle.Turtle()
    w = turtle.Screen()
    w.title("Python 分形树(白杨博贤)")
    w.bgcolor("black")
    
    t.left(90)
    t.speed(0)
    t.color("brown")
    
    t.penup()
    t.goto(0, -250)
    t.pendown()
    
    draw_tree(120, t)
    w.exitonclick()

if __name__ == "__main__":
    main()
