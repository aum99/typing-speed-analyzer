from tkinter import *
import random
import math

MAIN = "#588157"
BOX = "#a3b18a"
FLAG = 0
score = 0


with open('../typing-speed-analyzer/words.txt') as word_file:
    words = word_file.read()
    list_words = words.split(',')


random_words = random.choices(list_words, k=80)
select_words = ' '.join(random_words)


class TypeSpeed:

    def __init__(self):

        self.window = Tk()
        self.window.config(padx=40, pady=40, bg=MAIN)
        self.window.title("Typing Speed Analyzer")

        self.canvas = Canvas(bd=0, highlightthickness=0, height=60, width=1150, bg=MAIN)
        self.timer_text = self.canvas.create_text(1000, 15, text="00:00", fill="white", font=("Verdana", 25, "bold"))
        self.name = self.canvas.create_text(290, 15, text="Type for speed..", fill="white",
                                              font=("Verdana", 25, "bold"))
        keyboard_img = PhotoImage(file="../typing-speed-analyzer/keyboard.png")
        self.keyboard_image = self.canvas.create_image(100, 15,image=keyboard_img)
        self.canvas.grid(row=0, column=0)

        self.text = Text(self.window, {"bg": BOX, "bd": 50, "fg": "#000000", "height": 6, "font": ("Verdana", 20),
                             "insertbackground": "#FF2E63", "wrap": "word", "highlightthickness": 0})
        self.text.insert(INSERT,
                    select_words + "\n\n------------------------------------PLEASE TYPE IN THE BOX BELOW------------------------------------")
        self.text.mark_set("insert", "%d.%d" % (1.0, 0.0))
        self.text.grid(row=1, column=0)
        self.text.config(pady=5, state='disabled')

        self.typing_box = Text(height=5, bg="#3a5a40", bd=50, fg="#000000", font=("Verdana", 20), highlightthickness=0)
        self.typing_box.focus()
        self.typing_box.grid(row=2, column=0)

        self.button = Button(text="RESET", command=self.reset, height=2, width=5, bg=MAIN, highlightthickness=0)
        self.button.grid(row=3, column=0, pady=10)

        self.window.bind("<Key>", lambda event: self.start())

        self.window.mainloop()

    def get_text(self):
        user_input = self.typing_box.get(1.0, "end-1c")
        user_words = list(user_input.split(" "))
        global score
        score = 0
        for i in range(0, len(user_words)):
            if user_words[i] == random_words[i]:
                score += 1

    def start_timer(self):
        self.typing_box.config(state='normal')
        self.timer_start(60)

    def timer_start(self, COUNT):
        count_min = math.floor(COUNT / 60)
        count_sec = COUNT % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count_min < 10:
            count_min = f"0{count_min}"

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if COUNT > 0:
            global timer
            timer = self.window.after(1000, self.timer_start, COUNT - 1)
        else:
            self.get_text()
            score = self.print_score()
            self.typing_box.delete("1.0", "end")
            self.canvas.itemconfig(self.timer_text, text=f"Score: {score}wpm")
            self.typing_box.config(state='normal')
            self.typing_box.focus()

    def start(self):
        global FLAG
        if FLAG == 0:
            FLAG += 1
            self.start_timer()

    def print_score(self):
        global score
        return score

    def reset(self):
        global FLAG
        FLAG = 0
        self.window.after_cancel(timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.typing_box.delete("1.0", "end")



game = TypeSpeed()


