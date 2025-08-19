import tkinter as tk
from PIL import Image, ImageTk
from tictactoe import start_tictactoe
from car_racing import start_car_racing
from word_scramble import start_word_scramble
from snakegame import start_snake_game

def main_menu():
    root = tk.Tk()
    root.title("GameHub")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.resizable(False, False)
    bg_image = Image.open("pythonbg.webp").resize((screen_width, screen_height)).convert("RGBA")
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    
    title = tk.Label(root, text="🎮 Welcome to GameHub 🎮",
                     font=("Helvetica", 42, "bold"),
                     fg="#ffffff",
                     bg="#B0AAFF",
                     bd=3,
                     relief="solid")
    canvas.create_window(screen_width//2, 100, window=title)

    # Button style
    btn_params = {
        "width": 30,
        "height": 2,
        "font": ("Helvetica", 18, "bold"),
        "bg": "#9cf0b1",
        "fg": "#235522",
        "activebackground": "#D9F7D6",
        "bd": 3,
        "relief": "ridge",
        "cursor": "hand2"
    }

 
    start_y = 220
    gap = 120

    canvas.create_window(screen_width//2, start_y, window=tk.Button(root, text="Tic-Tac-Toe", command=start_tictactoe, **btn_params))
    canvas.create_window(screen_width//2, start_y + gap, window=tk.Button(root, text="Car Racing", command=start_car_racing, **btn_params))
    canvas.create_window(screen_width//2, start_y + 2*gap, window=tk.Button(root, text="Word Scramble", command=start_word_scramble, **btn_params))
    canvas.create_window(screen_width//2, start_y + 3*gap, window=tk.Button(root, text="Snake Game", command=start_snake_game, **btn_params))
    quit_button = tk.Button(root, text="Quit", command=root.destroy, **btn_params)
    canvas.create_window(screen_width//2, start_y + 4*gap, window=quit_button)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
