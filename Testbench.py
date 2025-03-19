import unittest
from unittest.mock import patch
from TOPMODULE import CheckMyGradeApp, CSVHandler, LoginUser, Grade
import time

class TestCheckMyGradeApp(unittest.TestCase):

    def setUp(self):
        self.app = CheckMyGradeApp()

    # Add two Professors 
    @patch('builtins.input', side_effect=[
        'prof_test@mycsu.edu', 'Dr. Test Prof', 'Senior', '1', # assuming DATA200 is the first course
        'prof_test2@mycsu.edu', 'Dr. SecondTest', 'Junior', '2' # assuming MATH101 is second
    ])
    def test_add_two_professors(self, mock_input):
        print("\nTesting adding two professors...")
        self.app.professor.add_new_professor()
        self.app.professor.add_new_professor()

        professors = CSVHandler.load_professors()
        login_data = CSVHandler.load_login()

        self.assertTrue(any(p['Professor_id'] == 'prof_test@mycsu.edu' for p in professors))
        self.assertTrue(any(p['Professor_id'] == 'prof_test2@mycsu.edu' for p in professors))
        self.assertTrue(any(u['User id'] == 'prof_test@mycsu.edu' for u in login_data))
        self.assertTrue(any(u['User id'] == 'prof_test2@mycsu.edu' for u in login_data))
    @patch('builtins.input', side_effect=[
        'student_test1@mycsu.edu', 'Test1', 'User1', '1', '95',  # DATA200
        'student_test2@mycsu.edu', 'Test2', 'User2', '2', '88'   # MATH101
    ])
    def test_add_two_students(self, mock_input):
        print("\nTesting adding two students...")
        self.app.student.add_new_student()
        self.app.student.add_new_student()

        students = CSVHandler.load_students()
        login_data = CSVHandler.load_login()

        self.assertTrue(any(s['Email address'] == 'student_test1@mycsu.edu' for s in students))
        self.assertTrue(any(s['Email address'] == 'student_test2@mycsu.edu' for s in students))
        self.assertTrue(any(u['User id'] == 'student_test1@mycsu.edu' for u in login_data))
        self.assertTrue(any(u['User id'] == 'student_test2@mycsu.edu' for u in login_data))
    # Delete only one professor
    def test_delete_one_professor(self):
        print("\nTesting deleting professor 'prof_test@mycsu.edu'...")
        self.app.professor.delete_professor('prof_test@mycsu.edu')

        professors = CSVHandler.load_professors()
        login_data = CSVHandler.load_login()

        self.assertFalse(any(p['Professor_id'] == 'prof_test@mycsu.edu' for p in professors))
        self.assertFalse(any(u['User id'] == 'prof_test@mycsu.edu' for u in login_data))
    # Add new course
    @patch('builtins.input', side_effect=['TEST100', 'Test Course', '3', 'Test Description'])
    def test_add_new_course(self, mock_input):
        print("\nTesting adding new course (TEST100)...")
        self.app.course.add_new_course()
        courses = CSVHandler.load_courses()
        self.assertTrue(any(c['Course_id'] == 'TEST100' for c in courses))

    # Delete course
    def test_delete_course(self):
        print("\nTesting deleting course 'TEST100'...")
        self.app.course.delete_new_course('TEST100')
        courses = CSVHandler.load_courses()
        self.assertFalse(any(c['Course_id'] == 'TEST100' for c in courses))

    # Modify Course
    @patch('builtins.input', side_effect=['TEST200', 'Original Course', '4', 'Original Description'])
    def test_modify_course(self, mock_input):
        print("\nTesting modifying course 'TEST200'...")
        self.app.course.add_new_course()
        courses = CSVHandler.load_courses()
        course = next(c for c in courses if c['Course_id'] == 'TEST200')
        course['Course_name'] = 'Modified Course'
        CSVHandler.save_courses(courses)
        updated_courses = CSVHandler.load_courses()
        updated_course = next(c for c in updated_courses if c['Course_id'] == 'TEST200')
        self.assertEqual(updated_course['Course_name'], 'Modified Course')

    # Delete only one Student
    def test_delete_one_student(self):
        print("\nTesting deleting student 'student_test1@mycsu.edu'...")
        self.app.student.delete_new_student('student_test1@mycsu.edu')

        students = CSVHandler.load_students()
        login_data = CSVHandler.load_login()

        self.assertFalse(any(s['Email address'] == 'student_test1@mycsu.edu' for s in students))
        self.assertFalse(any(u['User id'] == 'student_test1@mycsu.edu' for u in login_data))

    # Check existing professor login
    @patch('builtins.input', side_effect=['professor_0@mycsu.edu', 'ProfPass123', 'professor'])
    def test_existing_professor_login(self, mock_input):
        print("\nTesting existing professor login...")
        role, email = LoginUser.login()
        self.assertEqual(role, 'professor')

    # Existing student login
    @patch('builtins.input', side_effect=['student_0@mycsu.edu', 'StudentPass123', 'student'])
    def test_existing_student_login(self, mock_input):
        print("\nTesting existing student login...")
        role, email = LoginUser.login()
        self.assertEqual(role, 'student')

   
    def test_professor_course_statistics(self):
        print("\nTesting professor course statistics...")
        start_time = time.time()
        self.app.show_course_statistics('professor_0@mycsu.edu')
        print(f"Statistics timing: {time.time() - start_time:.6f} seconds")

    # Student records timing
    def test_student_records_timing(self):
        print("\nTesting viewing student records timing...")
        start_time = time.time()
        self.app.student.display_records('student_0@mycsu.edu')
        print(f"Displaying records took {(time.time() - start_time):.6f} seconds")

    # Sorting Student Records with Timing
    def test_sort_students_by_marks_email_timing(self):
        print("\nTesting sorting student records...")
        students = CSVHandler.load_students()
        students_valid = [s for s in students if s['Marks'].isdigit()]

        start = time.time()
        sorted_marks_asc = sorted(students_valid, key=lambda x: int(x['Marks']))
        print(f"Sorting by marks ascending took {time.time() - start:.6f} seconds")

        start = time.time()
        sorted_email_asc = sorted(students, key=lambda x: x['Email address'])
        print(f"Sorted by email ascending in {(time.time()-start):.6f} seconds")
    # Encrypt/Decrypt Password
    def test_encryption_decryption_password(self):
        print("\nTesting encryption/decryption for 'student_0@mycsu.edu'...")
        LoginUser.display_encrypted_and_decrypted_password('student_0@mycsu.edu')
    # Modify Professor Course
    @patch('builtins.input', side_effect=['DATA300'])
    def test_modify_professor_course(self, mock_input):
        print("\nTesting modifying course assignment for 'professor_0@mycsu.edu'...")
        self.app.professor.update_professor_course('professor_0@mycsu.edu')
        professors = CSVHandler.load_professors()
        prof = next(p for p in professors if p['Professor_id'] == 'professor_0@mycsu.edu')
        self.assertEqual(prof['Course.id'], 'DATA300')
    # Modify Professor Details
    def test_modify_professor_details(self):
        print("\nTesting modifying professor details for 'professor_0@mycsu.edu'...")
        professors = CSVHandler.load_professors()
        prof = next(p for p in professors if p['Professor_id'] == 'professor_0@mycsu.edu')
        old_rank = prof['Rank']
        prof['Rank'] = 'Associate'
        CSVHandler.save_professors(professors)
        updated_professors = CSVHandler.load_professors()
        updated_prof = next(p for p in updated_professors if p['Professor_id'] == 'professor_0@mycsu.edu')
        self.assertEqual(updated_prof['Rank'], 'Associate')

    # Modify Student Record
    @patch('builtins.input', side_effect=['1', 'UpdatedName'])
    def test_modify_student_record(self, mock_input):
        print("\nTesting modifying student 'student_0@mycsu.edu' first name...")
        self.app.student.update_student_record('student_0@mycsu.edu')
        students = CSVHandler.load_students()
        student = next(s for s in students if s['Email address'] == 'student_0@mycsu.edu')
        self.assertEqual(student['First name'], 'UpdatedName')

if __name__ == '__main__':
    unittest.main()
