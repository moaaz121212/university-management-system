import tkinter as tk
from tkinter import ttk, messagebox

# ========== Data Classes ==========
class Person:
    def __init__(self, name, id_number):
        self._name = name
        self._id_number = id_number

    def get_info(self):
        return f"Name: {self._name}, ID: {self._id_number}"

class Student(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)
        self._courses = []

    def enroll(self, course):
        if course not in self._courses:
            self._courses.append(course)
            course.add_student(self)

    def get_info(self):
        return super().get_info()

class Professor(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)
        self._courses = []

    def assign_course(self, course):
        self._courses.append(course)
        course.set_professor(self)

    def get_info(self):
        return super().get_info()

class Course:
    def __init__(self, name, code):
        self._name = name
        self._code = code
        self._students = []
        self._professor = None

    def add_student(self, student):
        if student not in self._students:
            self._students.append(student)

    def set_professor(self, professor):
        self._professor = professor

    def get_info(self):
        prof_name = self._professor._name if self._professor else "TBD"
        return f"{self._name} ({self._code}) - Professor: {prof_name}"

    def get_students(self):
        return self._students

class UniversitySystem:
    def __init__(self):
        self.students = []
        self.professors = []
        self.courses = []

    def add_student(self, student):
        self.students.append(student)

    def add_professor(self, professor):
        self.professors.append(professor)

    def add_course(self, course):
        self.courses.append(course)

# ========== GUI ==========
system = UniversitySystem()
root = tk.Tk()
root.title("University Management System")
root.geometry("900x650")
root.configure(bg="#1a1a2e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
style.configure("TNotebook.Tab", background="#0f3460", foreground="white", font=("Helvetica", 11, "bold"), padding=10)
style.map("TNotebook.Tab", background=[("selected", "#e94560")])
style.configure("TLabel", background="#1a1a2e", foreground="white", font=("Segoe UI", 11))
style.configure("TEntry", padding=5, relief="flat")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#e94560", foreground="white")

notebook = ttk.Notebook(root)
notebook.pack(pady=20, expand=True, fill="both")

def create_tab(name):
    tab = ttk.Frame(notebook, style="TFrame")
    notebook.add(tab, text=name)
    return tab

student_tab = create_tab("🧑‍🎓 Students")
professor_tab = create_tab("👩‍🏫 Professors")
course_tab = create_tab("📘 Courses")
assign_tab = create_tab("📌 Assign")
view_tab = create_tab("📊 View")
people_tab = create_tab("👥 People")

# === STUDENT TAB ===
def add_student():
    name = student_name.get()
    sid = student_id.get()
    if name and sid:
        student = Student(name, sid)
        system.add_student(student)
        messagebox.showinfo("Added", f"Student {name} added.")
        student_name.set("")
        student_id.set("")
    else:
        messagebox.showwarning("Missing", "Please fill all fields.")

student_name = tk.StringVar()
student_id = tk.StringVar()
ttk.Label(student_tab, text="Student Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
ttk.Entry(student_tab, textvariable=student_name, width=40).grid(row=0, column=1, padx=10)
ttk.Label(student_tab, text="Student ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(student_tab, textvariable=student_id, width=40).grid(row=1, column=1, padx=10)
ttk.Button(student_tab, text="Add Student", command=add_student).grid(row=2, column=0, columnspan=2, pady=15)

# === PROFESSOR TAB ===
def add_professor():
    name = prof_name.get()
    pid = prof_id.get()
    if name and pid:
        professor = Professor(name, pid)
        system.add_professor(professor)
        messagebox.showinfo("Added", f"Professor {name} added.")
        prof_name.set("")
        prof_id.set("")
    else:
        messagebox.showwarning("Missing", "Please fill all fields.")

prof_name = tk.StringVar()
prof_id = tk.StringVar()
ttk.Label(professor_tab, text="Professor Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
ttk.Entry(professor_tab, textvariable=prof_name, width=40).grid(row=0, column=1, padx=10)
ttk.Label(professor_tab, text="Professor ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(professor_tab, textvariable=prof_id, width=40).grid(row=1, column=1, padx=10)
ttk.Button(professor_tab, text="Add Professor", command=add_professor).grid(row=2, column=0, columnspan=2, pady=15)

# === COURSE TAB ===
def add_course():
    name = course_name.get()
    code = course_code.get()
    if name and code:
        course = Course(name, code)
        system.add_course(course)
        messagebox.showinfo("Added", f"Course {name} added.")
        course_name.set("")
        course_code.set("")
        update_assign_dropdowns()
    else:
        messagebox.showwarning("Missing", "Please fill all fields.")

course_name = tk.StringVar()
course_code = tk.StringVar()
ttk.Label(course_tab, text="Course Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
ttk.Entry(course_tab, textvariable=course_name, width=40).grid(row=0, column=1, padx=10)
ttk.Label(course_tab, text="Course Code:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ttk.Entry(course_tab, textvariable=course_code, width=40).grid(row=1, column=1, padx=10)
ttk.Button(course_tab, text="Add Course", command=add_course).grid(row=2, column=0, columnspan=2, pady=15)

# === ASSIGN PROFESSOR TO COURSE ===
def update_assign_dropdowns():
    prof_menu['values'] = [p._name for p in system.professors]
    course_menu['values'] = [c._name for c in system.courses]

def assign_prof_to_course():
    prof_name = prof_var.get()
    course_name = course_var.get()
    prof = next((p for p in system.professors if p._name == prof_name), None)
    course = next((c for c in system.courses if c._name == course_name), None)
    if prof and course:
        prof.assign_course(course)
        messagebox.showinfo("Assigned", f"{prof_name} assigned to {course_name}")
    else:
        messagebox.showwarning("Invalid", "Please select valid professor and course.")

prof_var = tk.StringVar()
course_var = tk.StringVar()
ttk.Label(assign_tab, text="Select Professor:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
prof_menu = ttk.Combobox(assign_tab, textvariable=prof_var, width=40)
prof_menu.grid(row=0, column=1, padx=10)

ttk.Label(assign_tab, text="Select Course:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
course_menu = ttk.Combobox(assign_tab, textvariable=course_var, width=40)
course_menu.grid(row=1, column=1, padx=10)

ttk.Button(assign_tab, text="Assign", command=assign_prof_to_course).grid(row=2, column=0, columnspan=2, pady=20)

# === VIEW COURSES TAB ===
def show_courses():
    output.delete("1.0", tk.END)
    for course in system.courses:
        output.insert(tk.END, f"📘 {course.get_info()}\n")
        for student in course.get_students():
            output.insert(tk.END, f"   ┗ 👤 {student.get_info()}\n")
        output.insert(tk.END, "-" * 60 + "\n")

ttk.Button(view_tab, text="Show All Courses", command=show_courses).pack(pady=10)
output = tk.Text(view_tab, width=95, height=25, bg="#16213e", fg="#00f5d4", font=("Consolas", 11))
output.pack(padx=15, pady=10)

# === PEOPLE TAB ===
def show_people():
    people_output.delete("1.0", tk.END)
    people_output.insert(tk.END, "👨‍🎓 Students:\n")
    for s in system.students:
        people_output.insert(tk.END, f"  - {s.get_info()}\n")
    people_output.insert(tk.END, "\n👩‍🏫 Professors:\n")
    for p in system.professors:
        people_output.insert(tk.END, f"  - {p.get_info()}\n")

ttk.Button(people_tab, text="Show All People", command=show_people).pack(pady=10)
people_output = tk.Text(people_tab, width=95, height=25, bg="#0f3460", fg="#f0f0f0", font=("Consolas", 11))
people_output.pack(padx=15, pady=10)

root.mainloop()