import turtle
import time
import random

# 设置游戏窗口
window = turtle.Screen()
window.title("贪吃蛇游戏 - 使用方向键或WASD控制")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)  # 关闭自动刷新，手动控制刷新

# 蛇头
snake_head = turtle.Turtle()
snake_head.speed(0)
snake_head.shape("square")
snake_head.color("green")
snake_head.penup()
snake_head.goto(0, 0)
snake_head.direction = "stop"

# 食物
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# 分数显示
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("得分: 0", align="center", font=("Arial", 24, "normal"))

# 游戏边界
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

# 控制说明
control_info = turtle.Turtle()
control_info.speed(0)
control_info.color("gray")
control_info.penup()
control_info.hideturtle()
control_info.goto(0, -270)
control_info.write("使用方向键或WASD控制移动", align="center", font=("Arial", 12, "normal"))

# 游戏变量
score = 0
segments = []
delay = 0.1

# 移动函数
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

# 键盘绑定 - 方向键
window.listen()
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")

# 键盘绑定 - WASD键
window.onkeypress(move_up, "w")
window.onkeypress(move_down, "s")
window.onkeypress(move_left, "a")
window.onkeypress(move_right, "d")

# 游戏主循环
while True:
    window.update()
    
    # 检查是否撞到边界
    if (snake_head.xcor() > 280 or snake_head.xcor() < -280 or 
        snake_head.ycor() > 280 or snake_head.ycor() < -280):
        time.sleep(1)
        snake_head.goto(0, 0)
        snake_head.direction = "stop"
        
        # 隐藏所有身体段
        for segment in segments:
            segment.goto(1000, 1000)
        
        # 清空身体段列表
        segments.clear()
        
        # 重置分数
        score = 0
        score_display.clear()
        score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
        
        # 重置延迟
        delay = 0.1
    
    # 检查是否吃到食物
    if snake_head.distance(food) < 20:
        # 移动食物到随机位置
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)
        
        # 添加新的身体段
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("light green")
        new_segment.penup()
        segments.append(new_segment)
        
        # 增加分数
        score += 10
        score_display.clear()
        score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
        
        # 稍微加快游戏速度
        delay -= 0.001
    
    # 移动身体段（从后往前）
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)
    
    # 移动第一节身体段到蛇头位置
    if len(segments) > 0:
        x = snake_head.xcor()
        y = snake_head.ycor()
        segments[0].goto(x, y)
    
    # 移动蛇头
    move()
    
    # 检查是否撞到自己
    for segment in segments:
        if segment.distance(snake_head) < 20:
            time.sleep(1)
            snake_head.goto(0, 0)
            snake_head.direction = "stop"
            
            # 隐藏所有身体段
            for segment in segments:
                segment.goto(1000, 1000)
            
            # 清空身体段列表
            segments.clear()
            
            # 重置分数
            score = 0
            score_display.clear()
            score_display.write(f"得分: {score}", align="center", font=("Arial", 24, "normal"))
            
            # 重置延迟
            delay = 0.1
    
    # 游戏速度控制
    time.sleep(delay)

# 保持窗口打开
window.mainloop()