import tkinter as tk
import random

words_with_hints = {
    "python": "A powerful programming language (and a snake)",
    "robot": "An automated mechanical machine",
    "coding": "Typing logic into a computer",
    "screen": "What you're looking at right now",
    "keyboard": "You type on it daily",
    "function": "Reusable part of a program",
    "debugging": "Fixing issues in code",
    "internet": "The global network",
    "compiler": "Code translator for computers",
    "database": "Where organized digital data lives"
}

score = 0 

def start_word_scramble():
    global score

    original_word, hint = random.choice(list(words_with_hints.items()))
    scrambled_word = original_word
    while scrambled_word == original_word:
        scrambled_word = ''.join(random.sample(original_word, len(original_word)))

    window = tk.Toplevel()
    window.title("Word Scramble Game")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.configure(bg="#f0f4f7")

    # Score display
    score_label = tk.Label(window, text=f"Score: {score}", font=("Arial", 20, "bold"), fg="#007f5f", bg="#f0f4f7")
    score_label.pack(pady=20)

  
    tk.Label(window, text="🧠 Word Scramble Challenge 🧩", font=("Arial", 28, "bold"), fg="#2b2d42", bg="#f0f4f7").pack()

    tk.Label(window, text="Drag the letters to form the correct word.", font=("Arial", 16, "italic"), fg="#555555", bg="#f0f4f7").pack(pady=10)

    hint_label = tk.Label(window, text=f"Hint: {hint}", font=("Arial", 18), fg="#1d3557", bg="#f0f4f7")
    hint_label.pack(pady=20)

    frame_width = len(original_word) * 80
    letter_frame = tk.Frame(window, width=frame_width, height=100, bg="#f0f4f7")
    letter_frame.pack(pady=40)
    letter_frame.pack_propagate(False)

    letters = []

    def update_word_order():
        return ''.join(label.cget("text").lower() for label in sorted(letters, key=lambda x: x.winfo_x()))

    def check_word():
        current_word = update_word_order()
        if current_word == original_word:
            def show_custom_popup():
                popup = tk.Toplevel(window)
                popup.title("Well Done!")
                popup_width = 400
                popup_height = 250
                
                screen_width = popup.winfo_screenwidth()
                screen_height = popup.winfo_screenheight()
                x = (screen_width // 2) - (popup_width // 2)
                y = (screen_height // 2) - (popup_height // 2)
                popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
                
                popup.configure(bg="#e0f7fa")
                popup.transient(window)
                popup.grab_set()

                tk.Label(popup, text="🎉 Correct! 🎉", font=("Arial", 24, "bold"),
                         bg="#e0f7fa", fg="#007f5f").pack(pady=20)
                tk.Label(popup, text=f"The word was: {original_word.upper()}",
                         font=("Arial", 18), bg="#e0f7fa", fg="#023047").pack()

                def close_popup():
                    popup.destroy()
                    window.destroy()
                    start_word_scramble()

                def quit_game():
                    popup.destroy()
                    window.destroy()

                button_frame = tk.Frame(popup, bg="#e0f7fa")
                button_frame.pack(pady=30)

                tk.Button(button_frame, text="Next Word ➡️", font=("Arial", 14), bg="#00b4d8", fg="white",
                          padx=15, pady=5, command=close_popup).pack(side="left", padx=10)

                tk.Button(button_frame, text="Quit Game ❌", font=("Arial", 14), bg="#d62828", fg="white",
                          padx=15, pady=5, command=quit_game).pack(side="left", padx=10)

            global score
            score += 1
            score_label.config(text=f"Score: {score}")
            show_custom_popup()
        else:
            
            def show_game_over_popup():
                popup = tk.Toplevel(window)
                popup.title("Game Over")
                popup_width = 400
                popup_height = 250
                
                screen_width = popup.winfo_screenwidth()
                screen_height = popup.winfo_screenheight()
                x = (screen_width // 2) - (popup_width // 2)
                y = (screen_height // 2) - (popup_height // 2)
                popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

                popup.configure(bg="#3e88a8")
                popup.transient(window)
                popup.grab_set()

                tk.Label(popup, text="❌ Game Over ❌", font=("Arial", 24, "bold"),
                         bg="#3e88a8", fg="#fbfcf9").pack(pady=20)
                tk.Label(popup, text=f"Your final score was: {score}",
                         font=("Arial", 18), bg="#3e88a8", fg="#f8f3f3").pack()

                def close_game():
                    popup.destroy()
                    window.destroy()

                def try_again():
                    popup.destroy()
                    window.destroy()
                    global score
                    score = 0
                    start_word_scramble()

                button_frame = tk.Frame(popup, bg="#3e88a8")
                button_frame.pack(pady=30)

                tk.Button(button_frame, text="Try Again 🔄", font=("Arial", 14), bg="#1f7540", fg="white",
                          padx=15, pady=5, command=try_again).pack(side="left", padx=10)

                tk.Button(button_frame, text="Close ❌", font=("Arial", 14), bg="#1f7540", fg="white",
                          padx=15, pady=5, command=close_game).pack(side="left", padx=10)

            show_game_over_popup()

    def start_drag(event):
        widget = event.widget
        widget.startX = event.x
        widget.lift()

    def on_drag(event):
        widget = event.widget
        dx = event.x - widget.startX
        widget.place(x=widget.winfo_x() + dx)

    def stop_drag(event):
        sorted_positions = sorted(letters, key=lambda lbl: lbl.winfo_x())
        for i, lbl in enumerate(sorted_positions):
            lbl.place(x=i * 70, y=0)
        letters[:] = sorted_positions

    for i, char in enumerate(scrambled_word):
        color = "#4cc9f0" if i % 2 == 0 else "#80ed99"
        lbl = tk.Label(letter_frame, text=char.upper(), font=("Arial", 30, "bold"),
                       width=3, height=1, bg=color, fg="#1d1d1d", relief="raised", bd=3)
        lbl.place(x=i * 70, y=0)
        lbl.bind("<Button-1>", start_drag)
        lbl.bind("<B1-Motion>", on_drag)
        lbl.bind("<ButtonRelease-1>", stop_drag)
        letters.append(lbl)

    tk.Button(window, text="Check Answer ✅", font=("Arial", 18, "bold"), bg="#00b4d8", fg="white",
              padx=20, pady=5, command=check_word).pack(pady=20)

    result_label = tk.Label(window, text="", font=("Arial", 16), fg="red", bg="#f0f4f7")
    result_label.pack()

    window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    start_word_scramble()
