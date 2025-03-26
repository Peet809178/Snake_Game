import tkinter
import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #hide pygame support prompt
import pygame

#music
pygame.init()
pygame.mixer.music.load('slither.mp3')
pygame.mixer.music.play(loops=-1, start=2)

#sound effects
collect = pygame.mixer.Sound('collect.mp3')
crash = pygame.mixer.Sound('crash.mp3')

#constants
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = ROWS * TILE_SIZE
WINDOW_HEIGHT = COLS * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game

snake = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
food = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
fruit = 0

def change_direction(e): #event
    
    ##testing key input
    #print(e)
    #print(e.keysym)
    
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (e.keysym == "Up" or e.keysym == "w") and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" or e.keysym == "s") and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" or e.keysym == "a") and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" or e.keysym == "d") and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, fruit
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        crash.play()
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            crash.play()
            return
        
    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(snake.x, snake.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        fruit += 1
        collect.play()

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if(i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def restart_game(e):  # Optional event parameter for key binding
    global snake, food, snake_body, velocityX, velocityY, game_over, fruit
    # Reset game variables
    snake = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
    food = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    fruit = 0
    pygame.mixer.music.play(loops=-1, start=2)  # Restart background music
    window.after_cancel(window.timer)  # Cancel the previous timer
    draw()  # Redraw the game

def draw():
    global snake, food, snake_body, game_over, fruit

    move()
    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if game_over:
        # Display game over text
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50, font="arial 60", text="GAME OVER", fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20, font="arial 20", text=f"Fruit: {fruit}", fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 70, font="arial 20", text="Press any key to restart.", fill="white")
        pygame.mixer.music.stop()
    else:
        # Display fruit
        canvas.create_text(WINDOW_WIDTH / 2, 30, font="arial 20", text=f"Fruit: {fruit}", fill="white")

    window.after(100, draw)  # 100ms = 1/10 second, 10 frames per second

draw()

def handle_keypress(e):
    if game_over:
        restart_game(e)
    else:
        change_direction(e)

window.bind("<KeyPress>", handle_keypress)
window.mainloop()
