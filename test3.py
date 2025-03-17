import unittest
from unittest.mock import patch
from main import CheckMyGradeApp, CSVHandler, LoginUser, Grade

class TestCheckMyGradeApp(unittest.TestCase):

    def setUp(self):
        self.app = CheckMyGradeApp()
    def setUp(self):
        self.app = CheckMyGradeApp()
        students = CSVHandler.load_students()
        for student in students:
            if student['Email address'] == 'student_0@mycsu.edu':
                student['First name'] = 'Curtis'  # original name from CSV
        CSVHandler.save_students(students)

    @patch('builtins.input', side_effect=['DATA300', 'Advanced Math', '4', 'Complex concepts'])
    def test_add_new_course_flow(self, mock_input):
        print("\nTesting adding new course...")
        self.app.course.add_new_course()
        courses = CSVHandler.load_courses()
        self.assertTrue(any(c['Course_id'] == 'DATA300' for c in courses))
        print("Course added successfully!")

    @patch('builtins.input', side_effect=['professor_5@mycsu.edu', 'Dr. Grace Hopper', 'Senior Professor', 'DATA300', 'ProfGracePass'])
    def test_add_new_professor(self, mock_input):
        print("\nTesting adding new professor...")
        self.app.professor.add_new_professor()
        professors = CSVHandler.load_professors()
        self.assertTrue(any(p['Professor_id'] == 'professor_5@mycsu.edu' for p in professors))
        print("Professor added successfully!")

    @patch('builtins.input', side_effect=['1', 'student_12@mycsu.edu', 'Alice', 'Wonder', '95'])
    def test_add_student_with_course_validation(self, mock_input):
        print("\nTesting adding new student with validation...")
        self.app.add_student_with_course_validation()
        students = CSVHandler.load_students()
        self.assertTrue(any(s['Email address'] == 'student_12@mycsu.edu' for s in students))
        print("Student added successfully!")

    @patch('builtins.input', side_effect=['ProfPass0', 'NewProfPass123'])
    def test_professor_change_password(self, mock_input):
        print("\nTesting professor password change...")
        LoginUser.change_password('professor_0@mycsu.edu')
        login_data = CSVHandler.load_login()
        prof = next(u for u in login_data if u['User id'] == 'professor_0@mycsu.edu')
        self.assertEqual(prof['Password'], LoginUser.encrypt_password('NewProfPass123'))
        print("Password change successful!")

    @patch('builtins.input', side_effect=['student_0@mycsu.edu', 'StudentPass0'])
    def test_student_login_existing_user(self, mock_input):
        print("\nTesting existing student login...")
        role, email = LoginUser.login()
        self.assertEqual(role, 'student')
        self.assertEqual(email, 'student_0@mycsu.edu')
        print("Existing student login successful!")

    @patch('builtins.input', side_effect=['newstudent@mycsu.edu', 'student', 'NewStudentPass'])
    def test_student_new_registration(self, mock_input):
        print("\nTesting new student registration...")
        role, email = LoginUser.login()
        self.assertIsNone(role)
        login_data = CSVHandler.load_login()
        self.assertTrue(any(u['User id'] == 'newstudent@mycsu.edu' for u in login_data))
        print("Student registration completed successfully!")

    @patch('builtins.input', side_effect=['1', 'student_updated_again'])
    def test_update_student_first_name(self, mock_input):
        print("\nTesting student updating first name...")
        before_students = CSVHandler.load_students()
        before_name = next(s for s in before_students if s['Email address'] == 'student_0@mycsu.edu')['First name']
        self.app.student.update_student_record('student_0@mycsu.edu')
        after_students = CSVHandler.load_students()
        after_name = next(s for s in after_students if s['Email address'] == 'student_0@mycsu.edu')['First name']
        self.assertNotEqual(before_name, after_name)
        print(f"Student first name updated from {before_name} to {after_name}")

    def test_professor_show_course_statistics(self):
        print("\nTesting professor showing course statistics...")
        self.app.show_course_statistics('professor_0@mycsu.edu')

    def test_student_view_records(self):
        print("\nTesting student viewing records...")
        self.app.student.display_records('student_0@mycsu.edu')

if __name__ == '__main__':
    unittest.main()
