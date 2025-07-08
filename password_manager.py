import random
import string
import json
import os

BASE_DIR = os.path.join(os.path.expanduser("~"), "Password Manager")
STORED_FILE = os.path.join(BASE_DIR, "passwords.json")
os.makedirs(BASE_DIR, exist_ok=True)

def create_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def save_password(service, username, password):
    data = load_data()

    if service in data:
        overwrite = input(f"An entry for '{service}' exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Save canceled.")
            return

    data[service] = {
        "username": username,
        "password": password
    }

    try:
        with open(STORED_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("Error saving password:", e)
        input("Press Enter to exit...")

def get_password(service):
    data = load_data()
    return data.get(service)

def delete_password(service):
    data = load_data()
    if not data:
        print("No stored passwords.")
        return
    if service in data:
        del data[service]
        with open(STORED_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Entry for {service} removed")
    else:
        print(f"No entry found for {service}")

def load_data():
    if not os.path.exists(STORED_FILE):
        return {}
    with open(STORED_FILE, 'r') as f:
        try:
            return json.load(f)
        except Exception:
            print("Error loading stored password file")
            return {}


if __name__ == "__main__":
    while True:
        print("\n1. Generate Password")
        print("2. Save Password")
        print("3. Retrieve Password")
        print("4. Delete Password")
        print("5. Saved services")
        print("6. Exit")
        choice = input("Choose an option: \n")

        if choice == "1":
            try:
                length = int(input("Enter password length: \n"))
                if length < 4 or length > 128:
                    print("Please enter a length between 4 and 128.")
                    continue
            except ValueError:
                print("Invalid input; please enter a number.")
                continue
                
            print("Generated Password:", create_password(length))

        elif choice == "2":
            service = input("Enter service name (e.g. Gmail): \n").strip().lower()
            username = input("Enter your username/email: \n")
            use_generated = input("Generate password? (y/n): \n").lower()

            if use_generated == "y":
                password = create_password()
                print("Generated Password:", password)
            else:
                password = input("Enter your password: \n")

            save_password(service, username, password)
            print("Password saved.")

        elif choice == "3":
            service = input("Enter service name to retrieve: \n").strip().lower()
            creds = get_password(service)
            if creds:
                print("Username:", creds["username"])
                print("Password:", creds["password"])
            else:
                print("No password found for that service.")
        elif choice == "4":
            service = input("Enter service name to delete\n").strip().lower()
            delete_password(service)
        elif choice == "5":
            data = load_data()
            if data:
                print("Saved services:")
                for service in data:
                    print("-", service)
            else:
                print("No services saved.")

        elif choice == "6":
            break

        else:
            print("Invalid option. Try again.")
