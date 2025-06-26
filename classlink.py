import turtle
from datetime import date

# Data Storage
pupil_records = {
    "P1001": "Alex Brown",
    "P1002": "Sam Wilson",
    "P1003": "Taylor Green"
}
attendance_log = {
    str(date.today()): [("P1001", "here"), ("P1002", "absent"), ("P1003", "here")]
}
class_work = ["Math Test", "Science Project", "Reading Assignment"]
grade_book = {
    "P1001": {"Math Test": "88", "Science Project": "92"},
    "P1002": {"Math Test": "72", "Science Project": "68"},
    "P1003": {"Math Test": "58", "Science Project": "62"}
}

# Helper Functions
def show_options(menu_items):
    border = "»" * 35
    print(f"\n{border}")
    for idx, item in enumerate(menu_items, 1):
        print(f"{idx}. {item}")
    print(border)

def compute_grades(pid):
    marks = [int(score) for score in grade_book.get(pid, {}).values()]
    return round(sum(marks)/len(marks), 1) if marks else 0.0

def identify_struggling():
    return [(pid, pupil_records[pid]) for pid in pupil_records if compute_grades(pid) < 65]

# Core Features
def register_pupil():
    print("\n«« Add New Pupil »»")
    new_id = input("Create pupil ID: ").strip()
    if new_id in pupil_records:
        print("ID already registered!")
        return
    full_name = input("Enter full name: ").strip()
    pupil_records[new_id] = full_name
    print(f"Added {full_name} successfully!")

def mark_attendance():
    current_date = str(date.today())
    if current_date in attendance_log:
        print("Already marked attendance today!")
        return

    print(f"\n«« Attendance for {current_date} »»")
    attendance_log[current_date] = []
    for pid, pname in pupil_records.items():
        status = input(f"{pname} present? (y/n): ").lower()
        while status not in {'y', 'n'}:
            status = input("Please enter y or n: ").lower()
        attendance_log[current_date].append((pid, "here" if status == 'y' else "absent"))
    print("Attendance recorded!")

def enter_scores():
    if not class_work:
        print("No assignments available!")
        return

    print("\nAvailable assignments:")
    for num, work in enumerate(class_work, 1):
        print(f"{num}. {work}")

    try:
        selection = int(input("Choose assignment: ")) - 1
        chosen_work = class_work[selection]
    except (ValueError, IndexError):
        print("Invalid selection!")
        return

    for pid, pname in pupil_records.items():
        while True:
            try:
                points = int(input(f"Score for {pname} (0-100): "))
                if 0 <= points <= 100:
                    grade_book.setdefault(pid, {})[chosen_work] = str(points)
                    break
                else:
                    print("Score must be 0-100!")
            except ValueError:
                print("Numbers only please!")
    print("Scores recorded!")

def create_assignment():
    new_work = input("\nNew assignment name: ").strip()
    if new_work in class_work:
        print("Assignment exists!")
        return
    class_work.append(new_work)
    print(f"Added '{new_work}' to class work!")

# Reports
def display_attendance():
    print("\n«« Attendance Overview »»")
    for day in sorted(attendance_log, reverse=True):
        present = sum(1 for _, stat in attendance_log[day] if stat == "here")
        print(f"{day}: {present} present, {len(pupil_records) - present} absent")

def display_grades():
    print("\n«« Grade Summary »»")
    for pid in pupil_records:
        avg = compute_grades(pid)
        print(f"{pupil_records[pid]} (ID: {pid}): {avg} average")

def display_struggling():
    struggling = identify_struggling()
    print("\n«« Pupils Needing Help »»")
    if not struggling:
        print("All pupils meeting expectations")
    else:
        for pid, pname in struggling:
            avg = compute_grades(pid)
            print(f"{pname} (ID: {pid}) - Current average: {avg}")

# Turtle Dashboard
def draw_interface():
    screen = turtle.Screen()
    screen.title("ClassLink Visual")
    screen.bgcolor("#f5f5f5")
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()
    # Header
    pen.penup()
    pen.goto(-210, 210)
    pen.color("#333366")
    pen.write("Class Management Dashboard", font=("Verdana", 14, "bold"))

    # Data boxes
    draw_data_box(pen, -210, 160, "Pupils", len(pupil_records))
    draw_data_box(pen, -70, 160, "Attendance Days", len(attendance_log))
    draw_data_box(pen, 70, 160, "Assignments", len(class_work))

    # Status boxes
    struggling_count = len(identify_struggling())
    draw_data_box(pen, -140, 60, "Needing Help", struggling_count, "#cc0000")

    if attendance_log:
        recent_day = sorted(attendance_log.keys(), reverse=True)[0]
        present = sum(1 for _, stat in attendance_log[recent_day] if stat == "here")
        draw_data_box(pen, 0, 60, f"Present {recent_day}", present, "#009900")

    turtle.done()  # Keeps window open

def draw_data_box(pen, x, y, label, value, color="#333333"):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)

    # Draw box
    for _ in range(2):
        pen.forward(130)
        pen.right(90)
        pen.forward(90)
        pen.right(90)

    # Label
    pen.penup()
    pen.goto(x + 65, y - 25)
    pen.write(label, align="center", font=("Arial", 9))

    # Value
    pen.goto(x + 65, y - 55)
    pen.write(str(value), align="center", font=("Arial", 12, "bold"))

# Menu Systems
def report_menu():
    while True:
        options = [
            "Attendance Report",
            "Grade Summary",
            "Pupils Needing Help",
            "Return to Main Menu"
        ]
        show_options(options)
        choice = input("Choose report (1-4): ")

        reports = {
            '1': display_attendance,
            '2': display_grades,
            '3': display_struggling,
            '4': lambda: "back"
        }

        action = reports.get(choice)
        if action == "back":
            break
        elif action:
            action()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice!")

def manage_class():
    while True:
        choices = [
            "Register New Pupil",
            "Take Attendance",
            "Create Assignment",
            "Enter Scores",
            "View Reports",
            "Open Dashboard",
            "Quit"
        ]
        show_options(choices)
        selection = input("Choose option (1-7): ")

        actions = {
            '1': register_pupil,
            '2': mark_attendance,
            '3': create_assignment,
            '4': enter_scores,
            '5': report_menu,
            '6': draw_interface,
            '7': lambda: exit("Closing ClassLink...")
        }

        action = actions.get(selection)
        if action:
            action()
        else:
            print("Invalid selection!")

# Start Program
if name == "main":
    print("«« ClassLink Pupil Management System »»")
    manage_class()