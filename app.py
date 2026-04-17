import streamlit as st
import PyPDF2
import re
import matplotlib.pyplot as plt
from collections import Counter

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📄 AI Resume Analyzer")
st.write("Upload your Resume PDF and get smart analysis instantly 🚀")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

# ---------------- SKILLS DATABASE ----------------
skills_list = [
    "Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Flask", "Django", "Machine Learning",
    "Data Science", "AWS", "Git", "Excel", "Power BI"
]

# ---------------- MAIN ----------------
if uploaded_file is not None:

    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    text_lower = text.lower()

    # ---------------- WORD COUNT ----------------
    word_count = len(text.split())

    # ---------------- SKILLS FOUND ----------------
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    skills_found_count = len(found_skills)
    missing_skills = len(skills_list) - skills_found_count

    # ---------------- CONTACT DETAILS ----------------
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phones = re.findall(r'\d{10}', text.replace(" ", ""))

    # ---------------- SCORE ----------------
    score = 0

    if word_count > 150:
        score += 25
    elif word_count > 80:
        score += 15

    if skills_found_count >= 8:
        score += 40
    elif skills_found_count >= 5:
        score += 25
    elif skills_found_count >= 2:
        score += 15

    if emails:
        score += 15

    if phones:
        score += 20

    if score > 100:
        score = 100

    # ---------------- RESUME CONTENT ----------------
    st.subheader("📜 Resume Content")
    st.write(text)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📝 Word Count", word_count)

    with col2:
        st.metric("💡 Skills Found", skills_found_count)

    with col3:
        st.metric("📊 Resume Score", f"{score}/100")

    st.progress(score / 100)

    # ---------------- CONTACT ----------------
    st.subheader("📞 Contact Details")

    if emails:
        st.success(f"Email: {emails[0]}")
    else:
        st.error("Email not found")

    if phones:
        st.success(f"Phone: {phones[0]}")
    else:
        st.error("Phone not found")

    # ---------------- SKILLS ----------------
    st.subheader("💡 Skills Found")

    if found_skills:
        st.write(found_skills)
    else:
        st.warning("No matching skills found")

    # ---------------- SUGGESTIONS ----------------
    st.subheader("📢 Suggestions")

    if skills_found_count < 5:
        st.warning("Add more technical skills.")

    if word_count < 100:
        st.warning("Resume is too short. Add projects and experience.")

    if not phones:
        st.warning("Add phone number.")

    if not emails:
        st.warning("Add email.")

    if score >= 80:
        st.success("Excellent Resume 🚀")
    elif score >= 60:
        st.info("Good Resume 👍")
    else:
        st.error("Needs Improvement ❌")

    # ---------------- GRAPH 1 ----------------
    st.subheader("📊 Skills Analysis")

    labels = ["Found Skills", "Missing Skills"]
    values = [skills_found_count, missing_skills]

    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.bar(labels, values)
    ax1.set_title("Skills Comparison")
    st.pyplot(fig1)

    # ---------------- GRAPH 2 ----------------
    st.subheader("📈 Resume Composition")

    useful_words = len(found_skills) * 10
    other_words = max(word_count - useful_words, 1)

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.pie(
        [useful_words, other_words],
        labels=["Skills", "Other"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.axis("equal")
    st.pyplot(fig2)

    # ---------------- GRAPH 3 ----------------
    st.subheader("📌 Top Keywords")

    stop_words = [
        'in', 'the', 'and', 'is', 'of', 'to', 'a', 'for',
        'on', 'with', 'at', 'by', 'an', 'or'
    ]

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    filtered_words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    common_words = Counter(filtered_words).most_common(5)

    if common_words:
        word_names = [i[0] for i in common_words]
        word_counts = [i[1] for i in common_words]

        fig3, ax3 = plt.subplots(figsize=(6, 3))
        ax3.bar(word_names, word_counts)
        ax3.set_title("Most Used Words")
        ax3.tick_params(axis='x', labelrotation=20)
        st.pyplot(fig3)

else:
    st.info("Please upload your resume PDF.")