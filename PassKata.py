from cryptography.fernet import Fernet
import os

# Generate and save encryption key
KEY_FILE = "key.key"
PASSWORD_FILE = "passwords.txt"

def generate_key():
    """Generate and save a key for encryption."""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)


def load_key():
    """Load the encryption key from file."""
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_password(password):
    """Encrypt a password."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password):
    """Decrypt a password."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

def save_password(service, username, password):
    """Save an encrypted password to a file."""
    encrypted_password = encrypt_password(password)
    with open(PASSWORD_FILE, 'a') as file:
        file.write(f"{service} | {username} | {encrypted_password.decode()}\n")

def retrieve_password():
    """Retrieve and decrypt passwords from the file."""
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords stored yet.")
        return

    with open(PASSWORD_FILE, 'r') as file:
        for line in file:
            service, username, encrypted_password = line.strip().split(' | ')
            decrypted_password = decrypt_password(encrypted_password.encode())
            print(f"Service: {service}, Username: {username}, Password: {decrypted_password}")

if __name__ == "__main__":
    print("Password Manager")
    while True:
        print("\nOptions:")
        print("1. Save a new password")
        print("2. Retrieve saved passwords")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(service, username, password)
            print("Password saved successfully.")
        elif choice == "2":
            retrieve_password()
        elif choice == "3":
            print("Exiting password manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
