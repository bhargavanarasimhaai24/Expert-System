from data.students import students
from data.clubs import clubs


def recommend_clubs(usn):

    student = students.get(usn)

    if not student:
        return None

    interests = set(student["interests"])

    career_goal = student["career_goal"]
    coding_level = student["coding_level"]
    aicte_points = student["aicte_points"]

    best_matches = []
    better_matches = []
    okay_matches = []

    for club_name, club_data in clubs.items():

        score = 0
        reasons = []

        club_interests = set(club_data["interests"])

        # --------------------------
        # Interest Matching
        # --------------------------

        common = interests.intersection(club_interests)

        score += len(common) * 3

        if common:
            reasons.append(
                f"Matches interests: {', '.join(common)}"
            )

        # --------------------------
        # Career Goal Rules
        # --------------------------

        if career_goal == "ML Engineer":

            if (
                "AI" in club_interests
                or "Machine Learning" in club_interests
                or "Data Science" in club_interests
            ):
                score += 4
                reasons.append(
                    "Supports ML Engineer career goal"
                )

        elif career_goal == "Data Scientist":

            if (
                "AI" in club_interests
                or "Data Science" in club_interests
                or "Research" in club_interests
            ):
                score += 4
                reasons.append(
                    "Supports Data Scientist career goal"
                )

        elif career_goal == "Software Engineer":

            if (
                "Coding" in club_interests
                or "Software Development" in club_interests
                or "Problem Solving" in club_interests
            ):
                score += 4
                reasons.append(
                    "Supports Software Engineer career goal"
                )

        elif career_goal == "Robotics Engineer":

            if (
                "Robotics" in club_interests
                or "Automation" in club_interests
                or "Electronics" in club_interests
            ):
                score += 4
                reasons.append(
                    "Supports Robotics Engineer career goal"
                )

        elif career_goal == "Entrepreneur":

            if (
                "Entrepreneurship" in club_interests
                or "Business" in club_interests
                or "Leadership" in club_interests
            ):
                score += 4
                reasons.append(
                    "Supports Entrepreneurship goal"
                )

        # --------------------------
        # Coding Level Bonus
        # --------------------------

        if coding_level == "Advanced":

            if (
                "Competitive Programming" in club_interests
                or "Coding" in club_interests
            ):
                score += 2

        elif coding_level == "Beginner":

            if (
                "Leadership" in club_interests
                or "Public Speaking" in club_interests
            ):
                score += 1

        # --------------------------
        # AICTE Suggestion Bonus
        # --------------------------

        if aicte_points < 100:

            if club_data["aicte_points_estimate"] >= 15:
                score += 1

        # --------------------------
        # Categorization
        # --------------------------

        club_result = {
            "club": club_name,
            "score": score,
            "category": club_data["category"],
            "aicte_points": club_data["aicte_points_estimate"],
            "reasons": reasons
        }

        if score >= 8:
            best_matches.append(club_result)

        elif score >= 4:
            better_matches.append(club_result)

        elif score >= 1:
            okay_matches.append(club_result)

    # Sort by score descending

    best_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    better_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    okay_matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------
    # AICTE Analysis
    # --------------------------

    aicte_status = {}

    if aicte_points >= 100:

        aicte_status["status"] = "Completed"
        aicte_status["remaining"] = 0

    else:

        aicte_status["status"] = "Incomplete"
        aicte_status["remaining"] = 100 - aicte_points

    return {

        "student_name": student["name"],
        "usn": usn,

        "aicte_points": aicte_points,

        "aicte_status": aicte_status,

        "best_matches": best_matches,

        "better_matches": better_matches,

        "okay_matches": okay_matches
    }

def generate_club_report(usn):

    report = recommend_clubs(usn)

    if not report:
        return "Student not found."

    output = []

    output.append("=" * 60)
    output.append("CLUB RECOMMENDATION REPORT")
    output.append("=" * 60)

    output.append(
        f"Student Name : {report['student_name']}"
    )

    output.append(
        f"USN          : {report['usn']}"
    )

    output.append(
        f"AICTE Points : {report['aicte_points']}"
    )

    output.append("")

    output.append("BEST MATCHES ⭐")
    output.append("-" * 60)

    if report["best_matches"]:

        for club in report["best_matches"]:

            output.append(
                f"\n{club['club']}"
            )

            output.append(
                f"Score : {club['score']}"
            )

            output.append(
                f"Category : {club['category']}"
            )

            output.append(
                f"AICTE Points : {club['aicte_points']}"
            )

            for reason in club["reasons"]:

                output.append(
                    f"  • {reason}"
                )

    else:

        output.append("No Best Matches Found")

    output.append("")
    output.append("BETTER MATCHES 👍")
    output.append("-" * 60)

    if report["better_matches"]:

        for club in report["better_matches"]:

            output.append(
                f"{club['club']} "
                f"(Score: {club['score']})"
            )

    else:

        output.append("No Better Matches")

    output.append("")
    output.append("OKAY MATCHES ✓")
    output.append("-" * 60)

    if report["okay_matches"]:

        for club in report["okay_matches"]:

            output.append(
                f"{club['club']} "
                f"(Score: {club['score']})"
            )

    else:

        output.append("No Okay Matches")

    output.append("")
    output.append("AICTE STATUS")
    output.append("-" * 60)

    output.append(
        f"Status : {report['aicte_status']['status']}"
    )

    output.append(
        f"Remaining Points : "
        f"{report['aicte_status']['remaining']}"
    )

    output.append("=" * 60)

    return "\n".join(output)