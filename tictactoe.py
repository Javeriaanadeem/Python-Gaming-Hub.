import tkinter as tk
from tkinter import messagebox

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def get_both_player_names():
    dialog = tk.Toplevel()
    dialog.title("Enter Player Names")
    dialog.configure(bg="#c8d0da")
    center_window(dialog, 350, 250)

    p1_var = tk.StringVar()
    p2_var = tk.StringVar()

    tk.Label(dialog, text="Enter Player 1 Name (X):", font=("Arial", 12), bg="#f0f0f0").pack(pady=(20, 5))
    tk.Entry(dialog, textvariable=p1_var, font=("Arial", 12)).pack(pady=5)

    tk.Label(dialog, text="Enter Player 2 Name (O):", font=("Arial", 12), bg="#f0f0f0").pack(pady=(20, 5))
    tk.Entry(dialog, textvariable=p2_var, font=("Arial", 12)).pack(pady=5)

    def on_submit():
        if p1_var.get().strip() and p2_var.get().strip():
            dialog.destroy()
        else:
            messagebox.showwarning("Missing Info", "Please enter both player names.")

    tk.Button(dialog, text="Start Game", command=on_submit, bg="#add8e6", font=("Arial", 11)).pack(pady=20)

    dialog.grab_set()
    dialog.wait_window()

    return p1_var.get(), p2_var.get()

def start_tictactoe():
    root = tk.Tk()
    root.withdraw() 

    player1, player2 = get_both_player_names()
    if not player1 or not player2:
        root.destroy()
        return

    game_window = tk.Toplevel()
    game_window.title("Tic-Tac-Toe")
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    game_window.configure(bg="#8daaac")

    current_player = ["X"]
    buttons = []

    def check_winner():
        for i in range(3):
            if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
                return True
            if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
                return True
        if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
            return True
        if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
            return True
        return False

    def is_draw():
        for row in buttons:
            for btn in row:
                if btn["text"] == "":
                    return False
        return True

    def clear_board():
        for row in buttons:
            for btn in row:
                btn["text"] = ""

    def game_over_dialog(message):
        dlg = tk.Toplevel(game_window)
        dlg.title("Game Over")
        center_window(dlg, 300, 150)
        dlg.grab_set()

        tk.Label(dlg, text=message, font=("Arial", 14)).pack(pady=20)

        btn_frame = tk.Frame(dlg)
        btn_frame.pack(pady=10)

        def on_restart():
            dlg.destroy()
            clear_board()
            current_player[0] = "X"

        def on_quit():
            dlg.destroy()
            game_window.destroy()
            root.destroy()

        tk.Button(btn_frame, text="Restart Game", command=on_restart, width=12, bg="#789ed6").pack(side="left", padx=10)
        tk.Button(btn_frame, text="Quit Game", command=on_quit, width=12, bg="#58a544").pack(side="left", padx=10)

    def on_click(row, col):
        if buttons[row][col]["text"] == "":
            buttons[row][col]["text"] = current_player[0]
            if check_winner():
                winner = player1 if current_player[0] == "X" else player2
                game_over_dialog(f"{winner} wins!")
            elif is_draw():
                game_over_dialog("It's a draw!")
            else:
                current_player[0] = "O" if current_player[0] == "X" else "X"

    board_frame = tk.Frame(game_window, bg="#d0f0c4")
    board_frame.pack(pady=50)

    for i in range(3):
        row = []
        for j in range(3):
            btn = tk.Button(board_frame, text="", width=15, height=6, font=("Arial", 24),
                            command=lambda r=i, c=j: on_click(r, c))
            btn.grid(row=i, column=j, padx=10, pady=10)
            row.append(btn)
        buttons.append(row)

    control_frame = tk.Frame(game_window)
    control_frame.pack(pady=20)

    tk.Button(control_frame, text="Restart Game", command=lambda: clear_board() or current_player.__setitem__(0, "X"),
              font=("Arial", 12), bg="#9bafbe", width=15).pack(side="left", padx=20)

    tk.Button(control_frame, text="Quit Game", command=lambda: (game_window.destroy(), root.destroy()),
              font=("Arial", 12), bg="#9be2a4", width=15).pack(side="left", padx=20)

    root.mainloop()
if __name__ == "__main__":
    start_tictactoe()
