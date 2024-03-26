import streamlit as st
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.image("data/resume.png", width=700)

nav = st.sidebar.radio("Navigation",["Scanner"])      

if nav == 'Scanner':
    st.write('Job Description')
    txt = st.text_area('Paste text')

    # Title for the app
    st.write("File Upload Example")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file", type='docx')

    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Display some information about the file
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

    if st.button("Scan"):
        # Extract text from the text area directly
        r1 = txt
        # Extract text from the uploaded file
        if uploaded_file:
            try:
                r2 = docx2txt.process(uploaded_file)
            except Exception as e:
                st.error("An error occurred while processing the file. Please try again.")
                r2 = ""
        else:
            r2 = ""

# resume match score