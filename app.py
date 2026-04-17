import streamlit as st
import PyPDF2
import re

# ---------------- Page Settings ----------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# ---------------- Title ----------------
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a Job Description.")

# ---------------- Sidebar ----------------
st.sidebar.header("About")
st.sidebar.write("This tool analyzes resumes, detects skills, and checks job match score.")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type="pdf")

# ---------------- Job Description ----------------
jd_text = st.text_area("📋 Paste Job Description Here")

# ---------------- Skills List ----------------
skills_list = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Data Science", "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Flask", "Django"
]

# ---------------- If File Uploaded ----------------
if uploaded_file is not None:

    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # ---------------- Resume Content ----------------
    st.subheader("📜 Resume Content")
    st.write(text)

    # ---------------- Word Count ----------------
    word_count = len(text.split())

    # ---------------- Email & Phone ----------------
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\d{10}', text)

    # ---------------- Skills Detection ----------------
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # ---------------- Resume Score ----------------
    score = min(len(found_skills) * 10, 100)

    # ---------------- Dashboard ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("📝 Word Count", word_count)
    col2.metric("💡 Skills Found", len(found_skills))
    col3.metric("📊 Resume Score", f"{score}/100")

    st.progress(score)

    # ---------------- Contact Info ----------------
    st.subheader("📞 Contact Details")

    if email:
        st.write("📧 Email:", email[0])
    else:
        st.write("❌ Email not found")

    if phone:
        st.write("📱 Phone:", phone[0])
    else:
        st.write("❌ Phone not found")

    # ---------------- Skills Found ----------------
    st.subheader("💡 Skills Found")
    st.write(found_skills)

    # ---------------- Suggestions ----------------
    st.subheader("📢 Suggestions")

    if score < 40:
        st.error("Add more technical skills, projects, and certifications.")
    elif score < 70:
        st.warning("Good resume. Add more experience and achievements.")
    else:
        st.success("Excellent resume! Ready to apply.")

    # ---------------- Job Description Match ----------------
    if jd_text:

        resume_words = set(text.lower().split())
        jd_words = set(jd_text.lower().split())

        common_words = resume_words.intersection(jd_words)

        if len(jd_words) > 0:
            match_score = int((len(common_words) / len(jd_words)) * 100)
        else:
            match_score = 0

        st.subheader("🎯 Job Match Score")
        st.metric("Match Percentage", f"{match_score}%")
        st.progress(match_score)

        # Missing Keywords
        missing = jd_words - resume_words

        st.subheader("❌ Missing Keywords")
        st.write(list(missing)[:20])

        # Final Suggestion
        if match_score < 50:
            st.error("Low match. Add missing keywords to improve ATS chances.")
        elif match_score < 75:
            st.warning("Moderate match. Improve resume for better chances.")
        else:
            st.success("Strong match for this job role!")

else:
    st.info("Please upload your resume PDF to begin.")