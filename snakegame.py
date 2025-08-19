import tkinter as tk
import random

SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#97F597"
FOOD_COLOR = "#6498F8"
BACKGROUND_COLOR = "#111111"
SPEED = 100  

def start_snake_game():
    game_window = tk.Toplevel()
    game_window.title("Snake Game")
    screen_width = game_window.winfo_screenwidth() - 15
    screen_height = game_window.winfo_screenheight() - 40
    game_window.geometry(f"{screen_width}x{screen_height}")
    game_window.configure(bg=BACKGROUND_COLOR)

    global WIDTH, HEIGHT
    WIDTH, HEIGHT = screen_width, screen_height

    score = 0

    canvas = tk.Canvas(game_window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
    canvas.pack()

    score_text = canvas.create_text(60, 30, text=f"Score: {score}", font=("Arial", 24), fill="white", anchor="w")

    class Snake:
        def __init__(self):
            self.body_size = BODY_PARTS
            self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
            self.squares = []

            for x, y in self.coordinates:
                square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
                self.squares.append(square)

    class Food:
        def __init__(self):
            while True:
                x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
                y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
                if [x, y] not in snake.coordinates:
                    break
            self.coordinates = [x, y]
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    def update_score():
        nonlocal score
        score += 1
        canvas.itemconfigure(score_text, text=f"Score: {score}")

    def next_turn():
        nonlocal direction, food

        x, y = snake.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        new_head = [x, y]
        snake.coordinates.insert(0, new_head)
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.insert(0, square)

        if new_head == food.coordinates:
            canvas.delete("food")
            food = Food()
            update_score()
        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if check_collision():
            game_over()
        else:
            game_window.after(SPEED, next_turn)

    def change_direction(new_direction):
        nonlocal direction
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if new_direction != opposites.get(direction):
            direction = new_direction

    def check_collision():
        x, y = snake.coordinates[0]

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True

        for body_part in snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        return False

    def restart_game():
        game_window.destroy()
        start_snake_game()

    def game_over():
        canvas.delete(tk.ALL)
        canvas.create_text(WIDTH // 2, HEIGHT // 2 - 60, text="GAME OVER", fill="red", font=("Arial", 48))
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Final Score: {score}", fill="white", font=("Arial", 36))

        restart_btn = tk.Button(game_window, text="Restart", font=("Arial", 20), bg="#72db8e", fg="#E6F3E5",
                                activebackground="#6CD463", bd=5, relief="ridge", cursor="hand2", command=restart_game)
        restart_btn_window = canvas.create_window(WIDTH // 2 - 100, HEIGHT // 2 + 80, window=restart_btn)

     
        quit_btn = tk.Button(game_window, text="Quit", font=("Arial", 20), bg="#9596f5", fg="#fffbfb",
                             activebackground="#95d9f3", bd=5, relief="ridge", cursor="hand2", command=game_window.destroy)
        quit_btn_window = canvas.create_window(WIDTH // 2 + 100, HEIGHT // 2 + 80, window=quit_btn)

    direction = "right"
    snake = Snake()
    food = Food()

    canvas.focus_set()
    canvas.bind_all("<Up>", lambda event: change_direction("up"))
    canvas.bind_all("<Down>", lambda event: change_direction("down"))
    canvas.bind_all("<Left>", lambda event: change_direction("left"))
    canvas.bind_all("<Right>", lambda event: change_direction("right"))

    next_turn()
    game_window.mainloop()
