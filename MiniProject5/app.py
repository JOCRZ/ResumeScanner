import streamlit as st
import os
import fitz
import tempfile
from docx import Document

# Functions to convert file to txt format


def extract_text_from_pdf(pdf_path):
    text = ""
    # Open the PDF file
    with fitz.open(pdf_path) as pdf_document:
        # Iterate through each page in the PDF
        for page_num in range(pdf_document.page_count):
            # Get the page
            page = pdf_document.load_page(page_num)
            # Extract text from the page
            text += page.get_text()
    return text


def extract_text_from_docx(docx_path):
    text = ""
    # Open the .docx file
    doc = Document(docx_path)
    # Extract text from each paragraph in the document
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def to_load_file(uploaded_file):
    if uploaded_file is None:
        return None  # Handle case where no file is uploaded
    
    def check_allowed_file_extension(filename):
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_extension = os.path.splitext(filename)[1].lower()
        return file_extension in allowed_extensions

    filename = uploaded_file.name  # Use filename property
    if check_allowed_file_extension(filename):
        # Create a temporary directory to store the uploaded file
        temp_dir = tempfile.TemporaryDirectory()
        file_path = os.path.join(temp_dir.name, filename)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())  # Write the file content to the temporary directory
        if filename.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        elif filename.endswith('.docx'):
            return extract_text_from_docx(file_path)
        else:
            with open(file_path, 'r') as f:
                return f.read()  # Read the content of the file
    else:
        raise ValueError("File extension is not allowed.")


st.write('Convert pdf,docx to txt')

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=['docx','pdf','txt'])

if uploaded_file is not None:
  text = to_load_file(uploaded_file)  # Pass the uploaded file to the function
  if st.button("Show"):
      st.write(text)
