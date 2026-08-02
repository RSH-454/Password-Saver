import os
import json
import getpass
import hashlib
from cryptography.fernet import Fernet

def file_names():
    if os.name == "nt":
        return "vault.json", "auth.hash", "secret.key"
    else:
        return ".vault.json", ".auth.hash", ".secret.key"

file_data, auth, key_file = file_names()


def header():
    os.system("cls" if os.name == "nt" else "clear")
    print(r"""
   ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
  ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
  ╚██████╗██║  ██║   ██║   ██║        ██║   
   ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝  

               PASSWORD MANAGER
               ver 0.4.0-beta.1
""")


def hide_file(filename):
    if os.name == "nt" and os.path.exists(filename):
        os.system(f'attrib +h "{filename}"')


def unhide_file(filename):
    if os.name == "nt" and os.path.exists(filename):
        os.system(f'attrib -h "{filename}"')


def check_file(path):
    return (not os.path.exists(path)) or os.path.getsize(path) == 0


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_key():
    if check_file(key_file):
        key = Fernet.generate_key()

        with open(key_file, "wb") as f:
            f.write(key)

        hide_file(key_file)
        return key

    with open(key_file, "rb") as f:
        return f.read()


def encrypt_password(password):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()


def load_vault():
    if check_file(file_data):
        return []

    with open(file_data, "r") as f:
        return json.load(f)


def save_vault(vault):
    unhide_file(file_data)

    with open(file_data, "w") as f:
        json.dump(vault, f, indent=4)

    hide_file(file_data)


def access():
    if check_file(auth):
        set_password = getpass.getpass("Create a password: ").strip()
        stored_hash = hash_password(set_password)

        with open(auth, "w") as f:
            f.write(stored_hash)

        hide_file(auth)

    else:
        with open(auth, "r") as f:
            stored_hash = f.read().strip()

    while True:
        password = getpass.getpass("Enter password: ").strip()

        if hash_password(password) == stored_hash:
            print("[ACCESS GRANTED]\n")
            break
        else:
            print("[ACCESS DENIED]: Incorrect password. Try again.\n")


def save():
    account = input("Enter name of the account: ").strip()
    password = getpass.getpass("Enter password: ").strip()

    encrypted_password = encrypt_password(password)

    vault = load_vault()

    vault.append({
        "account": account,
        "password": encrypted_password
    })

    save_vault(vault)

    print("Account saved successfully.")


def search():
    account = input("Enter the name of the account you want to view: ").strip()

    vault = load_vault()

    if not vault:
        print("No passwords saved yet.")
        return

    for entry in vault:
        if entry["account"] == account:
            decrypted_password = decrypt_password(entry["password"])
            print(f"Account: {entry['account']} Password: {decrypted_password}")
            return

    print("Account not found.")


def view_all():
    vault = load_vault()

    if not vault:
        print("No passwords saved yet.")
        return

    for entry in vault:
        decrypted_password = decrypt_password(entry["password"])
        print(f"Account: {entry['account']} Password: {decrypted_password}")


def reset_password():
    current_password = getpass.getpass("Enter your current password: ").strip()

    with open(auth, "r") as f:
        stored_hash = f.read().strip()

    if hash_password(current_password) != stored_hash:
        print("Incorrect current password.")
        return

    new_password = getpass.getpass("Enter new password: ").strip()
    confirm_password = getpass.getpass("Confirm new password: ").strip()

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    unhide_file(auth)

    with open(auth, "w") as f:
        f.write(hash_password(new_password))

    hide_file(auth)

    print("Password reset successful.")

header()
access()
input("Press enter to continue...\n")

while True:
    option = input(
        "Choose option: \n"
        " 1. Save \n"
        " 2. Search \n"
        " 3. View all \n"
        " 4. Reset Password \n"
        " 5. Exit \n"
        "Option: "
    )

    if option == "1":
        save()
        input("Press enter to return to menu...\n")

    elif option == "2":
        search()
        input("Press enter to return to menu...\n")

    elif option == "3":
        view_all()
        input("Press enter to return to menu...\n")

    elif option == "4":
        reset_password()
        input("Press enter to return to menu...\n")

    elif option == "5":
        print("Goodbye.")
        clear = "cls" if os.name == "nt" else "clear"
        os.system(clear)
        break

    else:
        print("Invalid option.")
        input("Press enter to return to menu...\n")