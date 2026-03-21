import streamlit as st
import PyPDF2

# Title
st.title("📄 Resume Analyzer")

# File Upload
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

# Skills list
skills_list = ["Python", "Java", "C++", "SQL", "Machine Learning", "Data Science", "HTML", "CSS", "JavaScript"]

if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    st.subheader("📜 Resume Content")
    st.write(text)

    # Word Count
    word_count = len(text.split())
    st.write("📝 Word Count:", word_count)

    # Skills Detection
    st.subheader("💡 Skills Found")
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    st.write(found_skills)

    # Resume Score
    score = len(found_skills) * 10

    st.subheader("📊 Resume Score")
    st.write(score, "/ 100")

    # Suggestions
    st.subheader("📢 Suggestions")

    if score < 50:
        st.write("❌ Add more skills to improve your resume.")
    else:
        st.write("✅ Good resume! Try adding projects and experience.")