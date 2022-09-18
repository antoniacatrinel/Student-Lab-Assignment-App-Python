# Student Lab Assignment Application

Write an application that manages student lab assignments for a discipline. The application will store the following entities:
- **Student**: `student_id`, `name`, `group`
- **Assignment**: `assignment_id`, `description`, `deadline`
- **Grade**: `assignment_id`, `student_id`, `grade_value`

Create an application that allows to:
1. Manage students and assignments. The user can add, remove, update, and list both students and assignments.
2. Give assignments to a student or a group of students. In case an assignment is given to a group of students, every student in the group will receive it. In case there are students who were previously given that assignment, it will not be assigned again.
3. Grade student for a given assignment. When grading, the program must allow the user to select the assignment that is graded, from the student’s list of ungraded assignments. A student’s grade for a given assignment cannot be changed. Deleting a student removes their assignments. Deleting an assignment also removes all grades at that assignment.
4. Create statistics:
    - All students who received a given assignment, ordered descending by grade.
    - All students who are late in handing in at least one assignment. These are all the students who have an ungraded assignment for which the deadline has passed.
    - Students with the best school situation, sorted in descending order of the average grade received for all graded assignments.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations must cascade and have a memory-efficient implementation.
6. Create a Python module that contains an iterable data structure, a sort method and a filter method, together with complete PyUnit unit tests (100% coverage). 
7. Implement persistent storage for all entities using file-based repositories: one using text files for storage, one using binary files (using object serialization with Pickle) and one using JSON files. The decision of which repositories are employed, as well as the location of the repository input files will be made in the program’s settings.properties file. Create a Settings class into which you load the data from the settings.properties file. Then, the application start module decides which modules are started by examining the settings object. This further decouples the properties input file from the application.
8. Implement a database-backed SQL repository.
9. Implement a graphical user interface, in addition to the required menu-driven UI. Program can be started with either UI, without changing the source code.
10. Implement PyUnit test cases, with 95% unit test code coverage for all modules except the UI.
