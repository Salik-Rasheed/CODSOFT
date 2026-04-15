import random
import string

def generate_password(length):
    if length < 4:
        return "Password length should be at least 4"

    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Ensure strong password (at least one from each category)
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_chars = letters + digits + symbols

    # Fill remaining length
    password += random.choices(all_chars, k=length - 3)

    # Shuffle for randomness
    random.shuffle(password)

    return "".join(password)

# Main program
try:
    length = int(input("Enter password length: "))
    print("Generated Password:", generate_password(length))
except:
    print("Invalid input! Please enter a number.")
