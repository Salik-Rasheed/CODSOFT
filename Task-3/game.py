import random
import time
import os

# ---------------- CLEAR SCREEN ----------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------------- COMPUTER ----------------
def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

# ---------------- WINNER ----------------
def determine_winner(player, computer):
    if player == computer:
        return 'tie'
    beats = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    return 'win' if beats[player] == computer else 'lose'

# ---------------- ANIMATION ----------------
def countdown():
    for i in ["Rock...", "Paper...", "Scissors..."]:
        print(i)
        time.sleep(0.5)

# ---------------- RESULT MESSAGE ----------------
def get_result_message(player, result):
    details = {
        'rock':     {'win': 'Rock smashes Scissors!', 'lose': 'Paper covers Rock!',     'tie': 'Both chose Rock!'},
        'paper':    {'win': 'Paper covers Rock!',      'lose': 'Scissors cut Paper!',    'tie': 'Both chose Paper!'},
        'scissors': {'win': 'Scissors cut Paper!',     'lose': 'Rock smashes Scissors!', 'tie': 'Both chose Scissors!'},
    }
    return details[player][result]

# ---------------- CELEBRATION ----------------
def celebrate():
    for _ in range(3):
        print("🎉✨ YOU WIN! ✨🎉")
        time.sleep(0.3)
        clear()
        print("✨🎉 YOU WIN! 🎉✨")
        time.sleep(0.3)
        clear()

# ---------------- SCORE BOARD ----------------
def show_scores(player_score, cpu_score, rounds):
    print("\n" + "="*40)
    print(f" ROUND: {rounds}")
    print(f" YOU: {player_score}   |   CPU: {cpu_score}")
    print("="*40)

# ---------------- FINAL ----------------
def show_final_scores(player_score, cpu_score, rounds):
    print("\n" + "="*40)
    print(" FINAL RESULT ")
    print(f" You: {player_score}  |  CPU: {cpu_score}  |  Rounds: {rounds}")

    if player_score > cpu_score:
        print(" 🏆 YOU ARE THE CHAMPION!")
    elif cpu_score > player_score:
        print(" 🤖 CPU DOMINATES!")
    else:
        print(" 🤝 IT'S A DRAW!")

    print("="*40)
    print(" Thanks for playing!\n")

# ---------------- MAIN GAME ----------------
def play_game():
    player_score = 0
    cpu_score = 0
    rounds = 0

    options = {'1': 'rock', '2': 'paper', '3': 'scissors'}

    while True:
        clear()
        print("="*40)
        print("   ROCK PAPER SCISSORS GAME 🎮")
        print("="*40)
        print("1. Rock 🪨")
        print("2. Paper 📄")
        print("3. Scissors ✂️")
        print("4. Quit ❌")

        choice = input("\nEnter choice: ").strip()

        if choice == '4':
            clear()
            show_final_scores(player_score, cpu_score, rounds)
            break

        if choice not in options:
            print("Invalid choice!")
            time.sleep(1)
            continue

        player = options[choice]
        computer = get_computer_choice()

        clear()
        countdown()

        print(f"\nYou: {player.upper()}  |  CPU: {computer.upper()}")

        result = determine_winner(player, computer)
        rounds += 1

        if result == 'win':
            player_score += 1
            print("\n🔥 YOU WIN THIS ROUND!")
            celebrate()

        elif result == 'lose':
            cpu_score += 1
            print("\n💀 YOU LOST THIS ROUND!")

        else:
            print("\n🤝 IT'S A TIE!")

        print(get_result_message(player, result))

        show_scores(player_score, cpu_score, rounds)

        input("\nPress Enter to continue...")

# ---------------- RUN ----------------
if __name__ == "__main__":
    play_game()
