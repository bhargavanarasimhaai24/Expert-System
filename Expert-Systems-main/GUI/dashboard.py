from tkinter import messagebox, simpledialog
from expert_modules.career import generate_career_report
from expert_modules.analytics import generate_analytics_report
from expert_modules.attendance import generate_attendance_report
from expert_modules.clubs import generate_club_report
from expert_modules.aicte import generate_aicte_report
from expert_modules.library import generate_library_report
from expert_modules.faculty import generate_faculty_report

from expert_modules.holiday import (
    analyze_specific_date,
    suggest_from_start_date,
    find_best_leave_plan,
    format_plan
)

import tkinter as tk
from data.students import students


class Dashboard:

    def __init__(self, usn):

        self.usn = usn
        self.student = students[usn]

        self.root = tk.Tk()

        self.root.title("Student Expert System Dashboard")
        self.root.geometry("900x900")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Student Expert System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # ----------------------------------
        # Student Details Frame
        # ----------------------------------

        info_frame = tk.LabelFrame(
            self.root,
            text="Student Profile",
            padx=10,
            pady=10
        )

        info_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            info_frame,
            text=f"Name : {self.student['name']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"USN : {self.usn}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Branch : {self.student['branch']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Semester : {self.student['semester']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Section : {self.student['section']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"CGPA : {self.student['cgpa']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"CIE Total : {self.student['cie_total']}/50",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"AICTE Points : {self.student['aicte_points']}",
            font=("Arial", 11)
        ).pack(anchor="w")

        # ----------------------------------
        # Expert Modules
        # ----------------------------------

        modules_frame = tk.LabelFrame(
            self.root,
            text="Expert Modules",
            padx=10,
            pady=10
        )

        modules_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        tk.Button(
            modules_frame,
            text="Attendance Advisor",
            width=30,
            height=2,
            command=self.attendance_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="Club Recommender",
            width=30,
            height=2,
            command=self.club_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="AICTE Advisor",
            width=30,
            height=2,
            command=self.aicte_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="Faculty Availability",
            width=30,
            height=2,
            command=self.faculty_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="Library Advisor",
            width=30,
            height=2,
            command=self.library_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="Holiday Planner",
            width=30,
            height=2,
            command=self.holiday_module
        ).pack(pady=8)
        tk.Button(
            modules_frame,
            text="Career Guidance",
            width=30,
            height=2,
            command=self.career_module
        ).pack(pady=8)

        tk.Button(
            modules_frame,
            text="Dashboard Analytics",
            width=30,
            height=2,
            command=self.analytics_module
        ).pack(pady=8)
        
        tk.Button(
            modules_frame,
            text="Logout",
            width=30,
            height=2,
            bg="red",
            fg="white",
            command=self.root.destroy
        ).pack(pady=20)

    # ----------------------------------
    # Placeholder Functions
    # ----------------------------------

    def attendance_module(self):

        report = generate_attendance_report(self.usn)

        self.show_report_window(
            "📈 Attendance Advisor",
            report
        )

    def club_module(self):

        report = generate_club_report(self.usn)

        self.show_report_window("🏆 Club Recommender", report)

    def aicte_module(self):

        report = generate_aicte_report(self.usn)

        self.show_report_window("🎯 AICTE Advisor",report)

    def faculty_module(self):

        faculty_name = simpledialog.askstring(
            "Faculty Availability",
            "Enter Faculty Name"
        )

        if not faculty_name:
            return

        report = generate_faculty_report(
            faculty_name
        )

        self.show_report_window(
            "Faculty Availability",
            report
        )

    def library_module(self):

        subject = simpledialog.askstring("Library Advisor","Enter Subject:\n IAI / IML / IST / OPS / DAA / MML")

        if not subject:
            return

        report = generate_library_report(self.usn,subject.upper())

        self.show_report_window("📚 Library Advisor", report)
        
    def holiday_module(self):
        window = tk.Toplevel(self.root)

        window.title("Holiday Planner")
        window.geometry("500x350")

        mode = tk.IntVar(value=1)

        tk.Label(
            window,
            text="Choose Holiday Planner Mode",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Radiobutton(
            window,
            text="📅 Analyze Particular Date",
            variable=mode,
            value=1
        ).pack(anchor="w", padx=30)

        tk.Radiobutton(
            window,
            text="🗓 Suggest From Start Date",
            variable=mode,
            value=2
        ).pack(anchor="w", padx=30)

        tk.Radiobutton(
            window,
            text="🏖 Find Best Leave Plan",
            variable=mode,
            value=3
        ).pack(anchor="w", padx=30)

        def run_option():

            try:

                if mode.get() == 1:

                    date = simpledialog.askstring(
                        "Date",
                        "Enter date (YYYY-MM-DD)"
                    )

                    if not date:
                        return

                    result = analyze_specific_date(
                        self.usn,
                        date
                    )

                    report = format_plan(result)

                    self.show_report_window(
                        "Holiday Analysis",
                        report
                    )

                elif mode.get() == 2:

                    date = simpledialog.askstring(
                        "Start Date",
                        "Enter start date (YYYY-MM-DD)"
                    )

                    if not date:
                        return

                    desired_days = int(
                        simpledialog.askstring(
                            "Vacation Length",
                            "Enter desired vacation days:"
                        )
                    )

                    plans = suggest_from_start_date(
                        self.usn,
                        date,
                        desired_days
                    )

                    report = ""

                    for plan in plans:
                        report += format_plan(plan)
                        report += "\n\n"

                    self.show_report_window(
                        "Leave Suggestions",
                        report
                    )

                else:

                    days = simpledialog.askinteger(
                        "Vacation Days",
                        "Enter required vacation days"
                    )

                    if not days:
                        return

                    plans = find_best_leave_plan(
                        self.usn,
                        days
                    )

                    report = ""

                    for plan in plans:
                        report += format_plan(plan)
                        report += "\n\n"

                    self.show_report_window(
                        "Best Leave Plans",
                        report
                    )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

        tk.Button(
            window,
            text="Generate Report",
            command=run_option
        ).pack(pady=20)

    def show_report_window(self,title,report):

        window = tk.Toplevel(self.root)

        window.title(title)

        window.geometry("900x600")

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)

        scrollbar.pack(
            side="right",
            fill="y"
        )

        text = tk.Text(
            frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Consolas", 11)
        )

        text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=text.yview
        )

        text.insert("1.0", report)

        text.config(state="disabled")
    
    def career_module(self):

        report = generate_career_report(
            self.usn
        )

        self.show_report_window(
            "Career Guidance",
            report
        )


    def analytics_module(self):

        report = generate_analytics_report(
            self.usn
        )

        self.show_report_window(
            "Dashboard Analytics",
            report
        )
    
    def run(self):
        self.root.mainloop()