'''
author: Jimmy Yeh
date: 2023/1/31

future work:
- second button change music "change alarm"
- drop_down menu for music
- stop flashing after music ends or after set time
- package into executable

- activate sudo and use keyboard to control (enter, space)?
- fix button area and fill good color?
- threading??
'''

import os
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont

from pathlib import Path

import subprocess
from utils import *


class TimerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.configure_gui()
        self.text_messages_and_options()
        self.reset_gui()

    def text_messages_and_options(self):
        self.default_text = "my pomodoro clock 😂"
        self.default_work_text = ":}work phase{:"
        self.default_rest_text = ":) rest phase (:"
        self.rest_text_list = [
            "🎉 ~~time to rest~~ 🤤", 
            "🎉 ~~hallelujah~~ 🤤", "🎉 ~~happy~happy~~ 🤤", "🎉 ~~have a cup of tea~~ 🤤",
            "🎉 ~~time to chat~~ 🤤", "🎉 ~~relax and be glad~~ 🤤", "🎉 ~~tip tip tap tap~~ 🤤"
            ]
        self.work_text_list = [
            "💪 !!time to work!! 🤔", 
            "💪 !!grace abounds!! 🤔", "💪 !!go!go!go!go!! 🤔", "💪 !!give him the glory!! 🤔", 
            "💪 !!time to soar!! 🤔", "💪 !!hear the lion roar!! 🤔", "💪 !!I will have more!! 🤔"]

        self.work_options = ("20", "25", "30", "45")
        self.rest_options = ("5", "10", "15", "20")
        self.process = False
        self.pause = False
        self.after_stop_alarm = False

    def configure_gui(self):
        self.geometry("420x285+{}+{}".format(
            int(self.winfo_screenwidth() / 2) + 250,
            int(self.winfo_screenheight() / 2) - 300
        ))
        self.resizable(0, 0)
        self.configure(bg=code_rgb()) 
        self.title('my pomodoro')
        
        self.clockframe = tk.Frame(self)
        self.clockframe.pack(side="top", pady=15)
        self.clock_text = tk.Label(self.clockframe, bg=code_rgb())
        self.clock_text.pack(side="top")
        
        self.displaytext = tk.StringVar()
        display = tk.Label(self, textvariable=self.displaytext, font=("Times New Roman", 36), bg=code_rgb())
        display.pack(side="top")
        mainframe = tk.Frame(self)
        mainframe.pack(side="top", pady=10)

        # create buttons
        buttons_frame = tk.Frame(mainframe)
        buttons_frame.pack(side="left", fill="x")
        self.start_button = tk.Button(buttons_frame, width=12, font=("Helvetica", 22))
        self.start_button.pack(fill="x", pady=1)
        self.stop_button = tk.Button(buttons_frame, width=12, font=("Helvetica", 22))
        self.stop_button.pack(fill="x", pady=1)

        # create combo_boxes
        fillin_frame = tk.Frame(mainframe)
        fillin_frame.pack(side="left", fill="x", padx=30)
        
        work_frame = tk.Frame(fillin_frame)
        work_frame.pack(fill="x", pady=1)
        
        self.work_label = tk.Label(work_frame, text="(work for", width=6)
        self.work_label.pack(side="left", fill="x")
        self.work_entry = ttk.Combobox(work_frame, state="readonly", width=3)
        self.work_entry.pack(side="left")

        self.work_time_label = tk.Label(work_frame, text="min)", width=3)
        self.work_time_label.pack(side="left", fill="x")

        rest_frame = tk.Frame(fillin_frame)
        rest_frame.pack(fill="x", pady=1)
        
        self.rest_label = tk.Label(rest_frame, text="(rest for", width=6)
        self.rest_label.pack(side="left", fill="x")
        self.rest_entry = ttk.Combobox(rest_frame, state="readonly", width=3)
        self.rest_entry.pack(side="left")

        self.rest_time_label = tk.Label(rest_frame, text="min)", width=3)
        self.rest_time_label.pack(side="left", fill="x")

    def reset_gui(self):
        self.pause = True
        self.displaytext.set(self.default_text)
        self.start_button.configure(text="Start Working", command=self.start_timer)
        self.stop_button.configure(text="Change Alarm", command=self.change_alarm)
        self.work_label.configure(text="(work for", width=6)
        self.work_time_label.configure(text="min)", width=3)
        self.rest_label.configure(text="(rest for", width=6)
        self.rest_time_label.configure(text="min)", width=3)
        self.work_entry.configure(width=3)
        self.work_entry['values'] = self.work_options
        self.work_entry.current(1)
        self.rest_entry.configure(width=3)
        self.rest_entry['values'] = self.rest_options
        self.rest_entry.current(0)

        self.work_alarm = 'work_alarm/we_are_standing_on_holy_ground.mp3'
        self.rest_alarm = 'rest_alarm/waloyo_yamoni.mp3'
        self.tsec = 671
        self.update_clock()

    ## CLOSING and RUNNING and Update_clock ##

    def on_closing(self):
        if self.process:
            self.process.kill()
        self.destroy()

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def update_clock(self):
        mins, secs = divmod(self.tsec, 60)
        timetext = '{:02d}:{:02d}'.format(mins, secs)
        clockimg = create_clock_textimg(timetext)
        self.clock_text.configure(image=clockimg)
        self.clock_text.image = clockimg

        if self.process:
            textlist = self.work_text_list if self.workphase else self.rest_text_list
            self.displaytext.set(textlist[secs % len(textlist)])

    
    #### BUTTON FUNCTIONS (DFS) ####

    def start_timer(self):
        self.start_button.configure(text="Pause", command=self.pause_countdown)
        self.stop_button.configure(text="Stop", command=self.reset_gui)
        self.work_time = int(self.work_entry.get())
        self.rest_time = int(self.rest_entry.get())
        self.workphase = True
        self.displaytext.set(self.default_work_text)
        self.tsec = int(self.work_time*60)        
        if len(sys.argv) == 2:
            self.tsec = 10

        self.countdown()

    def pause_countdown(self):
        self.pause = True
        self.tsec += 1
        self.update_clock()
        self.update()
        self.start_button.configure(text="Continue", command=self.continue_countdown)
        self.stop_button.configure(text="Stop", command=self.reset_gui)
        self.stop_alarm()

    def continue_countdown(self):
        # self.reset_gui(True)
        self.start_button.configure(text="Pause", command=self.pause_countdown)
        self.stop_button.configure(text="Stop", command=self.reset_gui)
        self.countdown()

    def countdown(self):
        self.pause = False
        tsec_init = self.tsec
        self.update_clock()
        self.update()
        start = time.time()
        wait_time = 0.7
        while self.tsec:
            if self.tsec >=1 and self.tsec != tsec_init:
                # self.call_time = time.time()
                self.update_clock()
                if self.pause:
                    print('pause!')
                    return 
                self.update()
            while True:
                if self.pause:
                    return
                time.sleep(wait_time)
                wait_time = 0.001
                timedelta = 1-(time.time() - start - (tsec_init - self.tsec))
                if timedelta <= 0.0001:
                    break
            self.tsec -= 1

        self.play_alarm()
        if len(sys.argv) == 2:
            self.tsec = 10
        self.countdown()

    def play_alarm(self):
        self.stop_button.configure(text="Stop Alarm", command=self.stop_alarm)
        
        if self.process:
            self.process.kill()
            self.process = False
        if self.workphase:
            self.workphase = False
            self.process = subprocess.Popen(["afplay", self.rest_alarm])
            self.update()
            self.focus_force()
            self.tsec = self.rest_time*60
        else:
            self.workphase = True
            self.process = subprocess.Popen(["afplay", self.work_alarm])
            self.update()
            self.focus_force()
            self.tsec = self.work_time*60

        self.after_stop_alarm = self.after(1000*132, self.stop_alarm)

        # self.stop_alarm()

    def stop_alarm(self):
        if self.process:
            self.process.kill()
            self.process = False
        if self.workphase:
            self.displaytext.set(self.default_work_text)
        else:
            self.displaytext.set(self.default_rest_text)
        self.stop_button.configure(text="Stop", command=self.reset_gui)
        if self.after_stop_alarm:
            self.after_stop_alarm = False

    def change_alarm(self):
        self.displaytext.set("choose alarm music 😉")
        self.start_button.configure(text="Confirm", command=self.confirm_change_alarm)
        self.stop_button.configure(text="Cancel", command=self.reset_gui)

        self.work_label.configure(text="work:", width=5)
        self.work_time_label.configure(text="")
        self.rest_label.configure(text="rest:", width=5)
        self.rest_time_label.configure(text="")

        self.work_entry.configure(width=25)
        self.work_entry['values'] = os.listdir('work_alarm')
        self.work_entry.current(0)
        self.rest_entry.configure(width=25)
        self.rest_entry['values'] = os.listdir('rest_alarm')
        self.rest_entry.current(0)

    def confirm_change_alarm(self):
        self.work_alarm = self.work_entry.get()
        self.rest_alarm = self.rest_entry.get()
        full_ticker = f'::⏰ 🎵:: 🤔💪 [{self.work_alarm}]; 🤤🎉 [{self.rest_alarm}]'
        ticker_width = 16
        self.displaytext.set(full_ticker[:ticker_width])
        self.update()
        time.sleep(0.3)
        for i in range(len(full_ticker) - ticker_width+1):
            self.displaytext.set(full_ticker[i:ticker_width+i])
            self.update()
            time.sleep(0.2)
        time.sleep(0.7)

        self.work_alarm = Path('work_alarm')/self.work_alarm
        self.rest_alarm = Path('rest_alarm')/self.rest_alarm
        self.reset_gui()


if __name__ == "__main__":
    app = TimerApp()
    app.run()


    