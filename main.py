from tkinter import *
import random
import string


HEIGHT = 1080
WIDTH = 1920

NOT_LETTER = 0
WRONG_LETTER = 1
ALREADY_GUESSED_LETTER = 2
GUESSED_LETTER = 3


def random_line():
    lines = open('words.txt').read().splitlines()
    myline = random.choice(lines)
    return myline


class Hangman:
    def __init__(self):
        self.win = Tk()
        self.win.title("Hangman")
        self.canvas = Canvas(self.win, height=HEIGHT, width=WIDTH, background="white")
        self.canvas.pack()
        Label(self.win, text="Welcome to the Hangman!", bg="white", fg="black",
              font="none 12 bold").place(x=30, y=5)
        word = Label(self.win, text="Computer will randomly select a word from english dictionary.",
                     bg="white", fg="black", font="none 12 bold")
        word.place(x=30, y=40)
        self.word = ""
        self.letter_count = dict.fromkeys(string.ascii_lowercase, 0)
        self.guessed_letters = []
        self.winning_letters = []
        self.state = 0
        self.winner = 0
        self.entry_text = None
        self.setup()
        self.last_label = None

    def setup(self):
        w = random_line().strip()
        self.word = w
        self.winning_letters = list(set(self.word))
        self.winning_letters.sort()
        letters = len(self.word)
        grid = Label(self.win, text="_ " * letters, bg="white", fg="black", font="none 20 bold")
        grid.place(x=30, y=60)
        self.draw_hangman()
        self.win.update_idletasks()
        self.win.update()


    def play_round(self):

        var = IntVar()
        self.entry_text = Entry(self.win)
        self.canvas.create_window(200, 160, window=self.entry_text)
        button = Button(text="Enter letter", command=lambda: var.set(1))
        self.canvas.create_window(200, 200, window=button)
        button.wait_variable(var)
        if self.last_label:
            self.last_label.destroy()
        self.win.update_idletasks()
        self.win.update()
        x = self.get_letter()
        check = self.check_letter(x)
        if check == NOT_LETTER:
            self.last_label = Label(self.win,
                                    text="Written letter is either not alphabetical letter or is longer or shorter "
                                         "than 1",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(430, 120, window=self.last_label)
        elif check == WRONG_LETTER:
            self.last_label = Label(self.win,
                                    text="You guessed wrong letter. You have " + str(6 - self.state) + " live(s) left.",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(280, 120, window=self.last_label)
            self.state += 1
        elif check == ALREADY_GUESSED_LETTER:
            self.last_label = Label(self.win,
                                    text="You guessed already guessed letter. Try again.",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(260, 120, window=self.last_label)
        else:
            self.last_label = Label(self.win,
                                    text="You guessed correct letter. Great job.",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(220, 120, window=self.last_label)
            self.guessed_letters.append(x)
            self.guessed_letters.sort()
            self.draw_letter(x)
        self.draw_hangman()
        if self.guessed_letters == self.winning_letters:
            self.winner = 1

    def get_letter(self):
        return self.entry_text.get()

    def check_letter(self, letter):
        if not letter.isalpha() or len(letter) != 1:
            return NOT_LETTER
        if letter not in self.winning_letters:
            return WRONG_LETTER
        if letter in self.winning_letters:
            if letter in self.guessed_letters:
                return ALREADY_GUESSED_LETTER
            else:
                return GUESSED_LETTER

    def play(self):
        while self.winner == 0:
            if self.state != 7:
                self.play_round()
            else:
                self.winner = 2
        if self.winner == 1:
            self.last_label = Label(self.win,
                                    text="Congrats, you won the game!",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(500, 300, window=self.last_label)
        else:
            self.last_label = Label(self.win,
                                    text="You died!",
                                    bg="white", fg="black", font="none 12 bold")
            self.canvas.create_window(500, 300, window=self.last_label)




    def draw_hangman(self):
        self.canvas.create_line(800, 790, 850, 790)
        self.canvas.create_line(830, 790, 830, 450)
        self.canvas.create_line(830, 450, 1000, 450)
        radius = 30
        if self.state >= 1:  # Draw sting to neck
            self.canvas.create_line(1000, 450, 1000, 470, tags="hang")
        if self.state >= 2:  # Draw face
            self.canvas.create_oval(1000 - radius, 500 - radius,
                                    1000 + radius, 500 + radius, tags="hang")
        if self.state >= 3:  # Draw body
            self.canvas.create_line(1000, 530, 1000, 650, tags="hang")
        if self.state >= 4:  # Draw first arm
            self.canvas.create_line(1000, 550, 940, 620, tags="hang")
        if self.state >= 5:  # Draw second arm
            self.canvas.create_line(1000, 550, 1060, 620, tags="hang")
        if self.state >= 6:  # Draw one leg
            self.canvas.create_line(1000, 650, 940, 720, tags="hang")
        if self.state >= 7:  # Draw second leg
            self.canvas.create_line(1000, 650, 1060, 720, tags="hang")
        self.canvas.pack()

    def draw_letter(self, letter):
        labels = []
        counter = 0
        for i in range(len(self.word)):
            if self.word[i] == letter:
                labels.append(Label(self.win, text=letter, bg="white", fg="black", font="none 20 bold"))
                labels[counter].place(x=30 + i * 32, y=60)
                counter += 1
                self.win.update_idletasks()
                self.win.update()


def main():
    h = Hangman()
    h.play()
    h.win.mainloop()


if __name__ == '__main__':
    main()
