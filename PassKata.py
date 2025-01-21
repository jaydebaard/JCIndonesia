import streamlit as st
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

def retrieve_passwords():
    """Retrieve and decrypt passwords from the file."""
    if not os.path.exists(PASSWORD_FILE):
        return []

    passwords = []
    with open(PASSWORD_FILE, 'r') as file:
        for line in file:
            try:
                service, username, encrypted_password = line.strip().split(' | ')
                decrypted_password = decrypt_password(encrypted_password.encode())
                passwords.append((service, username, decrypted_password))
            except ValueError:
                continue  # Skip lines that do not match the expected format
    return passwords

# Streamlit UI
st.title("Password Manager")

menu = ["Save Password", "View Passwords"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Save Password":
    st.subheader("Save a New Password")
    service = st.text_input("Service Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Save"):
        if service and username and password:
            save_password(service, username, password)
            st.success("Password saved successfully.")
        else:
            st.error("Please fill in all fields.")

elif choice == "View Passwords":
    st.subheader("Stored Passwords")
    passwords = retrieve_passwords()
    if passwords:
        for service, username, password in passwords:
            st.write(f"**Service:** {service}")
            st.write(f"**Username:** {username}")
            st.write(f"**Password:** {password}")
            st.write("---")
    else:
        st.info("No passwords stored yet.")
