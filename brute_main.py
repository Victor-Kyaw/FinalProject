import tkinter as tk
from tkinter import ttk
from tkinter import *

import subprocess
import os

current_directory = os.getcwd()
process = None

def run_program():
    global process
    try:
        process = subprocess.Popen(["python3", current_directory+"/brute_force/brute_force_main.py"])
    except FileNotFoundError:
        print("Error: The specified Python program was not found.")
    except Exception as e:
        print("An error occurred:", e)

def stop_program():
    global process
    if process:
        process.terminate()
        process = None

def toggle_switch():
    global switch_state
    if switch_state:
        switch_button.config(text="RUN ATTACK", style="SwitchButton.Off.TButton")
        stop_program()
    else:
        switch_button.config(text="CALCEN ATTACK", style="SwitchButton.On.TButton")
        run_program()
    switch_state = not switch_state

def create_window():
    global switch_state
    switch_state = False

    # Create the main window
    root = tk.Tk()
    root.title("BRUTE FORCE ATTACK")

    root.geometry("400x500")  # Width x Height
    root.resizable(True,True)

    # Create the style for the switch button
    style = ttk.Style()
    style.configure("SwitchButton.On.TButton", foreground="red")
    style.configure("SwitchButton.Off.TButton", foreground="green")

    # Create the switch (Button)
    global switch_button
    switch_button = ttk.Button(root, text="RUN ATTACK", style="SwitchButton.Off.TButton", command=toggle_switch)
    switch_button.grid(ipadx=50, ipady=30 )
    switch_button.place(x=150, y=50)
    # switch_button.pack(pady=50)

    # Text box
    frame = Frame(root)
    frame.place(x = 16, y = 275, width = 370, height = 215)
    listbox = Listbox(frame, width = 59, height = 6)
    listbox.place(x = 0, y = 0)
    listbox.bind('<<ListboxSelect>>')
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Run the main event loop
    root.mainloop()
if __name__ == "__main__":
    create_window()
