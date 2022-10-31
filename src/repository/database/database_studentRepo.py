import mysql.connector

from src.repository.inmemory.studentRepo import StudentRepository
from src.domain.student import Student


class StudentDatabaseRepository(StudentRepository):
    """
    Class that represents a student repository that uses a database for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for StudentDatabaseRepository class
        :param file_name: path to file for storage
        """
        StudentRepository.__init__(self)
        self.connection = mysql.connector.connect(host='localhost', user='root', password='1234', port='3306', database=file_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students (student_id INT PRIMARY KEY)""")  # , name VARCHAR(30), group INT)""")
        self.connection.commit()

    @property
    def students(self):
        self.cursor.execute('SELECT * FROM students;')
        students = self.cursor.fetchall()
        return [Student(s[0], s[1], s[2]) for s in students]

    def search_by_id(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE student_id=%s;', (student_id,))
        students = self.cursor.fetchall()
        if len(students) == 0:
            return None
        self._student_data = [Student(s[0], s[1], s[2]) for s in students]
        return [Student(s[0], s[1], s[2]) for s in students][0]

    def add_student(self, new_student):
        self.cursor.execute(
            'INSERT INTO `student_lab_assignment_database`.`students` (`student_id`,`name`,`group`) VALUES (%s, %s, %s);',
            (new_student.student_id, new_student.name, new_student.group))
        StudentRepository.add_student(self, new_student)
        self.connection.commit()

    def remove_student_by_id(self, stud_id):
        self.cursor.execute('DELETE FROM students WHERE student_id=%s;', (stud_id,))
        StudentRepository.remove_student_by_id(self, stud_id)
        self.connection.commit()

    def update_student_name(self, stud_id, new_name):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`students` SET `name`= %s, WHERE `student_id`= %s;', (new_name, stud_id))
        StudentRepository.update_student_name(self, stud_id, new_name)
        self.connection.commit()

    def update_student_group(self, stud_id, new_group):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`students` SET `group`= %s, WHERE `student_id`= %s;', (new_group, stud_id))
        StudentRepository.update_student_group(self, stud_id, new_group)
        self.connection.commit()
