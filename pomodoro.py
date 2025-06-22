import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_DURATION = 25 * 60
SHORT_BREAK_DURATION = 5 * 60
LONG_BREAK_DURATION = 30 * 60


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("275x85")
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.style = Style(theme="simplex")

        self.opacity_level = 1.0
        self.work_duration = WORK_DURATION
        self.short_break_duration = SHORT_BREAK_DURATION
        self.long_break_duration = LONG_BREAK_DURATION

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.timer_display = ttk.Label(main_frame, text="25:00", font=("TkDefaultFont", 18))
        self.timer_display.grid(row=0, column=0, rowspan=3, sticky="w", padx=(0, 20))

        self.counter_label = ttk.Label(main_frame, text="0/4", font=("TkDefaultFont", 10))
        self.counter_label.grid(row=2, column=0, sticky="w", padx=(22, 0), pady=(40, 0))

        self.start_button = ttk.Button(main_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=2, column=1, sticky="ew", pady=(20, 0))

        self.stop_button = ttk.Button(main_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=2, sticky="ew", pady=(20, 0))

        self.settings_button = ttk.Button(main_frame, text="Settings", command=self.open_settings)
        self.settings_button.grid(row=2, column=3, sticky="ew", pady=(20, 0))

        self.reset_timer()
        self.root.mainloop()

    def reset_timer(self):
        self.work_time = self.work_duration
        self.break_time = self.short_break_duration
        self.is_work_time = True
        self.completed_pomodoros = 0
        self.is_timer_running = False
        self.update_timer_display()
        self.update_counter_display()

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

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("250x300")
        settings_win.resizable(False, False)

        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        settings_win.geometry(f"+{main_x + 250}+{main_y}")

        ttk.Label(settings_win, text="Opacity (10–100%)").pack(pady=(10, 0))
        opacity_var = tk.IntVar(value=int(self.opacity_level * 100))
        ttk.Scale(settings_win, from_=0, to=100, orient="horizontal", variable=opacity_var).pack(pady=5)

        ttk.Label(settings_win, text="Work Duration (minutes)").pack()
        work_var = tk.IntVar(value=self.work_duration // 60)
        ttk.Entry(settings_win, textvariable=work_var).pack(pady=5)

        ttk.Label(settings_win, text="Short Break (minutes)").pack()
        short_var = tk.IntVar(value=self.short_break_duration // 60)
        ttk.Entry(settings_win, textvariable=short_var).pack(pady=5)

        ttk.Label(settings_win, text="Long Break (minutes)").pack()
        long_var = tk.IntVar(value=self.long_break_duration // 60)
        ttk.Entry(settings_win, textvariable=long_var).pack(pady=5)

        def apply_settings():
            try:
                new_opacity = max(10, min(100, opacity_var.get()))
                self.opacity_level = new_opacity / 100
                self.root.attributes("-alpha", self.opacity_level)

                self.work_duration = max(1, work_var.get()) * 60
                self.short_break_duration = max(1, short_var.get()) * 60
                self.long_break_duration = max(1, long_var.get()) * 60

                self.reset_timer()
                settings_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        ttk.Button(settings_win, text="Apply", command=apply_settings).pack(pady=10)

    def countdown(self):
        if self.is_timer_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time <= 0:
                    self.completed_pomodoros += 1
                    self.update_counter_display()
                    self.is_work_time = False
                    if self.completed_pomodoros % 4 == 0:
                        self.break_time = self.long_break_duration
                        messagebox.showinfo("Pomodoro Complete", "Time for a long break")
                    else:
                        self.break_time = self.short_break_duration
                        messagebox.showinfo("Pomodoro Complete", "Time for a short break")
            else:
                self.break_time -= 1
                if self.break_time <= 0:
                    self.is_work_time = True
                    self.work_time = self.work_duration
                    if self.completed_pomodoros % 4 == 0:
                        self.completed_pomodoros = 0
                        self.update_counter_display()
                    messagebox.showinfo("Break Over", "Time for some work")

            self.update_timer_display()
            self.root.after(1000, self.countdown)

    def update_timer_display(self):
        time_left = self.work_time if self.is_work_time else self.break_time
        minutes, seconds = divmod(time_left, 60)
        self.timer_display.config(text=f"{minutes:02d}:{seconds:02d}")

    def update_counter_display(self):
        pomodoro_count = self.completed_pomodoros % 4
        self.counter_label.config(text=f"{pomodoro_count}/4")


if __name__ == "__main__":
    PomodoroTimer()
