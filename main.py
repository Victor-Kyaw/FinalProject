import tkinter as tk
from tkinter import ttk
import subprocess
import os

current_directory = os.getcwd()
process = None

def run_program():
    global process
    try:
        process = subprocess.Popen(["python3", current_directory+"/nmap_tk.py"])
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
        switch_button.config(text="RUN Nmap", style="SwitchButton.Off.TButton")
        stop_program()
    else:
        switch_button.config(text="CLOSE Nmap", style="SwitchButton.On.TButton")
        run_program()
    switch_state = not switch_state

def create_window():
    global switch_state
    switch_state = False

    # Create the main window
    root = tk.Tk()
    root.title("TOOLS")

    root.geometry("300x500")  # Width x Height

    # Create the style for the switch button
    style = ttk.Style()
    style.configure("SwitchButton.On.TButton", foreground="green")
    style.configure("SwitchButton.Off.TButton", foreground="red")

    # Create the switch (Button)
    global switch_button
    switch_button = ttk.Button(root, text="RUN Nmap", style="SwitchButton.Off.TButton", command=toggle_switch)
    switch_button.grid(ipadx=50, ipady=30 )
    switch_button.place(x=150, y=50)
    # switch_button.pack(pady=50)

    # Run the main event loop
    root.mainloop()

if __name__ == "__main__":
    create_window()
