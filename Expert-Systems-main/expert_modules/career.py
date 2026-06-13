from data.students import students


def generate_career_report(usn):

    student = students[usn]

    cgpa = student["cgpa"]
    cie = student["cie_total"]
    interests = student["interests"]
    career_goal = student["career_goal"]
    coding_level = student["coding_level"]

    careers = []
    skills = []

    if "AI" in interests or "Machine Learning" in interests:
        careers.append("Machine Learning Engineer")
        skills.extend([
            "Python",
            "NumPy",
            "Pandas",
            "Scikit-Learn"
        ])

    if "Programming" in interests or coding_level == "Advanced":
        careers.append("Software Developer")
        skills.extend([
            "Data Structures",
            "Algorithms",
            "System Design"
        ])

    if cgpa >= 8.5:
        careers.append("Research Assistant")
        skills.extend([
            "Research Methodology",
            "Technical Writing"
        ])

    if career_goal.lower() == "higher studies":
        careers.append("Academic Researcher")
        skills.extend([
            "Publications",
            "Research Papers"
        ])

    careers = list(dict.fromkeys(careers))
    skills = list(dict.fromkeys(skills))

    report = []

    report.append("=" * 60)
    report.append("CAREER GUIDANCE REPORT")
    report.append("=" * 60)

    report.append(f"Student : {student['name']}")
    report.append(f"CGPA    : {cgpa}")
    report.append(f"CIE     : {cie}/50")
    report.append("")

    report.append("RECOMMENDED CAREERS")
    report.append("-" * 60)

    for i, career in enumerate(careers, start=1):
        report.append(f"{i}. {career}")

    report.append("")
    report.append("SKILLS TO DEVELOP")
    report.append("-" * 60)

    for skill in skills:
        report.append(f"• {skill}")

    report.append("")
    report.append("EXPERT RECOMMENDATION")
    report.append("-" * 60)

    if cgpa >= 8:
        report.append(
            "Strong academic profile. Aim for internships and advanced projects."
        )
    else:
        report.append(
            "Focus on improving academics while building practical skills."
        )

    report.append("=" * 60)

    return "\n".join(report)