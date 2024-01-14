import tkinter as tk
from tkinter import ttk
from datetime import timedelta


class CountdownApp:
    def __init__(self, master):
        self.master = master

        master.overrideredirect(True)
        master.geometry("230x160+200+200")

        master.bind("<Button-1>", self.start_move)
        master.bind("<ButtonRelease-1>", self.stop_move)
        master.bind("<B1-Motion>", self.on_move)

        self.state = False
        self.total_time = 0

        self.timer_label = ttk.Label(master, text="00:00:00", font=("default", 40))
        self.timer_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.horizontal_separator = ttk.Separator(master, orient='horizontal')
        self.horizontal_separator.grid(row=1, column=0, sticky="ew", columnspan=3)

        self.time_entry_label = ttk.Label(master, text="Enter time for countdown (hh:mm:ss):")
        self.time_entry_label.grid(row=2, column=0, columnspan=3)

        self.time_entry_hour = ttk.Spinbox(master, from_=0, to=23, width=6)
        self.time_entry_hour.set("00")  # Set default value
        self.time_entry_hour.grid(row=3, column=0, padx=(10, 0))

        self.time_entry_minute = ttk.Spinbox(master, from_=0, to=59, width=6)
        self.time_entry_minute.set("20")
        self.time_entry_minute.grid(row=3, column=1)

        self.time_entry_second = ttk.Spinbox(master, from_=0, to=59, width=6)
        self.time_entry_second.set("00")
        self.time_entry_second.grid(row=3, column=2)

        self.start_button = ttk.Button(master, text="Start", command=self.start)
        self.start_button.grid(row=4, column=0)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop)
        self.stop_button.grid(row=4, column=1)

        self.exit_button = ttk.Button(master, text="Exit", command=master.quit)
        self.exit_button.grid(row=4, column=2)

    def clear_placeholder(self, event):
        if self.time_entry.get() == 'hh:mm:ss':
            self.time_entry.delete(0, 'end')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")

    def start(self):
        if not self.state:
            time_string = f"{self.time_entry_hour.get()}:{self.time_entry_minute.get()}:{self.time_entry_second.get()}"
            self.total_time = self.time_string_to_seconds(time_string)
            self.state = True
            self.master.after(1000, self.countdown)

    def stop(self):
        self.state = False

    def countdown(self):
        if self.state and self.total_time > 0:
            self.total_time -= 1
            self.timer_label.config(text=self.seconds_to_time_string(self.total_time))
            self.master.after(1000, self.countdown)
        else:
            self.state = False

    def time_string_to_seconds(self, time_string):
        hours, minutes, seconds = map(int, time_string.split(":"))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()

    def seconds_to_time_string(self, seconds):
        return str(timedelta(seconds=seconds))


root = tk.Tk()
root.attributes('-topmost', 1)  # This line makes the window always stay on top
app = CountdownApp(root)
root.mainloop()
