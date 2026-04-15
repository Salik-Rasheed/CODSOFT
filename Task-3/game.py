import tkinter as tk
import random

# ---------------- DATA ----------------
player_score = 0
cpu_score = 0
rounds = 0
max_rounds = 3

choices_emoji = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}

# ---------------- LOGIC ----------------
def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(player, computer):
    if player == computer:
        return 'tie'
    beats = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    return 'win' if beats[player] == computer else 'lose'

# ---------------- FRAME SWITCH ----------------
def show_frame(frame):
    frame.tkraise()

# ---------------- START GAME ----------------
def start_game(mode):
    global player_score, cpu_score, rounds, max_rounds
    player_score = 0
    cpu_score = 0
    rounds = 0
    max_rounds = mode
    update_score()
    result_label.config(text="")
    detail_label.config(text="")
    show_frame(game_frame)

# ---------------- SCORE ----------------
def update_score():
    score_label.config(
        text=f"You: {player_score} | CPU: {cpu_score} | Round: {rounds}/{max_rounds if max_rounds else '∞'}"
    )

# ---------------- ADVANCED CELEBRATION ----------------
def celebrate():
    colors = ["#010101", "#222222", "#444444", "#222222"]
    texts = ["🎉 YOU WIN 🎉", "✨ AWESOME ✨", "🏆 VICTORY 🏆", "🔥 GREAT 🔥"]

    def animate(i=0):
        if i < 12:
            root.config(bg=colors[i % len(colors)])
            result_label.config(text=texts[i % len(texts)])

            confetti = tk.Label(root,
                                text="🎉✨🎊",
                                bg=root["bg"],
                                fg="white",
                                font=("Arial", 16))
            confetti.place(x=random.randint(50, 250),
                           y=random.randint(100, 400))

            root.after(100, lambda: confetti.destroy())
            root.after(100, lambda: animate(i + 1))
        else:
            root.config(bg="#010101")
            result_label.config(text="YOU WIN 🎉")

    animate()

# ---------------- RESULT SCREEN ----------------
def show_winner():
    if player_score > cpu_score:
        final_label.config(text="🏆 YOU WON THE GAME!")
    elif cpu_score > player_score:
        final_label.config(text="💀 CPU WON!")
    else:
        final_label.config(text="🤝 DRAW!")

    show_frame(result_frame)

# ---------------- PLAY ----------------
def play(player):
    result_label.config(text="CPU thinking...")
    root.after(500, lambda: finish_round(player))

def finish_round(player):
    global player_score, cpu_score, rounds

    computer = get_computer_choice()
    result = determine_winner(player, computer)
    rounds += 1

    if result == "win":
        player_score += 1
        celebrate()
    elif result == "lose":
        cpu_score += 1
        result_label.config(text="YOU LOSE 💀")
    else:
        result_label.config(text="TIE 🤝")

    detail_label.config(
        text=f"{choices_emoji[player]}  vs  {choices_emoji[computer]}"
    )

    update_score()

    if max_rounds and rounds >= max_rounds:
        root.after(1000, show_winner)

# ---------------- RESET ----------------
def reset_game():
    show_frame(start_frame)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("RPS Game")
root.geometry("320x500")
root.configure(bg="#010101")

# ---------------- FRAMES ----------------
start_frame = tk.Frame(root, bg="#010101")
game_frame = tk.Frame(root, bg="#010101")
result_frame = tk.Frame(root, bg="#010101")

for f in (start_frame, game_frame, result_frame):
    f.place(relwidth=1, relheight=1)

# ---------------- START SCREEN ----------------
tk.Label(start_frame, text="ROCK PAPER SCISSORS 🎮",
         font=("Arial", 14, "bold"),
         bg="#010101", fg="white").pack(pady=30)

tk.Button(start_frame, text="Best of 3",
          command=lambda: start_game(3),
          bg="#000", fg="white", width=20).pack(pady=10)

tk.Button(start_frame, text="Best of 5",
          command=lambda: start_game(5),
          bg="#000", fg="white", width=20).pack(pady=10)

tk.Button(start_frame, text="Endless Mode",
          command=lambda: start_game(0),
          bg="#000", fg="white", width=20).pack(pady=10)

# ---------------- GAME SCREEN ----------------
score_label = tk.Label(game_frame, text="",
                       bg="#010101", fg="white")
score_label.pack(pady=10)

result_label = tk.Label(game_frame, text="",
                        font=("Arial", 14, "bold"),
                        bg="#010101", fg="white")
result_label.pack(pady=10)

detail_label = tk.Label(game_frame, text="",
                        font=("Arial", 20),
                        bg="#010101", fg="white")
detail_label.pack(pady=10)

btn_frame = tk.Frame(game_frame, bg="#010101")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="🪨",
          command=lambda: play("rock"),
          width=5, height=2,
          bg="#000", fg="white").grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="📄",
          command=lambda: play("paper"),
          width=5, height=2,
          bg="#000", fg="white").grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="✂️",
          command=lambda: play("scissors"),
          width=5, height=2,
          bg="#000", fg="white").grid(row=0, column=2, padx=10)

tk.Button(game_frame, text="Back",
          command=reset_game,
          bg="#000", fg="white").pack(pady=10)

# ---------------- RESULT SCREEN ----------------
final_label = tk.Label(result_frame, text="",
                       font=("Arial", 18, "bold"),
                       bg="#010101", fg="white")
final_label.pack(pady=50)

tk.Button(result_frame, text="Play Again",
          command=reset_game,
          bg="#000", fg="white").pack(pady=10)

# ---------------- START ----------------
show_frame(start_frame)

root.mainloop()
