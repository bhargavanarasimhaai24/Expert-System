from data.students import students

def calculate_percentage(attended, conducted):
    if conducted == 0:
        return 0
    return round((attended / conducted) * 100, 2)


def get_attendance_status(percentage):

    if percentage < 75:
        return "CRITICAL"

    elif percentage < 85:
        return "CONDONATION"

    else:
        return "SAFE"


def get_subject_advice(percentage):

    if percentage < 75:
        return ("Attendance shortage. Apply valid certificates if available, meet faculty and attend all upcoming classes.")

    elif percentage < 85:
        return ("Eligible for condonation, but improving attendance is recommended.")

    else:
        return ("Attendance is safe.")


def analyze_attendance(usn):

    student = students.get(usn)

    if not student:
        return None

    results = []

    total_attended = 0
    total_conducted = 0

    highest_subject = None
    highest_percentage = -1

    lowest_subject = None
    lowest_percentage = 101

    for subject, details in student["attendance"].items():

        attended = details["attended"]
        conducted = details["conducted"]

        percentage = calculate_percentage(attended,conducted)

        status = get_attendance_status(percentage)

        advice = get_subject_advice(percentage)

        results.append({
            "subject": subject,
            "attended": attended,
            "conducted": conducted,
            "percentage": percentage,
            "status": status,
            "advice": advice
        })

        total_attended += attended
        total_conducted += conducted

        if percentage > highest_percentage:
            highest_percentage = percentage
            highest_subject = subject

        if percentage < lowest_percentage:
            lowest_percentage = percentage
            lowest_subject = subject

    overall_percentage = calculate_percentage(total_attended,total_conducted)

    overall_status = get_attendance_status(overall_percentage)

    if overall_status == "CRITICAL":

        overall_advice = "Overall attendance is below 75%. Immediate action required. Meet faculty advisors and improve attendance."

    elif overall_status == "CONDONATION":

        overall_advice = "Attendance is in condonation zone. Avoid unnecessary leave."

    else:

        overall_advice = "Attendance is healthy. You may plan occasional leave if necessary."

    return {
        "student_name": student["name"],
        "usn": usn,

        "overall_percentage": overall_percentage,
        "overall_status": overall_status,
        "overall_advice": overall_advice,

        "best_subject": highest_subject,
        "best_percentage": highest_percentage,

        "worst_subject": lowest_subject,
        "worst_percentage": lowest_percentage,

        "subject_analysis": results
    }

def generate_attendance_report(usn):

    report = analyze_attendance(usn)

    if not report:
        return "Student not found."

    output = []

    output.append("=" * 60)
    output.append("ATTENDANCE EXPERT REPORT")
    output.append("=" * 60)

    output.append(
        f"Student : {report['student_name']}"
    )

    output.append(
        f"USN     : {report['usn']}"
    )

    output.append("")

    output.append(
        f"Overall Attendance : "
        f"{report['overall_percentage']}%"
    )

    output.append(
        f"Status             : "
        f"{report['overall_status']}"
    )

    output.append(
        f"Advice             : "
        f"{report['overall_advice']}"
    )

    output.append("")

    output.append(
        f"Best Subject  : "
        f"{report['best_subject']} "
        f"({report['best_percentage']}%)"
    )

    output.append(
        f"Worst Subject : "
        f"{report['worst_subject']} "
        f"({report['worst_percentage']}%)"
    )

    output.append("")
    output.append("SUBJECT ANALYSIS")
    output.append("-" * 60)

    for item in report["subject_analysis"]:

        output.append(
            f"{item['subject']} | "
            f"{item['percentage']}% | "
            f"{item['status']}"
        )

    output.append("=" * 60)

    return "\n".join(output)