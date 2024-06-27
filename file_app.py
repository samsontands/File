import streamlit as st
import os
import base64
from datetime import datetime

# Set page config
st.set_page_config(page_title="File Management App with Login", layout="wide")

# User credentials
USERS = {
    "samson tan": "lala1112",
    "117743": "117743",
    "116627": "116627"
}

# Function to save uploaded file
def save_uploaded_file(uploaded_file, directory, username):
    user_dir = os.path.join(directory, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(user_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filename, file_path

# Function to get file download link
def get_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'

# Login function
def login(username, password):
    if username in USERS and USERS[username] == password:
        return True
    return False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Main app
st.title("File Management App with Login")

# Login section
if not st.session_state.logged_in:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# File management section (only visible after login)
if st.session_state.logged_in:
    st.header(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

    # File upload section
    st.header("Upload Files")
    uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True, key="general_files")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name, file_path = save_uploaded_file(uploaded_file, "uploads/files", st.session_state.username)
            st.success(f"File uploaded successfully: {file_name}")

    # File display and download section
    st.header("View and Download Your Files")

    # Display user's files
    user_files_dir = os.path.join("uploads/files", st.session_state.username)
    if os.path.exists(user_files_dir):
        files = os.listdir(user_files_dir)
        if files:
            for file in files:
                file_path = os.path.join(user_files_dir, file)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{file}**")
                with col2:
                    st.markdown(get_download_link(file_path, file), unsafe_allow_html=True)
        else:
            st.info("No files available")
    else:
        st.info("No files have been uploaded yet")
