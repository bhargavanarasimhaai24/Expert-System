from datetime import datetime

from data.faculty import faculty


def time_to_minutes(time_str):

    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute


def generate_faculty_report(name):

    selected_faculty = None

    for _, data in faculty.items():

        if data["name"].lower() == name.lower():

            selected_faculty = data
            break

    if not selected_faculty:
        return "Faculty not found."

    now = datetime.now()

    day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    current_minutes = time_to_minutes(current_time)

    college_start = time_to_minutes("08:00")
    college_end = time_to_minutes("16:45")

    today_classes = selected_faculty["schedule"].get(day, [])

    output = []

    output.append("=" * 60)
    output.append("FACULTY AVAILABILITY REPORT")
    output.append("=" * 60)

    output.append(f"Faculty Name : {selected_faculty['name']}")
    output.append(f"Subject      : {selected_faculty['subject']}")
    output.append(f"Cabin        : {selected_faculty['cabin']}")
    output.append(f"Current Day  : {day}")
    output.append(f"Current Time : {current_time}")

    output.append("")
    output.append("CURRENT STATUS")
    output.append("-" * 60)

    # Before working hours
    if current_minutes < college_start:

        output.append("Not Available Now ❌")
        output.append("")
        output.append(
            "College working hours have not started yet."
        )

        output.append("")
        output.append("=" * 60)

        return "\n".join(output)

    # After working hours
    if current_minutes >= college_end:

        output.append("Not Available Now ❌")
        output.append("")
        output.append(
            "College working hours are over."
        )

        output.append("")
        output.append("=" * 60)

        return "\n".join(output)

    in_class = False

    for start, end, room in today_classes:

        start_minutes = time_to_minutes(start)
        end_minutes = time_to_minutes(end)

        if start_minutes <= current_minutes < end_minutes:

            in_class = True
            break

    # Faculty free now
    if not in_class:

        output.append("Available Now ✅")
        output.append("")
        output.append(
            "Faculty is currently available in cabin."
        )

        output.append("")
        output.append("=" * 60)

        return "\n".join(output)

    # Faculty busy
    output.append("Not Available Now ❌")
    output.append("")
    output.append(
        "Faculty is currently taking a class."
    )

    output.append("")
    output.append("NEXT AVAILABLE CABIN SLOTS")
    output.append("-" * 60)

    free_slots = []

    classes_sorted = sorted(
        today_classes,
        key=lambda x: time_to_minutes(x[0])
    )

    current = college_start

    for start, end, room in classes_sorted:

        start_minutes = time_to_minutes(start)
        end_minutes = time_to_minutes(end)

        if current < start_minutes:

            free_slots.append(
                (
                    current,
                    start_minutes
                )
            )

        current = end_minutes

    if current < college_end:

        free_slots.append(
            (
                current,
                college_end
            )
        )

    upcoming_slots = []

    for start, end in free_slots:

        if end > current_minutes:

            actual_start = max(
                start,
                current_minutes
            )

            upcoming_slots.append(
                (
                    actual_start,
                    end
                )
            )

    if upcoming_slots:

        for start, end in upcoming_slots:

            output.append(
                f"• {start//60:02d}:{start%60:02d}"
                f" - "
                f"{end//60:02d}:{end%60:02d}"
            )

    else:

        output.append(
            "No more free slots available today."
        )

    output.append("")
    output.append("TODAY'S SCHEDULE")
    output.append("-" * 60)

    if not today_classes:

        output.append(
            "No classes scheduled today."
        )

    else:

        for start, end, room in today_classes:

            output.append(
                f"{start} - {end} | {room}"
            )

    output.append("")
    output.append("=" * 60)

    return "\n".join(output)