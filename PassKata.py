import streamlit as st
from cryptography.fernet import Fernet
import os
import smtplib
from email.mime.text import MIMEText

# Generate and save encryption key
KEY_FILE = "key.key"
PASSWORD_FILE = "passwords.txt"
USER_CREDENTIALS_FILE = "user_credentials.txt"
EMAIL = "anton.sanjaya0889@gmail.com"

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

def save_user_credentials(username, password, email):
    """Save user credentials to a file."""
    encrypted_password = encrypt_password(password)
    with open(USER_CREDENTIALS_FILE, 'w') as file:
        file.write(f"{username} | {encrypted_password.decode()} | {email}\n")

def load_user_credentials():
    """Load user credentials from the file."""
    if not os.path.exists(USER_CREDENTIALS_FILE):
        return None, None, None
    with open(USER_CREDENTIALS_FILE, 'r') as file:
        line = file.readline().strip()
        username, encrypted_password, email = line.split(' | ')
        password = decrypt_password(encrypted_password.encode())
        return username, password, email

def send_email(subject, body, to_email):
    """Send an email with the given subject and body."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = "noreply@example.com"
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            # Use environment variables or replace these with valid credentials
            server.login("your_email@gmail.com", "your_email_password")
            server.sendmail("noreply@example.com", to_email, msg.as_string())
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Streamlit UI
st.title("Password Manager")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not os.path.exists(USER_CREDENTIALS_FILE):
    st.subheader("Set Up New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_email = st.text_input("Email Address")
    if st.button("Save User"):
        if new_username and new_password and new_email:
            save_user_credentials(new_username, new_password, new_email)
            st.success("User credentials saved successfully.")
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields.")
else:
    saved_username, saved_password, saved_email = load_user_credentials()

    if not st.session_state["authenticated"]:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == saved_username and password == saved_password:
                st.session_state["authenticated"] = True
                st.success("Logged in successfully.")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        if st.button("Forgot Password"):
            send_email(
                subject="Password Recovery",
                body=f"Your credentials:\nUsername: {saved_username}\nPassword: {saved_password}",
                to_email=saved_email
            )
            st.info(f"Credentials have been sent to {saved_email}.")
    else:
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

        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.success("Logged out successfully.")
            st.experimental_rerun()
