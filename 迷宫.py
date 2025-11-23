import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_maze(maze, player_pos, enemy_pos, goal_pos):
    clear_screen()
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (x, y) == player_pos:
                print('P', end='')
            elif (x, y) == enemy_pos:
                print('E', end='')
            elif (x, y) == goal_pos:
                print('G', end='')
            else:
                print(cell, end='')
        print()

def create_maze():
    return [
        ['#','#','#','#','#','#','#','#','#','#'],
        ['#',' ',' ',' ',' ',' ',' ',' ',' ','#'],
        ['#',' ','#','#',' ','#','#',' ',' ','#'],
        ['#',' ','#',' ',' ',' ','#',' ',' ','#'],
        ['#',' ',' ',' ','#',' ',' ',' ',' ','#'],
        ['#',' ','#',' ','#',' ','#',' ',' ','#'],
        ['#',' ','#',' ',' ',' ','#',' ',' ','#'],
        ['#',' ','#','#','#','#','#',' ',' ','#'],
        ['#',' ',' ',' ',' ',' ',' ',' ',' ','#'],
        ['#','#','#','#','#','#','#','#','#','#']
    ]

def random_terrain(maze, player_pos, enemy_pos, goal_pos):
    for y in range(1, len(maze)-1):
        for x in range(1, len(maze[0])-1):
            if (x, y) != player_pos and (x, y) != enemy_pos and (x, y) != goal_pos:
                if random.random() < 0.1:
                    maze[y][x] = '#' if maze[y][x] == ' ' else ' '
    return maze

def move_player(maze, position, direction):
    x, y = position
    new_x, new_y = x, y
    
    if direction == 'w':
        new_y -= 1
    elif direction == 's':
        new_y += 1
    elif direction == 'a':
        new_x -= 1
    elif direction == 'd':
        new_x += 1
    
    if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
        if maze[new_y][new_x] != '#':
            return (new_x, new_y)
    
    return position

def move_enemy(maze, enemy_pos, player_pos):
    ex, ey = enemy_pos
    px, py = player_pos
    
    possible_moves = []
    
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_x, new_y = ex + dx, ey + dy
        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            if maze[new_y][new_x] != '#':
                possible_moves.append((new_x, new_y))
    
    if possible_moves:
        return random.choice(possible_moves)
    
    return enemy_pos

def maze_game():
    maze = create_maze()
    player_pos = (1, 1)
    enemy_pos = (8, 1)
    goal_pos = (8, 8)
    score = 0
    terrain_change_counter = 0
    
    while True:
        print_maze(maze, player_pos, enemy_pos, goal_pos)
        print(f"分数: {score}")
        print("移动: w(上), s(下), a(左), d(右)")
        print("目标: 到达终点(G)，避开敌人(E)")
        print("注意: 地形会随机变化!")
        print("游戏制作：白杨博贤")
        
        if player_pos == enemy_pos:
            print("被敌人抓住了！游戏结束！")
            break
        
        if player_pos == goal_pos:
            print("恭喜！你到达了终点！")
            break
        
        direction = input("输入移动方向: ").lower()
        
        if direction not in ['w', 's', 'a', 'd']:
            continue
        
        player_pos = move_player(maze, player_pos, direction)
        enemy_pos = move_enemy(maze, enemy_pos, player_pos)
        score += 1
        terrain_change_counter += 1
        
        if terrain_change_counter >= 5:
            maze = random_terrain(maze, player_pos, enemy_pos, goal_pos)
            terrain_change_counter = 0
    
    print(f"最终分数: {score}")
    

if __name__ == "__main__":
    maze_game()
