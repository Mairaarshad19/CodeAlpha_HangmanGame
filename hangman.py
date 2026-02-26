import tkinter as tk
import random

# Word list
words = [
    "apple", "banana", "cherry", "date", "elderberry",
    "grapefruit", "kiwi", "mango", "nectarine", "orange",
    "papaya", "pineapple", "raspberry", "strawberry", "watermelon"
]

# Hangman drawing
def draw_hangman(canvas, wrong_guesses):
    canvas.delete("all")
    # Gallows
    canvas.create_line(20, 180, 120, 180, width=3)
    canvas.create_line(70, 180, 70, 20, width=3)
    canvas.create_line(70, 20, 150, 20, width=3)
    canvas.create_line(150, 20, 150, 40, width=3)

    # Stick figure parts
    if wrong_guesses >= 1: canvas.create_oval(135, 40, 165, 70, width=3)   # head
    if wrong_guesses >= 2: canvas.create_line(150, 70, 150, 120, width=3)  # body
    if wrong_guesses >= 3: canvas.create_line(150, 80, 120, 100, width=3)  # left arm
    if wrong_guesses >= 4: canvas.create_line(150, 80, 180, 100, width=3)  # right arm
    if wrong_guesses >= 5: canvas.create_line(150, 120, 130, 150, width=3) # left leg
    if wrong_guesses >= 6: canvas.create_line(150, 120, 170, 150, width=3) # right leg

# Main game class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Hangman Game 🎉")
        self.root.configure(bg="#87ceeb")  # sky blue background

        # Heading
        self.heading = tk.Label(root, text="🎉 Hangman Game 🎉", 
                                font=("Comic Sans MS", 32, "bold"), 
                                bg="#87ceeb", fg="#ff1493")
        self.heading.pack(pady=20)

        # Word display
        self.word_label = tk.Label(root, text="", font=("Poppins", 28), bg="#87ceeb", fg="#000080")
        self.word_label.pack(pady=20)

        # Message area
        self.message_label = tk.Label(root, text="", font=("Poppins", 18), bg="#87ceeb", fg="green")
        self.message_label.pack(pady=10)

        # Score display
        self.score_label = tk.Label(root, text="Score: 0", font=("Poppins", 18, "bold"), bg="#87ceeb", fg="#800080")
        self.score_label.pack(pady=10)

        # Canvas for hangman
        self.canvas = tk.Canvas(root, width=250, height=200, bg="#f0f8ff", highlightthickness=2, relief="ridge")
        self.canvas.pack(pady=10)

        # Alphabet buttons
        self.buttons_frame = tk.Frame(root, bg="#87ceeb")
        self.buttons_frame.pack(pady=20)

        # Replay button
        self.replay_button = tk.Button(root, text="🔄 Play Again", font=("Poppins", 16),
                                       command=self.start_game, bg="#32cd32", fg="white", state="disabled")
        self.replay_button.pack(pady=10)

        self.start_game()

    def start_game(self):
        self.fruit = random.choice(words)
        self.revealed = ["_"] * len(self.fruit)
        self.guessed = set()
        self.wrong_guesses = 0
        self.score = 0
        self.update_word_display()
        self.update_score()
        self.message_label.config(text="Guess a letter! 🎯", fg="blue")
        draw_hangman(self.canvas, self.wrong_guesses)

        # Enable replay button only after game ends
        self.replay_button.config(state="disabled")

        # Clear old buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Create alphabet buttons
        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, font=("Comic Sans MS", 14, "bold"),
                            command=lambda l=letter.lower(): self.guess_letter(l),
                            bg="#ffdab9", fg="black", relief="raised")
            btn.grid(row=i // 9, column=i % 9, padx=3, pady=3)
            self.letter_buttons[letter.lower()] = btn

    def update_word_display(self):
        self.word_label.config(text=" ".join(self.revealed))

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def disable_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")
        self.replay_button.config(state="normal")

    def guess_letter(self, letter):
        if letter in self.guessed:
            self.message_label.config(text=f"⚠️ Already guessed '{letter}'!", fg="orange")
            return

        self.guessed.add(letter)

        if letter in self.fruit:
            for i, l in enumerate(self.fruit):
                if l == letter:
                    self.revealed[i] = letter
            self.update_word_display()
            self.score += 10
            self.update_score()
            self.message_label.config(text=f"✅ Great! '{letter}' is in the word.", fg="green")

            if self.revealed == list(self.fruit):
                self.score += 50
                self.update_score()
                self.message_label.config(text=f"🎉 You win! The word was '{self.fruit}'!", fg="purple")
                self.disable_buttons()
        else:
            self.wrong_guesses += 1
            self.score -= 5
            self.update_score()
            draw_hangman(self.canvas, self.wrong_guesses)
            self.message_label.config(text=f"❌ Oops! '{letter}' is not in the word.", fg="red")

            if self.wrong_guesses >= 6:
                self.message_label.config(text=f"💀 Game Over! The word was '{self.fruit}'.", fg="red")
                self.update_word_display()
                self.disable_buttons()

# Run the game
root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
