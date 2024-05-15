import tkinter as tk
import subprocess

def run_nmap_tk():
    # Replace 'script1.py' with the path to your Python script
    subprocess.run(["python3", "Brute_Force/nmap.py"])

def run_brute_force_gui():
    # Replace 'script2.py' with the path to your Python script
    subprocess.run(["python3", "Brute_Force/Brute_Force.py"])

root = tk.Tk()
root.title("Main Page")
root.geometry("300x100")

btn_program_1 = tk.Button(root, text="Run Nmap", command=run_nmap_tk)
btn_program_1.pack(pady=10)

btn_program_2 = tk.Button(root, text="Run Brute Force Attack GUI", command=run_brute_force_gui)
btn_program_2.pack(pady=10)

root.mainloop()
