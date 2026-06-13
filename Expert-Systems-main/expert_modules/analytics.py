from data.students import students


def generate_analytics_report(usn):

    student = students[usn]

    attendance = student["attendance"]

    percentages = {}

    for subject, data in attendance.items():

        percent = (
            data["attended"] /
            data["conducted"]
        ) * 100

        percentages[subject] = round(percent, 2)

    strongest_subject = max(
        percentages,
        key=percentages.get
    )

    weakest_subject = min(
        percentages,
        key=percentages.get
    )

    avg_attendance = (
        sum(percentages.values())
        / len(percentages)
    )

    report = []

    report.append("=" * 60)
    report.append("STUDENT ANALYTICS DASHBOARD")
    report.append("=" * 60)

    report.append(f"Name          : {student['name']}")
    report.append(f"Branch        : {student['branch']}")
    report.append(f"Semester      : {student['semester']}")
    report.append(f"CGPA          : {student['cgpa']}")
    report.append(f"CIE Total     : {student['cie_total']}/50")
    report.append(f"AICTE Points  : {student['aicte_points']}")

    report.append("")
    report.append("ATTENDANCE OVERVIEW")
    report.append("-" * 60)

    for subject, percent in percentages.items():

        report.append(
            f"{subject:<8} : {percent:.2f}%"
        )

    report.append("")

    report.append(
        f"Average Attendance : {avg_attendance:.2f}%"
    )

    report.append("")

    report.append(
        f"Strongest Subject : {strongest_subject}"
    )

    report.append(
        f"Weakest Subject   : {weakest_subject}"
    )

    report.append("")

    report.append("ACADEMIC STATUS")
    report.append("-" * 60)

    cgpa = student["cgpa"]

    if cgpa >= 9:
        report.append(
            "Excellent Academic Performance"
        )

    elif cgpa >= 8:
        report.append(
            "Very Good Academic Performance"
        )

    elif cgpa >= 7:
        report.append(
            "Good Academic Performance"
        )

    else:
        report.append(
            "Needs Improvement"
        )

    report.append("")

    report.append("EXPERT INSIGHTS")
    report.append("-" * 60)

    if avg_attendance < 75:

        report.append(
            "Attendance is below recommended level."
        )

    else:

        report.append(
            "Attendance is satisfactory."
        )

    if student["aicte_points"] >= 100:

        report.append(
            "Excellent AICTE participation."
        )

    elif student["aicte_points"] >= 50:

        report.append(
            "Good AICTE progress."
        )

    else:

        report.append(
            "Increase participation in AICTE activities."
        )

    if student["cie_total"] < 25:

        report.append(
            "CIE performance requires immediate attention."
        )

    elif student["cie_total"] < 35:

        report.append(
            "CIE performance can be improved."
        )

    else:

        report.append(
            "CIE performance is good."
        )

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)