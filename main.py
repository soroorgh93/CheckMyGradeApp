import csv
import time
import hashlib
from datetime import datetime

class CSVHandler:
    @staticmethod
    def load_data(filename):
        try:
            with open(filename, 'r') as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            return []

    @staticmethod
    def save_data(filename, data, fieldnames):
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def load_students():
        return CSVHandler.load_data('students.csv')

    @staticmethod
    def save_students(students):
        CSVHandler.save_data('students.csv', students, 
                           ['Email address', 'First name', 'Last name', 'Course.id', 'grades', 'Marks'])

    @staticmethod
    def load_courses():
        return CSVHandler.load_data('courses.csv')

    @staticmethod
    def save_courses(courses):
        CSVHandler.save_data('courses.csv', courses, 
                           ['Course_id', 'Course_name', 'Credits', 'Description'])

    @staticmethod
    def load_professors():
        return CSVHandler.load_data('professors.csv')

    @staticmethod
    def save_professors(professors):
        CSVHandler.save_data('professors.csv', professors, 
                           ['Professor_id', 'Professor Name', 'Rank', 'Course.id'])

    @staticmethod
    def load_login():
        return CSVHandler.load_data('login.csv')


    @staticmethod
    def save_login(login_data):
        CSVHandler.save_data('login.csv', login_data, 
                           ['User id', 'Password', 'password_without_hashing', 'Role'])
class Grade:
    grade_ranges = [
        {"grade_id": 1, "grade": "A", "min": 90, "max": 100},
        {"grade_id": 2, "grade": "B", "min": 80, "max": 89},
        {"grade_id": 3, "grade": "C", "min": 70, "max": 79},
        {"grade_id": 4, "grade": "D", "min": 60, "max": 69},
        {"grade_id": 5, "grade": "F", "min": 0, "max": 59}
    ]

    @classmethod
    def calculate_grade(cls, marks):
        for gr in cls.grade_ranges:
            if gr["min"] <= marks <= gr["max"]:
                return gr["grade"]
        return "F"

    @staticmethod
    def display_grade_report(email):
        start_time = time.time()
        students = CSVHandler.load_students()
        target = next((s for s in students if s['Email address'] == email), None)
        
        if not target:
            print("Student not found!")
            return

        course_id = target['Course.id']
        course_students = [s for s in students if s['Course.id'] == course_id]
        marks = [int(s['Marks']) for s in course_students]
        
        print(f"\nStudent: {target['First name']} {target['Last name']}")
        print(f"Course: {course_id}, Grade: {target['grades']}, Marks: {target['Marks']}")
        print(f"Min Marks: {min(marks)}, Max Marks: {max(marks)}")
        print(f"Report generated in {time.time() - start_time:.6f} seconds")

    @staticmethod
    def get_course_statistics(course_id):
        start_time = time.time()
        students = CSVHandler.load_students()
        marks = [int(s['Marks']) for s in students if s['Course.id'] == course_id]
        
        if not marks:
            print("No students found for this course!")
            return 0, 0, 0

        avg = sum(marks) / len(marks)
        sorted_marks = sorted(marks)
        median = sorted_marks[len(sorted_marks)//2]
        Min = min(sorted_marks)
        Max = max(sorted_marks)
        elapsed = time.time() - start_time
        
        print(f"\nCourse Statistics for {course_id}:")
        print(f"Average Marks: {avg:.2f}")
        print(f"Median Marks: {median}")
        print(f"Minimum Marks: {Min}")
        print(f"Maximum Marks: {Max}")
        print(f"Generated in {elapsed:.6f} seconds")
        return avg, median, elapsed

class Student:
    def __init__(self, app):
        self.app = app

    def display_records(self, email):
        students = CSVHandler.load_students()
        student = next((s for s in students if s['Email address'] == email), None)
        if student:
            print("\nStudent Record:")
            for key, value in student.items():
                print(f"{key}: {value}")
        else:
            print("Student not found!")

    def add_new_student(self):
        email = input("Enter student email: ")
        if any(s['Email address'] == email for s in CSVHandler.load_students()):
            print("Student already exists!")
            return

        first = input("First name: ")
        last = input("Last name: ")
        course = input("Course ID: ")
        marks = int(input("Marks (0-100): "))
        grade = Grade.calculate_grade(marks)

        new_student = {
            'Email address': email,
            'First name': first,
            'Last name': last,
            'Course.id': course,
            'grades': grade,
            'Marks': marks
        }

        students = CSVHandler.load_students()
        students.append(new_student)
        CSVHandler.save_students(students)

        # Add to login
        LoginUser.add_to_login(email, "student")
        print("Student added successfully!")


    def delete_new_student(self, email):
        students = CSVHandler.load_students()
        students = [s for s in students if s['Email address'] != email]
        CSVHandler.save_students(students)
        print("Student deleted successfully!")
        
    def update_student_record(self, email):
        students = CSVHandler.load_students()
        student = next((s for s in students if s['Email address'] == email), None)
        if not student:
            print("Student not found!")
            return

        print("\nUpdate options:")
        print("1. First name")
        print("2. Last name")
        print("3. Course ID")
        print("4. Marks")
        choice = input("Select field to update: ")

        if choice == '1':
            student['First name'] = input("New first name: ")
        elif choice == '2':
            student['Last name'] = input("New last name: ")
        elif choice == '3':
            student['Course.id'] = input("New course ID: ")
        elif choice == '4':
            marks = int(input("New marks: "))
            student['Marks'] = marks
            student['grades'] = Grade.calculate_grade(marks)
        else:
            print("Invalid choice!")
            return

        CSVHandler.save_students(students)
        print("Record updated successfully!")

class Course:
    def __init__(self, app):
        self.app = app
        
    @staticmethod
    def get_available_courses():
        courses = CSVHandler.load_courses()
        return [c['Course_id'] for c in courses]

    @staticmethod
    def select_course():
        courses = Course.get_available_courses()
        if not courses:
            print("No courses available!")
            return None
        print("\nAvailable Courses:")
        for idx, c in enumerate(courses, 1):
            print(f"{idx}. {c}")
        choice = int(input("Select course number: ")) - 1
        return courses[choice] if 0 <= choice < len(courses) else None
        
    def display_courses(self):
        courses = CSVHandler.load_courses()
        print("\nAvailable Courses:")
        for course in courses:
            print(f"{course['Course_id']}: {course['Course_name']} ({course['Credits']} credits)")

    def add_new_course(self):
        course_id = input("Course ID: ")
        if any(c['Course_id'] == course_id for c in CSVHandler.load_courses()):
            print("Course already exists!")
            return

        name = input("Course name: ")
        credits = input("Credits: ")
        desc = input("Description: ")

        courses = CSVHandler.load_courses()
        courses.append({
            'Course_id': course_id,
            'Course_name': name,
            'Credits': credits,
            'Description': desc
        })
        CSVHandler.save_courses(courses)
        print("Course added successfully!")

    def delete_new_course(self, course_id):
        courses = CSVHandler.load_courses()
        courses = [c for c in courses if c['Course_id'] != course_id]
        CSVHandler.save_courses(courses)
        print("Course deleted successfully!")

class Professor:
    def __init__(self, app):
        self.app = app
        
    def modify_professor_course(self, email):
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == email), None)
        if not prof:
            print("Professor not found!")
            return

        while True:
            print("\n1. Select existing course")
            print("2. Create new course")
            print("3. Cancel")
            choice = input("Choose option: ")

            if choice == '1':
                course_id = Course.select_course()
                if course_id:
                    prof['Course.id'] = course_id
                    CSVHandler.save_professors(professors)
                    print("Course assignment updated!")
                return

            elif choice == '2':
                self.app.course.add_new_course()
                
                new_courses = CSVHandler.load_courses()
                if new_courses:
                    prof['Course.id'] = new_courses[-1]['Course_id']
                    CSVHandler.save_professors(professors)
                    print("Automatically assigned to new course!")
                return

            elif choice == '3':
                return
            else:
                print("Invalid choice!")
                
    def professors_details(self, professor_id):
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == professor_id), None)
        if prof:
            print("\nProfessor Details:")
            for key, value in prof.items():
                print(f"{key}: {value}")
        else:
            print("Professor not found!")

    def add_new_professor(self):
        email = input("Professor email: ")
        if any(p['Professor_id'] == email for p in CSVHandler.load_professors()):
            print("Professor already exists!")
            return

        name = input("Full name: ")
        rank = input("Rank (Junior/Senior/Associate): ")
        course = input("Course ID: ")

        professors = CSVHandler.load_professors()
        professors.append({
            'Professor_id': email,
            'Professor Name': name,
            'Rank': rank,
            'Course.id': course
        })
        CSVHandler.save_professors(professors)

        # Add to login
        LoginUser.add_to_login(email, "professor")
        print("Professor added successfully!")

    def delete_professor(self, professor_id):
        professors = CSVHandler.load_professors()
        professors = [p for p in professors if p['Professor_id'] != professor_id]
        CSVHandler.save_professors(professors)
        print("Professor deleted successfully!")

    def show_course_details_by_professor(self, professor_id):
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == professor_id), None)
        if not prof:
            print("Professor not found!")
            return

        course_id = prof['Course.id']
        courses = CSVHandler.load_courses()
        course = next((c for c in courses if c['Course_id'] == course_id), None)
        if course:
            print("\nCourse Details:")
            for key, value in course.items():
                print(f"{key}: {value}")
        else:
            print("Course not found!")
    def update_professor_course(self, email):
        courses = Course.get_available_courses()
        if not courses:
            print("No courses available! Create courses first.")
            return

        print("\nAvailable Courses:")
        for c in courses:
            print(f"- {c}")
            
        new_course = input("Enter course ID from list above: ")
        if new_course not in courses:
            print("Invalid course selection!")
            return

        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == email), None)
        if prof:
            prof['Course.id'] = new_course
            CSVHandler.save_professors(professors)
            print("Course assignment updated!")





            
class LoginUser:
    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    @staticmethod
    def add_to_login(email, role):
        login_data = CSVHandler.load_login()
        if not any(user['User id'] == email for user in login_data):
            login_data.append({
                'User id': email,
                'Password': LoginUser.encrypt_password("default"),
                'Role': role
            })
            CSVHandler.save_login(login_data)

    @staticmethod
    def register_new_user(email, role):
        # Add to login.csv
        login_data = CSVHandler.load_login()
        if any(user['User id'] == email for user in login_data):
            return False
            
        password = input("Set password for new account: ")
        login_data.append({
            'User id': email,
            'Password': LoginUser.encrypt_password(password),
            'password_without_hashing': password,  
            'Role': role
        })
        CSVHandler.save_login(login_data)
        
        if role == 'student':
            students = CSVHandler.load_students()
            students.append({
                'Email address': email,
                'First name': 'New',
                'Last name': 'Student',
                'Course.id': 'TBD',
                'grades': 'Unavailable',
                'Marks': 'Unavailable'
            })
            CSVHandler.save_students(students)
        elif role == 'professor':
            professors = CSVHandler.load_professors()
            professors.append({
                'Professor_id': email,
                'Professor Name': 'New Professor',
                'Rank': 'Junior',
                'Course.id': 'TBD'
            })
            CSVHandler.save_professors(professors)
            
        return True

    @staticmethod
    def login():
        email = input("Email: ")
        login_data = CSVHandler.load_login()
        user = next((u for u in login_data if u['User id'] == email), None)
        
        if user:
            password = input("Password: ")
            input_hash = LoginUser.encrypt_password(password)
            stored_hash = user['Password']
            plaintext = user['password_without_hashing']
            
            #if input_hash == stored_hash and password == plaintext:
            if input_hash == stored_hash:                
                return user['Role'], email
            print("Invalid password!")
            return None, None
        else:  # New user
            print("New user detected! Let's create an account.")
            while True:
                role = input("Choose role (student/professor): ").lower()
                if role in ['student', 'professor']:
                    break
                print("Invalid role! Please choose student or professor.")
                
            if LoginUser.register_new_user(email, role):
                print("Account created successfully! Please login again.")
            else:
                print("Registration failed!")
            return None, None
    @staticmethod
    def change_password(email):
        old_pass = input("Current password: ")
        login_data = CSVHandler.load_login()
        user = next((u for u in login_data if u['User id'] == email), None)
        
        if not user or user['Password'] != LoginUser.encrypt_password(old_pass):
            print("Invalid password!")
            return
            
        new_pass = input("New password: ")
        user['Password'] = LoginUser.encrypt_password(new_pass)
        CSVHandler.save_login(login_data)
        print("Password changed successfully!")
class CheckMyGradeApp:
    def __init__(self):
        self.student = Student(self)
        self.course = Course(self)
        self.professor = Professor(self)
        
    def run(self):
        while True:
            print("\nCheckMyGrade System")
            print("1. Login")
            print("2. Exit")
            choice = input("Select option: ")
            
            if choice == '1':
                role, email = LoginUser.login()
                if role == 'student':
                    self.student_menu(email)
                elif role == 'professor':
                    self.professor_menu(email)
            elif choice == '2':
                break
            else:
                print("Invalid choice!")

    def student_menu(self, email):
        while True:
            print("\nStudent Menu")
            print("1. View Records")
            print("2. Check Grades")
            print("3. Update Record")
            print("4. Change Password")
            print("5. Logout")
            choice = input("Select option: ")
            
            if choice == '1':
                self.student.display_records(email)
            elif choice == '2':
                Grade.display_grade_report(email)
            elif choice == '3':
                self.student.update_student_record(email)
            elif choice == '4':
                LoginUser.change_password(email)
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
    def professor_menu(self, email):
        while True:
            print("\nProfessor Menu")
            print("1. Add Student")
            print("2. Update Student Grades")
            print("3. View Course Details")
            print("4. Show Course Statistics")
            print("5. Delete Student")
            print("6. Change Password")
            print("7. Manage Courses")
            print("8. Logout")
            choice = input("Select option: ")
            
            if choice == '1':
                self.add_student_with_course_validation()
            elif choice == '2':
                self.update_student_grade(email)
            elif choice == '3':
                self.professor.show_course_details_by_professor(email)
            elif choice == '4':
                self.show_course_statistics(email)
            elif choice == '5':
                self.delete_student(email)
            elif choice == '6':
                LoginUser.change_password(email)
            elif choice == '7':
                self.manage_courses_menu(email)           
            elif choice == '8':
                break
            else:
                print("Invalid choice!")
    def update_student_grade(self, professor_email):
        # Get professor's course
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == professor_email), None)
        if not prof or prof['Course.id'] == 'TBD':
            print("You must be assigned to a course first!")
            return
            
        course_id = prof['Course.id']
        student_email = input("Enter student email to update: ")
        
        students = CSVHandler.load_students()
        student = next((s for s in students if s['Email address'] == student_email), None)
        
        if student and student['Course.id'] == course_id:
            new_marks = int(input(f"Enter new marks (0-100) for {student_email}: "))
            student['Marks'] = new_marks
            student['grades'] = Grade.calculate_grade(new_marks)
            CSVHandler.save_students(students)
            print("Grades updated successfully!")
        else:
            print("Student not found in your course!")                
    def manage_courses_menu(self, email):
        while True:
            print("\nCourse Management")
            print("1. Add New Course")
            print("2. Modify Assigned Course")
            print("3. Delete Course")
            print("4. View All Courses")
            print("5. Back")
            choice = input("Select option: ")

            if choice == '1':
                self.course.add_new_course()
            elif choice == '2':
                self.professor.modify_professor_course(email)
            elif choice == '3':
                course_id = Course.select_course()
                if course_id:
                    self.course.delete_new_course(course_id)
            elif choice == '4':
                 self.course.display_courses()
            elif choice == '5':
                return
            else:
                print("Invalid choice!")
    def add_new_course_flow(self):
        self.course.add_new_course()
        
        new_courses = CSVHandler.load_courses()
        if new_courses:
            new_course_id = new_courses[-1]['Course_id']
            print(f"Would you like to assign yourself to {new_course_id}?")
            if input("(Y/N): ").lower() == 'y':
                professors = CSVHandler.load_professors()
                prof = next((p for p in professors if p['Professor_id'] == email), None)
                if prof:
                    prof['Course.id'] = new_course_id
                    CSVHandler.save_professors(professors)
                    print("Course assignment updated!")       
    def show_course_statistics(self, professor_email):
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == professor_email), None)
        if not prof or not prof['Course.id']:
            print("You must be assigned to a course first!")
            return
            
        Grade.get_course_statistics(prof['Course.id'])            

    def delete_student(self, professor_email):
        
        professors = CSVHandler.load_professors()
        prof = next((p for p in professors if p['Professor_id'] == professor_email), None)
        if not prof or not prof['Course.id']:
            print("You must be assigned to a course first!")
            return
        
        student_email = input("Enter student email to delete: ")
        
        # Verify student belongs to professor's course
        students = CSVHandler.load_students()
        student = next((s for s in students if s['Email address'] == student_email and 
                       s['Course.id'] == prof['Course.id']), None)
        
        if student:
            self.student.delete_new_student(student_email)
           
            login_data = CSVHandler.load_login()
            login_data = [u for u in login_data if u['User id'] != student_email]
            CSVHandler.save_login(login_data)
            print("Student completely removed from system!")
        else:
            print("Student not found in your course!")

    def add_student_with_course_validation(self):
        course_id = Course.select_course()
        if not course_id:
            print("Invalid course selection!")
            return

        email = input("Student email: ")
        if any(s['Email address'] == email for s in CSVHandler.load_students()):
            print("Student already exists!")
            return

        first = input("First name: ")
        last = input("Last name: ")
        marks = int(input("Initial marks (0-100): "))
        grade = Grade.calculate_grade(marks)

        new_student = {
            'Email address': email,
            'First name': first,
            'Last name': last,
            'Course.id': course_id,
            'grades': grade,
            'Marks': marks
        }

        students = CSVHandler.load_students()
        students.append(new_student)
        CSVHandler.save_students(students)
        LoginUser.add_to_login(email, "student")
        print("Student added successfully!")

if __name__ == "__main__":
    app = CheckMyGradeApp()
    app.run()
