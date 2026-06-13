from datetime import datetime, timedelta

from data.students import students
from data.holidays import ALL_HOLIDAY_DAYS
from data.timetable import timetable


SAFE_THRESHOLD = 85
MIN_THRESHOLD = 75


# =====================================================
# BASIC HELPERS
# =====================================================

def get_student(usn):
    return students.get(usn)

def date_to_day(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A")

def is_holiday(date_str):

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    if date_obj.weekday() >= 5:
        return True

    return date_str in ALL_HOLIDAY_DAYS

def get_holiday_reason(date_str):

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    if date_obj.weekday() == 5:
        return "Saturday"

    if date_obj.weekday() == 6:
        return "Sunday"

    return ALL_HOLIDAY_DAYS.get(date_str)

# =====================================================
# ATTENDANCE SIMULATION
# =====================================================

def simulate_leave(student, leave_dates):

    impact = {}
    total_penalty = 0

    affected_subjects = {}

    for leave_date in leave_dates:

        day_name = date_to_day(leave_date)

        if day_name not in timetable:
            continue

        for subject in timetable[day_name]:

            affected_subjects[subject] = (
                affected_subjects.get(subject, 0) + 1
            )

    final_status = "SAFE"

    for subject, missed_classes in affected_subjects.items():

        if subject not in student["attendance"]:
            continue

        attended = student["attendance"][subject]["attended"]
        conducted = student["attendance"][subject]["conducted"]

        before = (attended / conducted) * 100

        new_conducted = conducted + missed_classes

        after = (attended / new_conducted) * 100

        penalty = before - after

        total_penalty += penalty

        impact[subject] = {
            "before": round(before, 2),
            "after": round(after, 2),
            "penalty": round(penalty, 2)
        }

        if after < MIN_THRESHOLD:
            final_status = "NOT RECOMMENDED"

        elif after < SAFE_THRESHOLD:
            if final_status != "NOT RECOMMENDED":
                final_status = "CAUTION"

    return {
        "status": final_status,
        "penalty": round(total_penalty, 2),
        "impact": impact
    }


# =====================================================
# HOLIDAY CLUSTERING
# =====================================================

def get_connected_holidays(date_str):

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    cluster = []

    current = date_obj - timedelta(days=1)

    while is_holiday(current.strftime("%Y-%m-%d")):

        cluster.insert(
            0,
            current.strftime("%Y-%m-%d")
        )

        current -= timedelta(days=1)

    cluster.append(date_str)

    current = date_obj + timedelta(days=1)

    while is_holiday(current.strftime("%Y-%m-%d")):

        cluster.append(
            current.strftime("%Y-%m-%d")
        )

        current += timedelta(days=1)

    return cluster


# =====================================================
# VACATION SCORE
# =====================================================

def calculate_vacation_score(
        vacation_days,
        penalty,
        status):

    score = vacation_days * 2

    score -= penalty

    if status == "SAFE":
        score += 3

    elif status == "CAUTION":
        score += 1

    return round(score, 2)


# =====================================================
# OPTION 1
# PARTICULAR DATE ANALYSIS
# =====================================================

def analyze_specific_date(usn, date_str):

    student = get_student(usn)

    if not student:
        return None

    simulation = simulate_leave(
        student,
        [date_str]
    )

    cluster = get_connected_holidays(date_str)

    vacation_days = len(cluster)

    score = calculate_vacation_score(
        vacation_days,
        simulation["penalty"],
        simulation["status"]
    )

    return {
        "type": "PARTICULAR_DATE",
        "leave_dates": [date_str],
        "vacation_days": vacation_days,
        "connected_days": cluster,
        "attendance": simulation,
        "vacation_score": score
    }


# =====================================================
# OPTION 2
# START DATE BASED
# =====================================================

def suggest_from_start_date(
        usn,
        start_date,
        desired_days,
        search_days=60):

    student = get_student(usn)

    if not student:
        return None

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    plans = []

    current = start

    while current <= start + timedelta(days=search_days):

        date_str = current.strftime("%Y-%m-%d")

        if is_holiday(date_str):

            cluster = get_connected_holidays(
                date_str
            )

            cluster_start = datetime.strptime(
                cluster[0],
                "%Y-%m-%d"
            )

            if cluster_start < start:

                current += timedelta(days=1)
                continue

            leave_dates = []

            temp = start

            while temp < cluster_start:

                temp_str = temp.strftime(
                    "%Y-%m-%d"
                )

                if not is_holiday(temp_str):

                    leave_dates.append(
                        temp_str
                    )

                temp += timedelta(days=1)

            vacation_days = (
                len(leave_dates)
                + len(cluster)
            )

            simulation = simulate_leave(
                student,
                leave_dates
            )

            plans.append({

                "leave_dates":
                    leave_dates,

                "connected_days":
                    cluster,

                "vacation_days":
                    vacation_days,

                "attendance":
                    simulation,

                "vacation_score":
                    calculate_vacation_score(
                        vacation_days,
                        simulation["penalty"],
                        simulation["status"]
                    )
            })

        current += timedelta(days=1)

    if not plans:
        return []

    recommended = [

        p for p in plans

        if p["attendance"]["status"]
           != "NOT RECOMMENDED"
    ]

    if not recommended:
        recommended = plans

    # PLAN 1 : Closest to desired days

    best_match = min(

        recommended,

        key=lambda p: (

            abs(
                p["vacation_days"]
                - desired_days
            ),

            p["attendance"]["penalty"]
        )
    )

    # PLAN 2 : Safer (less vacation)

    smaller_plans = [

        p for p in recommended

        if p["vacation_days"]
           < desired_days
    ]

    if smaller_plans:

        safer_plan = max(

            smaller_plans,

            key=lambda p: (

                p["vacation_days"],
                -p["attendance"]["penalty"]
            )
        )

    else:

        safer_plan = best_match

    # PLAN 3 : Extended (more vacation)

    larger_plans = [

        p for p in recommended

        if p["vacation_days"]
           > desired_days
    ]

    if larger_plans:

        extended_plan = min(

            larger_plans,

            key=lambda p: (

                p["vacation_days"],
                p["attendance"]["penalty"]
            )
        )

    else:

        extended_plan = best_match

    result = []

    for plan in [
        best_match,
        safer_plan,
        extended_plan
    ]:

        if plan not in result:

            result.append(plan)

    return result


# =====================================================
# OPTION 3
# REQUIRED VACATION DAYS
# =====================================================

def find_best_leave_plan(
        usn,
        required_vacation_days):

    student = get_student(usn)

    if not student:
        return None

    start = datetime(2026, 1, 1)
    end = datetime(2026, 12, 31)

    plans = []

    current = start

    while current <= end:

        date_str = current.strftime(
            "%Y-%m-%d"
        )

        if not is_holiday(date_str):

            cluster = get_connected_holidays(
                date_str
            )

            vacation_days = len(cluster)

            if vacation_days >= required_vacation_days:

                simulation = simulate_leave(
                    student,
                    [date_str]
                )

                plans.append({

                    "leave_dates": [date_str],

                    "vacation_days":
                        vacation_days,

                    "connected_days":
                        cluster,

                    "attendance":
                        simulation,

                    "vacation_score":
                        calculate_vacation_score(
                            vacation_days,
                            simulation["penalty"],
                            simulation["status"]
                        )
                })

        current += timedelta(days=1)

    plans.sort(
        key=lambda x: (

            x["attendance"]["status"]
                == "NOT RECOMMENDED",

            x["attendance"]["penalty"],

            -x["vacation_days"]
        )
    )

    return plans[:3]


# =====================================================
# REPORT GENERATOR
# =====================================================

def format_plan(plan):

    output = []

    output.append("=" * 50)

    output.append(
        f"Vacation Days : {plan['vacation_days']}"
    )

    output.append(
        f"Status        : "
        f"{plan['attendance']['status']}"
    )

    output.append(
        f"Penalty       : "
        f"{plan['attendance']['penalty']:.2f}"
    )

    output.append(
        f"Score         : "
        f"{plan['vacation_score']}"
    )

    output.append("")

    output.append("Leave Dates:")

    for d in plan["leave_dates"]:
        output.append(f"  {d}")

    output.append("")

    output.append("Connected Holidays:")

    for d in plan["connected_days"]:

        reason = get_holiday_reason(d)

        if reason:
            output.append(
                f"  {d} -> {reason}"
            )
        else:
            output.append(f"  {d}")

    output.append("")

    output.append("Attendance Impact")

    for subject, data in (
            plan["attendance"]["impact"]
            .items()
    ):

        output.append(

            f"{subject}: "
            f"{data['before']}% -> "
            f"{data['after']}% "
            f"(Penalty {data['penalty']}%)"
        )

    output.append("=" * 50)

    return "\n".join(output)