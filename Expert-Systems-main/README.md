# Student Expert System

An intelligent, rule-based Student Expert System built with **Python** and **Tkinter**. This desktop application serves as a multi-module advisory portal to assist students with academics, attendance monitoring, club selection, AICTE points tracking, real-time faculty availability checking, library resources, and vacation planning.

---

## 📌 Problem Statement
Academic environments present students with numerous complex decisions and monitoring tasks, such as:
- Keeping track of attendance constraints to avoid falling below mandatory thresholds.
- Navigating career choices based on CGPA, academic performance, and personal interests.
- Finding optimal time slots to meet faculty advisors in their cabins without clashes.
- Planning vacations/holleaves while mathematically predicting and minimizing the impact on course attendance.
- Identifying and participating in co-curricular/extra-curricular clubs to satisfy AICTE point milestones.
- Selecting appropriate textbooks and reference materials based on their academic strengths.

The **Student Expert System** addresses these issues by offering an automated, rules-based intelligence agent that processes student profiles, schedules, timetables, and rules to provide real-time recommendations and insights.

---

## 🚀 Key Features & Enhancements

### 1. 💼 Career Guidance Expert
- Analyzes student interests, CGPA, CIE scores, and coding levels (Beginner, Intermediate, Advanced).
- Suggests professional career pathways (e.g., ML Engineer, Software Developer, Researcher).
- Recommends a curated set of technical and soft skills to prioritize.

### 2. 🕒 Faculty Availability Expert (Recent Enhancement)
- Integrates with the local system date and time.
- Predicts whether a faculty member is currently in a class or available in their cabin.
- Computes **next available cabin slots** for the day if the faculty is busy.
- Displays the faculty member's schedule, designation, contact info, and current cabin room number.

### 3. 🏖️ Intelligent Holiday Planning Expert (Recent Enhancement)
- Uses multiple sophisticated recommendation strategies:
  1. **Analyze Specific Date**: Evaluates the attendance penalty if a student takes leave on a chosen date.
  2. **Suggest From Start Date**: Recommends short, balanced, or extended plans matching desired vacation length.
  3. **Find Best Leave Plan**: Scans the annual calendar to locate optimal leave dates that produce minimum attendance penalties.
- Simulates how missed classes would affect each subject's attendance and warns the user with status alerts (**SAFE**, **CAUTION**, **NOT RECOMMENDED**).

### 4. 📊 Student Analytics Dashboard
- Aggregates CIE performance, CGPA, AICTE points progress, and average attendance.
- Displays an overview of attendance across all subjects, identifying the student's strongest and weakest courses.
- Generates expert insights regarding academic risk and AICTE completion status.

### 5. 📈 Attendance Analysis
- Compiles current attendance states and checks them against the **75% condonation** and **85% safe** thresholds.
- Provides actionable, subject-wise advice to improve or maintain attendance.

### 6. 🎓 Academic & Club Recommendation (AICTE & Library)
- **Club Recommender**: Maps student goals to co-curricular/extra-curricular clubs, prioritizing those with higher AICTE points.
- **Library Advisor**: Recommends appropriate textbooks and reference books tailored to the student's current academic level (**WEAK**, **AVERAGE**, or **STRONG**).

---

## 📁 Project Structure

```text
Student_Expert_System/
│
├── main.py                     # App entry point (controls login & dashboard orchestration)
│
├── GUI/                        # User Interface Layer
│   ├── login.py                # Tkinter Login Window (USN verification)
│   └── dashboard.py            # Main Dashboard GUI displaying student profile and modules
│
├── expert_modules/             # Rule-Based Inference Engines
│   ├── aicte.py                # AICTE points analysis and club recommendations
│   ├── analytics.py            # Overview dashboard analytics generator
│   ├── attendance.py           # Attendance shortage warnings and warnings advisor
│   ├── career.py               # Rules for career roadmap and skill suggestions
│   ├── clubs.py                # Interest-matching score algorithm for clubs
│   ├── faculty.py              # Time-based faculty cabin/class availability analyzer
│   ├── holiday.py              # Leave simulation and optimal vacation planner
│   └── library.py              # Subject book levels recommendation engine
│
└── data/                       # Mock Knowledge Bases
    ├── books.py                # Subject textbooks and reference library database
    ├── clubs.py                # Catalog of BMSCE co-curricular/extra-curricular clubs
    ├── faculty.py              # Faculty schedules, cabins, and contact catalog
    ├── holidays.py             # Annual calendar list of national/local holidays
    ├── students.py             # Registered student profile and academic metrics
    └── timetable.py            # Weekly subject schedule mapping for simulation
```

---

## 🛠️ Technologies Used
- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (Standard Library)
- **Date & Time Processing**: Datetime module
- **Testing/Linting**: PyCompile, Glob

---

## 💻 Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/saicharanraju2005/Expert-Systems.git
   cd Expert-Systems
   ```

2. **Verify Python Installation**:
   Ensure you have Python 3 installed:
   ```bash
   python --version
   ```

3. **Run the Application**:
   Since the app uses standard Python GUI packages (Tkinter), no external dependencies are strictly required. You can launch the system directly:
   ```bash
   python main.py
   ```

---

## 📖 Usage Instructions

1. **Login**:
   - Run the app to open the login window.
   - Enter a registered student USN (e.g., `1BM24AI001` or `1BM24AI002` from `data/students.py`) and click **Login**.

2. **Dashboard**:
   - Once logged in, view your student profile (Name, USN, CGPA, CIE Total, AICTE Points).
   - Click on any of the advisory buttons to trigger the corresponding expert module.

3. **Holiday Planner**:
   - Choose a mode (Analyze Date, Suggest Leaves, Find Best Plan).
   - Input dates in `YYYY-MM-DD` format to get an automated report showing simulated attendance penalty impact.

4. **Faculty Availability**:
   - Search for a faculty member (e.g., `Dr. Priyanka` or `Prof. Amitha S` from `data/faculty.py`).
   - Get immediate feedback on whether they are in their cabin right now, along with upcoming free windows.

---


