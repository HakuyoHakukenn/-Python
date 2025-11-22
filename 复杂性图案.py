import turtle
import random
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("艺术图案生成")
screen.setup(800, 800)

artist = turtle.Turtle()
artist.speed(0)
artist.hideturtle()

color_palette = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#6A0572", "#1A535C", 
                "#FF9F1C", "#2EC4B6", "#E71D36", "#FDFFFC", "#011627"]

def create_circular_spiral(center_x, center_y, start_size, rotation):
    artist.penup()
    artist.goto(center_x, center_y)
    artist.pendown()
    
    for circle_num in range(36):
        current_color = color_palette[circle_num % len(color_palette)]
        artist.color(current_color)
        artist.circle(start_size)
        artist.right(rotation)
        start_size += 2

def draw_polygon_pattern(pattern_x, pattern_y, sides_count, side_length):
    artist.penup()
    artist.goto(pattern_x, pattern_y)
    artist.pendown()
    
    for side_num in range(sides_count):
        current_color = color_palette[side_num % len(color_palette)]
        artist.color(current_color)
        
        for _ in range(sides_count):
            artist.forward(side_length)
            artist.right(360 / sides_count)
        
        artist.right(360 / sides_count)

def grow_branches(branch_size, branch_angle, levels_remaining):
    if levels_remaining == 0:
        return
    
    branch_color = random.choice(color_palette)
    artist.color(branch_color)
    artist.forward(branch_size)
    
    current_position = artist.position()
    current_direction = artist.heading()
    
    artist.right(branch_angle)
    grow_branches(branch_size * 0.7, branch_angle, levels_remaining - 1)
    
    artist.penup()
    artist.goto(current_position)
    artist.setheading(current_direction)
    artist.pendown()
    
    artist.left(branch_angle)
    grow_branches(branch_size * 0.7, branch_angle, levels_remaining - 1)
    
    artist.penup()
    artist.goto(current_position)
    artist.setheading(current_direction)
    artist.pendown()

def place_star(star_x, star_y, star_size, points_count):
    artist.penup()
    artist.goto(star_x, star_y)
    artist.pendown()
    
    star_color = random.choice(color_palette)
    artist.color(star_color)
    
    point_angle = 180 - (180 / points_count)
    
    artist.begin_fill()
    for _ in range(points_count):
        artist.forward(star_size)
        artist.right(point_angle)
    artist.end_fill()

def build_mandala(mandala_x, mandala_y, layer_count, base_size):
    artist.penup()
    artist.goto(mandala_x, mandala_y)
    artist.pendown()
    
    for layer_num in range(layer_count):
        layer_color = color_palette[layer_num % len(color_palette)]
        artist.color(layer_color)
        artist.circle(base_size)
        
        for decoration in range(8):
            artist.penup()
            artist.goto(mandala_x, mandala_y)
            artist.pendown()
            artist.setheading(decoration * 45)
            artist.forward(base_size * 0.7)
            artist.circle(base_size * 0.3)
        
        base_size += 20

def generate_artwork():
    create_circular_spiral(0, 0, 10, 10)
    
    for polygon_num in range(6):
        position_x = 200 * math.cos(polygon_num * math.pi/3)
        position_y = 200 * math.sin(polygon_num * math.pi/3)
        draw_polygon_pattern(position_x, position_y, 5 + polygon_num, 30)
    
    artist.penup()
    artist.goto(-300, -200)
    artist.pendown()
    artist.setheading(90)
    grow_branches(80, 30, 6)
    
    for _ in range(10):
        random_x = random.randint(-350, 350)
        random_y = random.randint(-350, 350)
        star_size = random.randint(10, 30)
        star_points = random.randint(5, 8)
        place_star(random_x, random_y, star_size, star_points)
    
    build_mandala(250, -250, 5, 40)

generate_artwork()
turtle.done()