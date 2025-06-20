import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_DURATION = 25 *60
SHORT_BREAK_DURATION = 5 * 60
LONG_BREAK_DURATION = 30 * 60


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("250x200")
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)

        self.style = Style(theme="simplex")

        self.timer_display = ttk.Label(self.root, text="25:00", font=("TkDefaultFont", 40))
        self.timer_display.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.reset_timer()

        self.root.mainloop()

    def reset_timer(self):
        self.work_time = WORK_DURATION
        self.break_time = SHORT_BREAK_DURATION
        self.is_work_time = True
        self.completed_pomodoros = 0
        self.is_timer_running = False
        self.update_timer_display()

    def start_timer(self):
        if not self.is_timer_running:
            self.is_timer_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.countdown()

    def stop_timer(self):
        self.is_timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def countdown(self):
        if self.is_timer_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time <= 0:
                    self.completed_pomodoros += 1
                    self.is_work_time = False
                    if self.completed_pomodoros % 4 == 0:
                        self.break_time = LONG_BREAK_DURATION
                        messagebox.showinfo("Pomodoro Complete", "Time for a long break")
                    else:
                        self.break_time = SHORT_BREAK_DURATION
                        messagebox.showinfo("Pomodoro Complete", "Time for a short break")
            else:
                self.break_time -= 1
                if self.break_time <= 0:
                    self.is_work_time = True
                    self.work_time = WORK_DURATION
                    messagebox.showinfo("Break Over", "Time for some work")

            self.update_timer_display()
            self.root.after(1000, self.countdown)

    def update_timer_display(self):
        time_left = self.work_time if self.is_work_time else self.break_time
        minutes, seconds = divmod(time_left, 60)
        self.timer_display.config(text=f"{minutes:02d}:{seconds:02d}")


if __name__ == "__main__":
    PomodoroTimer()
