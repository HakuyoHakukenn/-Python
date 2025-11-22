import random
import sys

def game():
    number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print("猜数字游戏！猜一个1到100之间的数字。")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"第{attempts + 1}次尝试，请输入你的猜测: "))
        except ValueError:
            print("请输入一个有效的数字！")
            continue
        
        if guess < number:
            print("太小了！")
        elif guess > number:
            print("太大了！")
        else:
            print(f"恭喜！你猜对了！数字就是{number}。")
            play_again()
            return
        
        attempts += 1
    
    print(f"游戏结束！正确答案是{number}。")
    play_again()

def play_again():
    choice = input("再玩一次？(y/n): ").lower()
    if choice == 'y':
        game()
    else:
        print("谢谢游玩！")
        sys.exit()

if __name__ == "__main__":
    game()
