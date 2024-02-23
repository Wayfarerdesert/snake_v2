from tkinter import *
import random
from random import choice


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 25
BODY_PARTS = 1
HEAD_COLOR = "#EE1815" #! pending application
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#EE1815"
BACKGROUND_COLOR = "#252526"

STARTING_DIRECTION = ["up", "down", "left", "right"]

score_font = ("Orbitron", 20)
game_over_font = ("consolas", 70)


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates.append([x, y])

            for x, y in self.coordinates:
                square = canvas.create_rectangle(
                    x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
                )
                self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    global score, SPEED

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
        y %= GAME_HEIGHT #prevents it from colliding on the sides

    elif direction == "down":
        y += SPACE_SIZE
        y %= GAME_HEIGHT #prevents it from colliding on the sides

    elif direction == "left":
        x -= SPACE_SIZE
        x %= GAME_WIDTH #prevents it from colliding on the sides

    elif direction == "right":
        x += SPACE_SIZE
        x %= GAME_WIDTH #prevents it from colliding on the sides

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )

    # update snake list of squares
    snake.squares.insert(0, square)

    # add the eaten squares to the body
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        # Check if the score increased 5 times
        if score % 5 == 0:
            SPEED -= 10  # Increase speed

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()
    # add the eaten squares to the body END

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:  # If there is no collision the game continues
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    # prevent moving 180º
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    # If it leaves the board the game ends
    # if x < 0 or x >= GAME_WIDTH:
    #     print("GAME OVER")
    #     return True
    # elif y < 0 or y >= GAME_HEIGHT:
    #     print("GAME OVER")
    #     return True

    # If he collides with his own body, the game ends.
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=(game_over_font),
        text="GAME OVER",
        fill="green",
        tag="gameover",
    )


window = Tk()
window.title("Snake Game")
# prevent the window from being resized
window.resizable(False, False)

score = 0
direction = "down"
# direction = choice(STARTING_DIRECTION)

label = Label(window, text="Score:{}".format(score), font=(score_font))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# * center the window on the screen
# window_width = window.winfo_width()
# window_height = window.winfo_height()
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()

# x = int((screen_width / 2) - (window_width / 2))
# y = int((screen_height / 2) - (window_height / 2))

# window.geometry(f"{window_width}x{window_height}+{x}+{y}")
# * center the window on the screen END

# controls for navigation
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))


# *MAIN ######################################################
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
