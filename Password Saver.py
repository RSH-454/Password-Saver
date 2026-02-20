print('[PASSWWORD SAVER]')
input('Press enter to continue...\n')
Option = input('Choose operation: \n 1. Save new password \n 2. View saved passwords \n 3. Exit') 

FileName = 'SavedPasswords.txt'
def SaveNew():
    print('Enter name of the account: ')
    Account = input()
    print('Enter password: ')
    Password = input()
    with open(FileName, 'w') as f:
        f.write("Account: " + Account + " " + "Password: " + Password)  

def ViewSaved():
    print('Enter the name of the account you want to view: ')
    Account = input()
    with open(FileName, 'r') as f:
        content = f.read()
        if Account in content:
            print(content)
        else:
            print("Account not found.")

if Option == '1':
    SaveNew()

elif Option == '2':
    ViewSaved()

elif Option == '3':
    exit()