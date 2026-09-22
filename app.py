import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI-Powered Resume Analyzer & Job Matcher")

skills = [
    "Python", "SQL", "Excel", "Power BI", "Pandas",
    "NumPy", "Machine Learning", "Deep Learning",
    "NLP", "Tableau", "MySQL", "Git", "GitHub",
    "Statistics", "DAX", "Java", "JavaScript",
    "HTML", "CSS", "React", "Node.js", "MongoDB",
    "Flask", "Django", "FastAPI"
]

recommendations = {
    "NumPy": "Learn NumPy arrays, indexing and mathematical operations.",
    "Statistics": "Learn mean, median, probability, distributions and hypothesis testing.",
    "Python": "Practice Python programming and problem-solving.",
    "SQL": "Practice SQL queries, joins, subqueries and window functions.",
    "Excel": "Learn advanced Excel formulas, Pivot Tables and Power Query.",
    "Power BI": "Practice DAX, data modeling and interactive dashboards.",
    "Pandas": "Practice data cleaning, grouping and data manipulation.",
    "MySQL": "Practice database design, joins and SQL queries.",
    "DAX": "Practice DAX formulas and calculated columns in Power BI.",
    "Java": "Practice Java programming and object-oriented concepts.",
    "JavaScript": "Practice JavaScript fundamentals and DOM manipulation.",
    "HTML": "Practice semantic HTML and web page structure.",
    "CSS": "Practice responsive design, Flexbox and Grid.",
    "React": "Learn React components, props, state and hooks.",
    "Node.js": "Learn Node.js and backend API development.",
    "MongoDB": "Practice MongoDB CRUD operations and database design.",
    "Flask": "Learn Flask routes, APIs and backend development.",
    "Django": "Learn Django models, views, URLs and REST APIs.",
    "FastAPI": "Practice building REST APIs with FastAPI."
}

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("🔍 Analyze Resume"):

    if resume_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a Job Description.")

    else:

        with st.spinner("Reading resume..."):

            pdf_bytes = resume_file.getvalue()
            pages = convert_from_bytes(pdf_bytes)

            resume_text = ""

            for page in pages:
                resume_text += pytesseract.image_to_string(page)

        found_skills = []

        for skill in skills:
            if skill.lower() in resume_text.lower():
                found_skills.append(skill)

        required_skills = []

        for skill in skills:
            if skill.lower() in job_description.lower():
                required_skills.append(skill)

        matched_skills = []
        missing_skills = []

        for skill in required_skills:

            if skill.lower() in resume_text.lower():
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        if required_skills:

            match_score = (
                len(matched_skills) /
                len(required_skills)
            ) * 100

        else:
            match_score = 0

        st.success("Resume analyzed successfully!")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Match Score",
            f"{match_score:.1f}%"
        )

        col2.metric(
            "Matched Skills",
            len(matched_skills)
        )

        col3.metric(
            "Missing Skills",
            len(missing_skills)
        )

        st.subheader("✅ Skills Found in Resume")
        st.write(found_skills)

        st.subheader("🟢 Matched Skills")
        st.write(matched_skills)

        st.subheader("🔴 Missing Skills")
        st.write(missing_skills)

        st.subheader("💡 Skill Gap Recommendations")

        for skill in missing_skills:

            st.write(f"**{skill}**")

            st.write(
                recommendations.get(
                    skill,
                    "Practice this skill with projects and hands-on exercises."
                )
            )

        st.subheader("📊 Skill Match Dashboard")

        labels = [
            "Matched Skills",
            "Missing Skills"
        ]

        values = [
            len(matched_skills),
            len(missing_skills)
        ]

        fig, ax = plt.subplots()

        ax.bar(labels, values)

        ax.set_ylabel("Number of Skills")

        ax.set_title(
            f"Resume Match Score: {match_score:.1f}%"
        )

        st.pyplot(fig)
