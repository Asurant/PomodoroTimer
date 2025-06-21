import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_DURATION = 25 * 60
SHORT_BREAK_DURATION = 5 * 60
LONG_BREAK_DURATION = 30 * 60


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("225x120")
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.style = Style(theme="simplex")

        self.opacity_level = 1.0


        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.timer_display = ttk.Label(main_frame, text="25:00", font=("TkDefaultFont", 20))
        self.timer_display.grid(row=0, column=0, rowspan=3, sticky="w", padx=(0, 20))

        self.start_button = ttk.Button(main_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=1, sticky="ew")

        self.stop_button = ttk.Button(main_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, sticky="ew")

        self.opacity_button = ttk.Button(main_frame, text="Opacity: 100%", command=self.change_opacity)
        self.opacity_button.grid(row=2, column=1, sticky="ew")

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

    def change_opacity(self):
        self.opacity_level -= 0.25
        if self.opacity_level <= 0:
            self.opacity_level = 1.0

        opacity_percent = int(self.opacity_level * 100)
        self.root.attributes("-alpha", self.opacity_level)
        self.opacity_button.config(text=f"Opacity: {opacity_percent}%")

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
