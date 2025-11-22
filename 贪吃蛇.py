import turtle
import time
import random


window = turtle.Screen()
window.title("贪吃蛇游戏 - 使用方向键或WASD控制")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)


snake_head = turtle.Turtle()
snake_head.speed(0)
snake_head.shape("square")
snake_head.color("green")
snake_head.penup()
snake_head.goto(0, 0)
snake_head.direction = "stop"


food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)


score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("得分: 0", align="center", font=("Arial", 24, "normal"))


border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-290, -290)
border.pendown()
border.pensize(2)
for _ in range(4):
    border.forward(580)
    border.left(90)
border.hideturtle()


control_info = turtle.Turtle()
control_info.speed(0)
control_info.color("gray")
control_info.penup()
control_info.hideturtle()
control_info.goto(0, -270)
control_info.write("使用方向键或WASD控制移动", align="center", font=("Arial", 12, "normal"))


score = 0
segments = []
delay = 0.1


def move_up():
    if snake_head.direction != "down":
        snake_head.direction = "up"

def move_down():
    if snake_head.direction != "up":
        snake_head.direction = "down"

def move_left():
    if snake_head.direction != "right":
        snake_head.direction = "left"

def move_right():
    if snake_head.direction != "left":
        snake_head.direction = "right"

def move():
    if snake_head.direction == "up":
        y = snake_head.ycor()
        snake_head.sety(y + 20)
    
    if snake_head.direction == "down":
        y = snake_head.ycor()
        snake_head.sety(y - 20)
    
    if snake_head.direction == "left":
        x = snake_head.xcor()
        snake_head.setx(x - 20)
    
    if snake_head.direction == "right":
        x = snake_head.xcor()
        snake_head.setx(x + 20)


window.listen()
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")


window.onkeypress(move_up, "w")
window.onkeypress(move_down, "s")
window.onkeypress(move_left, "a")
window.onkeypress(move_right, "d")


while True:
    window.update()
    
    
    if (snake_head.xcor() > 280 or snake_head.xcor() < -280 or 
        snake_head.ycor() > 280 or snake_head.ycor() < -280):
        time.sleep(1)
        snake_head.goto(0, 0)
        snake_head.direction = "stop"
        
        
        for segment in segments:
            segment.goto(1000, 1000)
        
        
        segments.clear()
        
        
        score = 0
        score_display.clear()
        score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
        
        
        delay = 0.1
    
    
    if snake_head.distance(food) < 20:
        
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)
        
        
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("light green")
        new_segment.penup()
        segments.append(new_segment)
        
        
        score += 10
        score_display.clear()
        score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
        
        
        delay -= 0.001
    
    
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)
    
    
    if len(segments) > 0:
        x = snake_head.xcor()
        y = snake_head.ycor()
        segments[0].goto(x, y)
    
    
    move()
    
    
    for segment in segments:
        if segment.distance(snake_head) < 20:
            time.sleep(1)
            snake_head.goto(0, 0)
            snake_head.direction = "stop"
            
            
            for segment in segments:
                segment.goto(1000, 1000)
            
            
            segments.clear()
            
            
            score = 0
            score_display.clear()
            score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
            
            
            delay = 0.1
    
    
    time.sleep(delay)


window.mainloop()
