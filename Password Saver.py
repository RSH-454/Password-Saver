import os
FileName = 'SavedData.txt'

#This function allows the user to save new data. 
def Save():
    print('Enter name of the account: ')
    Account = input()
    print('Enter password: ')
    Password = input()
    with open(FileName, 'a') as f:
        f.write("Account: " + Account + " " + "Password: " + Password + "\n")

#This function allows the user to view previously saved data. 
def Search():
    print('Enter the name of the account you want to view: ')
    Account = input()
    if CheckFile(FileName):
        print("No passwords saved yet.")
        return
    with open(FileName, 'r') as f:
        content = f.read()
        for line in content.splitlines():  
         if Account in line:
            print(line)    
            break
        else:
          print("Account not found.")

#This function allows the user to view all previously saved data.
def ViewAll():
    if CheckFile(FileName):
        print("No passwords saved yet.")
        return
    with open(FileName, 'r') as f:
        content = f.read()
        print(content)          

#This function checks if the file exists or if it is empty.
def CheckFile(Path):
    return (not os.path.exists(Path)) or os.path.getsize(Path) == 0

#This function allows the user to create and set a password for access. 
def Access():
    Authorization = "SetPassword.txt"
    if CheckFile(Authorization):
        CreatePassword = input('Create a password to access the password saver: ')
        with open(Authorization, 'w') as f:
            f.write(CreatePassword)
    else:
        with open(Authorization, 'r') as f:
            CreatePassword = f.read()
    while True:
        Password = input('Enter password: ')
        if Password == CreatePassword:
            print('Access granted.\n')
            break
        else:
            print('Incorrect password. Try again.\n')

Access()
print('[PASSWORD SAVER]')
input('Press enter to continue...\n')
while True:
    Option = input('Choose option: \n 1. Save \n 2. Search \n 3. View all \n 4. Exit\nOption: ')
 
    if Option == '1':
        Save()
        input('Press enter to return to menu...\n')

    elif Option == '2':
        Search()
        input('Press enter to return to menu...\n')

    elif Option == '3':
        ViewAll()
        input('Press enter to return to menu...\n')

    elif Option == '4':
        break 