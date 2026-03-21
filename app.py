import streamlit as st
import PyPDF2

st.title("Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    st.subheader("Resume Content")
    st.write(text)

    st.subheader("Word Count")
    st.write(len(text.split()))