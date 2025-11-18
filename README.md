# CheckMyGradeApp
This app is an intuitive, onsole-based Python application designed to manage and track student academic performance efficiently. Leveraging object-oriented programming principles, it enables professors and students to interact seamlessly with course information and academic records.
  
   UML Class Diagram:
   
![UML Class Diagram](UML_Class_Diagram.jpg)

Features

  Student Management:
    Add, modify, delete, and view student details, courses, grades, and marks.
    
  Professor Management:
    Create and manage professor profiles and course assignments.
    
  Course Management:
    Add, update, and delete course information, including course ID, credits, and descriptions.
    
   User Authentication:
    Secure login with a simple encryption/decryption method to protect passwords stored in CSV files.
    
  Statistical Analysis:
    Generate detailed statistics, including average, median, minimum, and maximum marks per course.
    
   Robust Unit Testing:
    Comprehensive unit tests ensure correct functionality and reliability.
    
   Chatbot: CheckMyGrade Chatbot assist you in managing and exploring your academic records effortlessly. Whether you're a student wanting to check your grades or a professor managing courses and student progress👋:
    
       View and update student records.
       Add or manage courses and professor assignments.
       Securely log in and manage your profile.


   Technologies Used

    Python 3.x  
    CSV Files:   Persistent data storage
    Encryption/Decryption:  SHA256 + Simple reversible method for password protection
    Unittest Framework:   Comprehensive testing of functionalities



Class Structure

   All classes listed explicitly with attributes and methods clearly defined.
   Static classes properly labeled (CSVHandler, LoginUser).

   No Inheritance Relationship 
   
        (No IS A)

   Composition Relationship (Has A)

        CheckMyGradeApp → Student, Professor, Course


   Aggregation Relationship 

         Course → Student (1 → *)

         Professor → Course (1 → *)

   Dependency Relationship (Dashed lines)
       CSVHandler dependencies: Student, Professor, Course, Grade, CheckMyGradeApp
         
       LoginUser dependency: CheckMyGradeApp
         
      Grade dependency: CheckMyGradeApp
      
  Multiplicity (Cardinality)
  
       One-to-One (1:1): LoginUser ↔ Student, LoginUser ↔ Professor
      
      One-to-Many (1:*): Course → Students, Professor → Courses
      

   Author
    Soroor Ghandali   
© CheckMyGrade 
 
