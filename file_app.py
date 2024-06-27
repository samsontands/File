import streamlit as st
import os
import base64
from datetime import datetime

# Set page config
st.set_page_config(page_title="File Upload and Download App", layout="wide")

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    # Create a 'uploads' directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join("uploads", filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filename

# Function to get file download link
def get_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'
    return href

# Main app
st.title("File Upload and Download App")

# File upload section
st.header("Upload Files")
uploaded_files = st.file_uploader("Choose files to upload", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = save_uploaded_file(uploaded_file)
        st.success(f"File uploaded successfully: {file_name}")

# Text input section
st.header("Upload Text")
text_input = st.text_area("Enter text to save as a file")
text_filename = st.text_input("Enter filename for the text (include extension, e.g., notes.txt)")

if st.button("Save Text"):
    if text_input and text_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_{text_filename}"
        file_path = os.path.join("uploads", file_name)
        with open(file_path, "w") as f:
            f.write(text_input)
        st.success(f"Text saved as file: {file_name}")
    else:
        st.warning("Please enter both text and filename")

# File download section
st.header("Download Files")
if os.path.exists("uploads"):
    files = os.listdir("uploads")
    if files:
        for file in files:
            file_path = os.path.join("uploads", file)
            st.markdown(get_download_link(file_path, file), unsafe_allow_html=True)
    else:
        st.info("No files available for download")
else:
    st.info("No files have been uploaded yet")
