import tkinter as tk
from tkinter import ttk
from vocabulary_quiz_app.quiz_logic import draw_word, check_answer

class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list) -> None:
        self.root = root
        self.words = words
        self.current = None
        self.checked = False
        self.score = 0
        self.total = 0
        self.wrong_count = 0  # 3번 틀리면 탈락시키기 위한 변수

        self.root.title("Vocabulary Quiz App")
        self.root.geometry("400x300")

        self.word_var = tk.StringVar()
        self.feedback_var = tk.StringVar()
        self.score_var = tk.StringVar(value="Score: 0/0 (정답률: 0.0%)")

        ttk.Label(root, textvariable=self.word_var, font=("Helvetica", 24)).pack(pady=20)
        self.answer_entry = ttk.Entry(root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", lambda event: self.check_current())

        buttons = ttk.Frame(root)
        buttons.pack(pady=10)
        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(side=tk.LEFT, padx=6)

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self) -> None:
        self.current = draw_word(self.words, self.root.nametowidget(".").children.get("rng"))
        if not self.current:
            import random
            self.current = random.choice(self.words) if self.words else None
        
        if self.current:
            self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()

    def check_current(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1  # 판수 카운트 정상 증가
        user_input = self.answer_entry.get().strip()

        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")
            self.wrong_count += 1

        if self.total > 0:
            rate = (self.score / self.total) * 100
            self.score_var.set(f"Score: {self.score}/{self.total} (정답률: {rate:.1f}%)")

        if self.wrong_count >= 3:
            self.check_button.config(state="disabled")
            self.answer_entry.config(state="disabled")
            self.feedback_var.set("🚨 3회 실패! 게임이 종료됩니다.")
            return

        self.check_button.state(["disabled"])
