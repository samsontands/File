import streamlit as st
import os
import base64
from datetime import datetime

# Set page config
st.set_page_config(page_title="File Management App with Login", layout="wide")

# User credentials
USERS = {
    "samson tan": "117853",
    "117743": "117743",
    "116627": "116627"
}

# Function to save uploaded file
def save_uploaded_file(uploaded_file, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(directory, filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filename

# Function to get file download link
def get_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'

# Function to read text file content
def read_text_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

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
            file_name = save_uploaded_file(uploaded_file, "uploads/files")
            st.success(f"File uploaded successfully: {file_name}")

    # Font upload section
    st.header("Upload Fonts")
    uploaded_fonts = st.file_uploader("Choose font files to upload (.ttf, .otf)", 
                                      accept_multiple_files=True, 
                                      type=['ttf', 'otf'],
                                      key="font_files")

    if uploaded_fonts:
        for uploaded_font in uploaded_fonts:
            font_name = save_uploaded_file(uploaded_font, "uploads/fonts")
            st.success(f"Font uploaded successfully: {font_name}")

    # Text input section
    st.header("Upload Text")
    text_input = st.text_area("Enter text to save as a file")
    text_filename = st.text_input("Enter filename for the text (include extension, e.g., notes.txt)")

    if st.button("Save Text"):
        if text_input and text_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{timestamp}_{text_filename}"
            file_path = os.path.join("uploads/texts", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(text_input)
            st.success(f"Text saved as file: {file_name}")
        else:
            st.warning("Please enter both text and filename")

    # File display and download section
    st.header("View and Download Files")

    # Function to display files from a specific directory
    def display_files(directory, header):
        st.subheader(header)
        if os.path.exists(directory):
            files = os.listdir(directory)
            if files:
                for file in files:
                    file_path = os.path.join(directory, file)
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{file}**")
                    with col2:
                        st.markdown(get_download_link(file_path, file), unsafe_allow_html=True)
                    
                    # If it's a text file, display its content
                    if directory == "uploads/texts":
                        with st.expander("View Content"):
                            content = read_text_file(file_path)
                            st.text_area("", value=content, height=200, key=f"text_{file}")
                            st.markdown("*You can copy the text from the box above.*")
            else:
                st.info(f"No {header.lower()} available")
        else:
            st.info(f"No {header.lower()} have been uploaded yet")

    # Display files for each category
    display_files("uploads/files", "General Files")
    display_files("uploads/fonts", "Fonts")
    display_files("uploads/texts", "Text Files")
