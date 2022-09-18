import mysql.connector
from repository.inmemory.gradeRepo import GradeRepository
from domain.grade import Grade


class GradeDatabaseRepository(GradeRepository):
    """
    Class that represents a grade repository that uses a database for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for GradeDatabaseRepository class
        :param file_name: path to file for storage
        """
        GradeRepository.__init__(self)
        self.connection = mysql.connector.connect(host='localhost', user='root', password='1234', port='3306', database=file_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS grades (assignment_id INTEGER PRIMARY KEY, student_id INTEGER PRIMARY KEY, grade_value INTEGER)""")
        self.connection.commit()

    @property
    def students(self):
        self.cursor.execute('SELECT * FROM grades;')
        grades = self.cursor.fetchall()
        return [Grade(g[0], g[1], g[2]) for g in grades]

    def search_by_assignment_id(self, assignment_id):
        self.cursor.execute('SELECT * FROM grades WHERE assignment_id=%s;', (assignment_id,))
        grades = self.cursor.fetchall()
        if len(grades) == 0:
            return None
        self._grade_data = [Grade(g[0], g[1], g[2]) for g in grades]
        return [Grade(g[0], g[1], g[2]) for g in grades][0]

    def search_by_student_id(self, student_id):
        self.cursor.execute('SELECT * FROM grades WHERE student_id=%s;', (student_id,))
        grades = self.cursor.fetchall()
        if len(grades) == 0:
            return None
        self._grade_data = [Grade(g[0], g[1], g[2]) for g in grades]
        return [Grade(g[0], g[1], g[2]) for g in grades][0]

    def search_student_and_assignment(self, student_id, assignment_id):
        self.cursor.execute('SELECT * FROM grades WHERE student_id=%s AND assignment_id=%s;', (student_id, assignment_id))
        grades = self.cursor.fetchall()
        if len(grades) == 0:
            return None
        self._grade_data = [Grade(g[0], g[1], g[2]) for g in grades]
        return [Grade(g[0], g[1], g[2]) for g in grades][0]

    def add_grade(self, new_grade):
        self.cursor.execute(
            'INSERT INTO `student_lab_assignment_database`.`grades` (`assignment_id`,`student_id`,`grade_value`) VALUES (%s, %s, %s);',
            (new_grade.assignment_id, new_grade.student_id, new_grade.grade_value))
        GradeRepository.add_grade(self, new_grade)
        self.connection.commit()

    def remove_grade(self, grade):
        self.cursor.execute('DELETE FROM grades WHERE student_id=%s AND assignment_id=%s;', (grade.student_id, grade.assignment_id))
        GradeRepository.remove_grade(self, grade)
        self.connection.commit()

    def remove_grade_with_student_id(self, student_id):
        self.cursor.execute('DELETE FROM grades WHERE student_id=%s;', (student_id,))
        GradeRepository.remove_grade_with_student_id(self, student_id)
        self.connection.commit()

    def remove_grade_with_assignment_id(self, assignment_id):
        self.cursor.execute('DELETE FROM grades WHERE assignment_id=%s;', (assignment_id, ))
        GradeRepository.remove_grade_with_assignment_id(self, assignment_id)
        self.connection.commit()

    def update_grade(self, assignment_id, student_id):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`grades` SET `grade_value`= %s, WHERE `student_id`= %s AND `assignment_id`= %s;', (-1, student_id, assignment_id))
        GradeRepository.update_grade(self, assignment_id, student_id)
        self.connection.commit()

    def repo_grade_student(self, assignment_id, student_id, grade_value):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`grades` SET `grade_value`= %s, WHERE `student_id`= %s AND `assignment_id`= %s;', (grade_value, student_id, assignment_id))
        GradeRepository.repo_grade_student(self, assignment_id, student_id, grade_value)
        self.connection.commit()
