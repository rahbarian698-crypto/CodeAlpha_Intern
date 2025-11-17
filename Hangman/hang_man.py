from models import CLASSIC_HANGMAN, EMOJI_HANGMAN, STICKMAN_HANGMAN
import random

def choose_theme():
    print("\nChoose your Hangman theme:")
    print("1. Classic ASCII")
    print("2. Emoji Hangman")
    print("3. Stickman Minimal")
    choice = input("Enter 1-3: ")
    if choice == "1":
        return CLASSIC_HANGMAN
    elif choice == "2":
        return EMOJI_HANGMAN
    elif choice == "3":
        return STICKMAN_HANGMAN
    else:
        print("Invalid choice, defaulting to Classic ASCII.")
        return CLASSIC_HANGMAN

def load_words():
    try:
        with open("words.txt", "r") as file:
            words = [line.strip() for line in file if line.strip()]
            if words:
                return words
    except FileNotFoundError:
        pass
    return ["python", "keyboard", "program", "laptop", "science", "coffee",
            "sunshine", "adventure", "dragon", "mountain", "river", "ocean",
            "forest", "castle", "wizard", "pirate", "galaxy", "planet", "rocket"]

def reveal_letters(word, num_letters=2):
    display = ["_"] * len(word)
    indices = random.sample(range(len(word)), min(num_letters, len(word)))
    for i in indices:
        display[i] = word[i]
    return display

def play_hangman():
    hangman_model = choose_theme()
    words = load_words()
    word = random.choice(words).lower()

    num_to_reveal = random.choice([1, 2])
    display = reveal_letters(word, num_letters=num_to_reveal)
    guessed_letters = [letter for letter in display if letter != "_"]

    wrong_attempts = 0
    max_attempts = len(hangman_model) - 1

    print("\nWelcome to Hangman!\n")

    while wrong_attempts < max_attempts:
        print(hangman_model[wrong_attempts])
        print("Word: ", " ".join(display))
        print("Guessed letters:", ", ".join(guessed_letters))
        guess = input("Enter a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter!\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue

        guessed_letters.append(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    display[i] = guess
            print("Good guess!\n")
        else:
            wrong_attempts += 1
            print("Wrong guess!\n")

        if "_" not in display:
            print("  _______")
            print(" |       |")
            print(" |       🙂")  # Happy face
            print(" |      \\|/")
            print(" |       |")
            print(" |      / \\")
            print("_|_")
            print("\nCongratulations! You guessed the word! 🎉")

            break

    if wrong_attempts == max_attempts:
        print(hangman_model[wrong_attempts])
        print("\nGame Over! The word was:", word)

if __name__ == "__main__":
    play_hangman()
