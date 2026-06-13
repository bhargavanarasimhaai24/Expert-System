from data.students import students
from data.books import books

def get_student_level(student):

    cgpa = student["cgpa"]
    cie = student["cie_total"]

    if cgpa < 7 or cie < 30:
        return "WEAK"

    elif cgpa >= 8.5 and cie >= 40:
        return "STRONG"

    else:
        return "AVERAGE"


def get_subject_data(subject):

    return books.get(subject.upper())


def generate_study_advice(
        level,
        subject,
        career_goal):

    advice = []

    if level == "WEAK":

        advice.append(
            "Focus primarily on Text Books."
        )

        advice.append(
            "Build strong fundamentals before using reference books."
        )

    elif level == "AVERAGE":

        advice.append(
            "Study Text Books thoroughly."
        )

        advice.append(
            "Use 1-2 reference books for deeper understanding."
        )

    else:

        advice.append(
            "Study both Text Books and Reference Books."
        )

        advice.append(
            "Solve additional problems and explore advanced topics."
        )

    # Career specific advice

    if career_goal == "ML Engineer":

        if subject in ["IML", "IAI", "MML"]:

            advice.append(
                "This subject is highly relevant for Machine Learning."
            )

    elif career_goal == "Data Scientist":

        if subject in ["IML", "IST", "MML"]:

            advice.append(
                "Focus on mathematical and statistical foundations."
            )

    elif career_goal == "Software Engineer":

        if subject in ["DAA", "OPS"]:

            advice.append(
                "Master problem solving and system concepts."
            )

    elif career_goal == "Researcher":

        advice.append(
            "Read reference books extensively and explore research topics."
        )

    return advice


def recommend_books(usn, subject):

    student = students.get(usn)

    if not student:
        return None

    subject = subject.upper()

    subject_data = get_subject_data(subject)

    if not subject_data:
        return None

    level = get_student_level(student)

    recommendations = {
        "student_name": student["name"],
        "usn": usn,
        "subject": subject,
        "cgpa": student["cgpa"],
        "cie_total": student["cie_total"],
        "career_goal": student["career_goal"],
        "student_level": level,
        "textbooks": [],
        "reference_books": [],
        "advice": []
    }

    # --------------------------
    # WEAK
    # --------------------------

    if level == "WEAK":

        recommendations["textbooks"] = (
            subject_data["textbooks"]
        )

        recommendations["reference_books"] = []

    # --------------------------
    # AVERAGE
    # --------------------------

    elif level == "AVERAGE":

        recommendations["textbooks"] = (
            subject_data["textbooks"]
        )

        recommendations["reference_books"] = (
            subject_data["reference_books"][:2]
        )

    # --------------------------
    # STRONG
    # --------------------------

    else:

        recommendations["textbooks"] = (
            subject_data["textbooks"]
        )

        recommendations["reference_books"] = (
            subject_data["reference_books"]
        )

    recommendations["advice"] = generate_study_advice(
        level,
        subject,
        student["career_goal"]
    )

    return recommendations


def generate_library_report(
        usn,
        subject):

    report = recommend_books(
        usn,
        subject
    )

    if not report:
        return "Student or Subject not found."

    output = []

    output.append("=" * 60)
    output.append("LIBRARY EXPERT RECOMMENDATION")
    output.append("=" * 60)

    output.append(
        f"Student Name : {report['student_name']}"
    )

    output.append(
        f"USN          : {report['usn']}"
    )

    output.append(
        f"Subject      : {report['subject']}"
    )

    output.append(
        f"CGPA         : {report['cgpa']}"
    )

    output.append(
        f"CIE Total    : {report['cie_total']}"
    )

    output.append(
        f"Career Goal  : {report['career_goal']}"
    )

    output.append(
        f"Level        : {report['student_level']}"
    )

    output.append("")

    output.append("TEXT BOOKS")

    for i, book in enumerate(
            report["textbooks"],
            start=1):

        output.append(
            f"{i}. {book}"
        )

    output.append("")

    output.append("REFERENCE BOOKS")

    if report["reference_books"]:

        for i, book in enumerate(
                report["reference_books"],
                start=1):

            output.append(
                f"{i}. {book}"
            )

    else:

        output.append(
            "Reference books not recommended currently."
        )

    output.append("")
    output.append("EXPERT ADVICE")

    for advice in report["advice"]:

        output.append(
            f"- {advice}"
        )

    output.append("=" * 60)

    return "\n".join(output)