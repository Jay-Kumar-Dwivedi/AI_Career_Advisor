
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("career.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            skills TEXT,
            interest TEXT,
            career TEXT
        )
    """)
    conn.commit()
    conn.close()

def recommend_career(skills, interest):
    skills = skills.lower()
    interest = interest.lower()

    scores = {}

    # Data Analyst
    da = 0
    if "data" in interest: da += 40
    if "excel" in skills: da += 20
    if "sql" in skills: da += 20
    if "power bi" in skills: da += 15
    if "statistics" in skills or "statistics" in interest: da += 5
    scores["Data Analyst"] = da

    # Python Developer
    py = 0
    if "python" in skills: py += 40
    if "software" in interest: py += 25
    if "oop" in skills or "django" in skills or "flask" in skills: py += 20
    if "git" in skills: py += 15
    scores["Python Developer"] = py

    # Web Developer
    web = 0
    if "web" in interest: web += 40
    if "html" in skills: web += 20
    if "css" in skills: web += 15
    if "javascript" in skills or "js" in skills: web += 20
    if "react" in skills: web += 5
    scores["Web Developer"] = web

    # AI / ML Engineer
    ai = 0
    if "ai" in interest or "machine learning" in interest or "ml" in interest: ai += 40
    if "python" in skills: ai += 20
    if "tensorflow" in skills or "pytorch" in skills or "keras" in skills: ai += 25
    if "numpy" in skills or "pandas" in skills: ai += 15
    scores["AI / ML Engineer"] = ai

    # Cybersecurity Analyst
    cs = 0
    if "cyber" in interest or "security" in interest or "hacking" in interest: cs += 45
    if "networking" in skills or "linux" in skills: cs += 25
    if "python" in skills: cs += 15
    if "firewall" in skills or "kali" in skills: cs += 15
    scores["Cybersecurity Analyst"] = cs

    # DevOps Engineer
    dv = 0
    if "devops" in interest or "cloud" in interest or "deployment" in interest: dv += 40
    if "docker" in skills or "kubernetes" in skills: dv += 25
    if "linux" in skills: dv += 15
    if "aws" in skills or "azure" in skills or "gcp" in skills: dv += 20
    scores["DevOps Engineer"] = dv

    # Pick best match
    best = max(scores, key=scores.get)
    confidence = min(scores[best], 95)
    if confidence < 30:
        confidence = 30  # minimum baseline

    careers = {
        "Data Analyst": (
            ["Advanced Excel", "SQL", "Power BI", "Python", "Tableau"],
            "Build a sales dashboard that shows revenue trends and KPIs using Python and Power BI."
        ),
        "Python Developer": (
            ["Python", "OOP", "Flask", "Git and GitHub", "REST APIs"],
            "Build a task manager or student management application with a web interface."
        ),
        "Web Developer": (
            ["HTML", "CSS", "JavaScript", "React", "Flask"],
            "Build a personal portfolio website with a contact form and project showcase."
        ),
        "AI / ML Engineer": (
            ["Python", "NumPy & Pandas", "Scikit-learn", "TensorFlow", "Model Deployment"],
            "Build a student performance predictor using a machine learning classification model."
        ),
        "Cybersecurity Analyst": (
            ["Networking Basics", "Linux", "Python Scripting", "Ethical Hacking", "OWASP Top 10"],
            "Build a port scanner tool and a basic intrusion detection system in Python."
        ),
        "DevOps Engineer": (
            ["Linux", "Docker", "Kubernetes", "CI/CD Pipelines", "AWS / Azure"],
            "Deploy a Flask web app using Docker and set up a CI/CD pipeline with GitHub Actions."
        ),
    }

    roadmap, project = careers.get(best, (
        ["Python basics", "SQL", "Git", "Problem solving"],
        "Build a simple student record management system."
    ))

    return best, roadmap, project, confidence

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        skills = request.form.get("skills", "").strip()
        interest = request.form.get("interest", "").strip()
        experience = request.form.get("experience", "beginner").strip()
        education = request.form.get("education", "").strip()

        if not name or not skills or not interest:
            return "Please fill in all fields.", 400

        career, roadmap, project, confidence = recommend_career(
            skills, interest
        )

        conn = sqlite3.connect("career.db")
        conn.execute(
            """INSERT INTO assessments
            (name, skills, interest, career)
            VALUES (?, ?, ?, ?)""",
            (name, skills, interest, career)
        )
        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            name=name,
            career=career,
            roadmap=roadmap,
            project=project,
            confidence=confidence,
            experience=experience,
            education=education
        )

    return render_template("index.html")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
