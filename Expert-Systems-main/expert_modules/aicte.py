from data.students import students
from expert_modules.clubs import recommend_clubs

REQUIRED_POINTS = 100
AVERAGE_POINTS_PER_ACTIVITY = 15


def get_aicte_status(points):

    if points >= REQUIRED_POINTS:
        return "COMPLETED"

    elif points >= 80:
        return "ALMOST COMPLETE"

    elif points >= 50:
        return "MODERATE"

    else:
        return "HIGH RISK"


def get_urgency(remaining_points):

    if remaining_points == 0:
        return "NONE"

    elif remaining_points <= 20:
        return "LOW"

    elif remaining_points <= 50:
        return "MEDIUM"

    else:
        return "HIGH"


def estimate_activities_needed(remaining_points):

    if remaining_points <= 0:
        return 0

    activities = remaining_points // AVERAGE_POINTS_PER_ACTIVITY

    if remaining_points % AVERAGE_POINTS_PER_ACTIVITY != 0:
        activities += 1

    return activities


def get_expert_advice(status, remaining_points):

    if status == "COMPLETED":

        return (
            "You have already satisfied the AICTE requirement. "
            "Continue participating in activities that improve your skills and profile."
        )

    elif status == "ALMOST COMPLETE":

        return (
            f"You need only {remaining_points} more points. "
            "Participate in 1 or 2 club activities, workshops, hackathons, "
            "or technical events to complete the requirement."
        )

    elif status == "MODERATE":

        return (
            f"You still require {remaining_points} points. "
            "Actively participate in technical clubs, competitions, "
            "workshops and institutional events this semester."
        )

    else:

        return (
            f"You require {remaining_points} additional points. "
            "Immediate participation is recommended. Join active clubs "
            "and regularly participate in technical and non-technical events."
        )


def get_top_recommended_clubs(usn, limit=5):

    recommendations = recommend_clubs(usn)

    if not recommendations:
        return []

    clubs = []

    for club in recommendations["best_matches"]:
        clubs.append(club)

    for club in recommendations["better_matches"]:
        clubs.append(club)

    clubs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return clubs[:limit]


def analyze_aicte(usn):

    student = students.get(usn)

    if not student:
        return None

    current_points = student["aicte_points"]

    remaining_points = max(
        0,
        REQUIRED_POINTS - current_points
    )

    status = get_aicte_status(
        current_points
    )

    urgency = get_urgency(
        remaining_points
    )

    activities_needed = estimate_activities_needed(
        remaining_points
    )

    advice = get_expert_advice(
        status,
        remaining_points
    )

    recommended_clubs = get_top_recommended_clubs(
        usn
    )

    return {

        "student_name": student["name"],

        "usn": usn,

        "current_points": current_points,

        "required_points": REQUIRED_POINTS,

        "remaining_points": remaining_points,

        "status": status,

        "urgency": urgency,

        "estimated_activities_needed": activities_needed,

        "recommended_clubs": recommended_clubs,

        "expert_advice": advice
    }


def generate_aicte_report(usn):

    report = analyze_aicte(usn)

    if not report:
        return "Student not found."

    output = []

    output.append("=" * 50)
    output.append("AICTE PROGRESS REPORT")
    output.append("=" * 50)

    output.append(f"Student Name : {report['student_name']}")
    output.append(f"USN          : {report['usn']}")

    output.append("")

    output.append(
        f"Current Points      : {report['current_points']}"
    )

    output.append(
        f"Required Points     : {report['required_points']}"
    )

    output.append(
        f"Remaining Points    : {report['remaining_points']}"
    )

    output.append(
        f"Status              : {report['status']}"
    )

    output.append(
        f"Urgency Level       : {report['urgency']}"
    )

    output.append(
        f"Activities Needed   : {report['estimated_activities_needed']}"
    )

    output.append("")

    output.append("RECOMMENDED CLUBS")

    if report["recommended_clubs"]:

        for i, club in enumerate(
            report["recommended_clubs"],
            start=1
        ):

            output.append(
                f"{i}. {club['club']} "
                f"(Score: {club['score']})"
            )

    else:

        output.append(
            "No club recommendations available."
        )

    output.append("")
    output.append("EXPERT ADVICE")
    output.append(report["expert_advice"])

    output.append("=" * 50)

    return "\n".join(output)