import random
import pandas as pd
from tkinter import Tk, simpledialog, messagebox, Button, Entry, Label, Text, END
import sys
import os

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

smallwordlist_path = os.path.join(base_path, 'rsc', 'smallwordlist.csv')
wordlist_path = os.path.join(base_path, 'rsc', 'wordlist.csv')

SMALLCORPS = pd.read_csv(smallwordlist_path)
CORPS = pd.read_csv(wordlist_path)


# Initialize wordlist
def choose_word(n):
    words = SMALLCORPS['word' + f'{n}'].dropna().tolist()
    vocab = CORPS['word' + f'{n}'].dropna().tolist()
    return random.choice(words), vocab


def check_guess(guess, answer):
    exact_matches = 0
    wrong_place = 0
    answer_letters = list(answer)
    guessed_letters = list(guess)

    for i in range(len(answer)):
        if guessed_letters[i] == answer_letters[i]:
            exact_matches += 1
            guessed_letters[i] = None
            answer_letters[i] = None

    for i in range(len(answer)):
        if guessed_letters[i] and guessed_letters[i] in answer_letters:
            wrong_place += 1
            answer_letters[answer_letters.index(guessed_letters[i])] = None

    wrong_letters = len(answer) - exact_matches - wrong_place
    return exact_matches, wrong_place, wrong_letters


def play_wordle():
    def give_up():
        messagebox.showinfo("Answer", f"You gave up. The correct answer is: {answer}")
        root.destroy()

    def submit_guess():
        guess = guess_entry.get()
        if guess in vocab:
            guess_entry.delete(0, END)
            if guess == answer:
                messagebox.showinfo("Congratulations", f"Congratulations! You guessed it right! The answer is: {answer}")
                root.destroy()
            else:
                exact_matches, wrong_place, wrong_letters = check_guess(guess, answer)
                guesses.append(guess)
                feedbacks.append((exact_matches, wrong_place, wrong_letters))
                update_history()
                messagebox.showinfo("Result", f"Exact matches: {exact_matches}, Wrong place: {wrong_place}, Wrong letters: {wrong_letters}, Remaining attempts: {attempts[0]-1}")
                attempts[0] -= 1
                if attempts[0] == 0:
                    messagebox.showinfo("Failed", f"Unfortunately, you didn't guess it. The correct answer is: {answer}")
                    root.destroy()
        else:
            messagebox.showerror("Error", "The guessed word is not in the vocabulary or the length is incorrect. Please re-enter.")

    def update_history():
        history_text.delete(1.0, END)
        for i, (guess, feedback) in enumerate(zip(guesses, feedbacks)):
            exact_matches, wrong_place, wrong_letters = feedback
            line = f"{guess} - {'O' * exact_matches}{'V' * wrong_place}{'X' * wrong_letters}"
            history_text.insert(END, line + ("\t    \t" if i % 2 == 0 else "\n"))

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.update_idletasks()

    root = Tk()
    root.withdraw()
    center_window(root)

    root.update()
    wl = int(simpledialog.askstring("Input", "Word length:", parent=root))
    center_window(root)
    answer, vocab = choose_word(wl)
    attempts = int(simpledialog.askstring("Input", "Allowed number of guesses (5-15):", parent=root))
    center_window(root)
    if attempts < 5:
        attempts = 5
    elif attempts > 15:
        attempts = 15
    attempts = [attempts]
    messagebox.showinfo("Welcome", f"Welcome to the Wordle game! You have {attempts[0]} attempts to guess a word.")

    root.deiconify()
    root.title("Worduel Game")

    guesses = []
    feedbacks = []

    root.geometry("")

    Label(root, text=f"Enter your guess (word length is {wl}):").grid(row=0, column=0, columnspan=2, pady=10)
    guess_entry = Entry(root)
    guess_entry.grid(row=1, column=0, columnspan=2, pady=10)

    submit_button = Button(root, text="Submit", command=submit_guess)
    submit_button.grid(row=2, column=0, padx=10, pady=10)

    give_up_button = Button(root, text="Give Up", command=give_up)
    give_up_button.grid(row=2, column=1, padx=10, pady=10)

    history_label = Label(root, text="Guess History:")
    history_label.grid(row=3, column=0, columnspan=2, pady=10)

    history_text = Text(root, height=10, width=50)
    history_text.grid(row=4, column=0, columnspan=2, pady=10)

    root.update_idletasks()
    center_window(root)
    root.mainloop()


# Start the game
play_wordle()
