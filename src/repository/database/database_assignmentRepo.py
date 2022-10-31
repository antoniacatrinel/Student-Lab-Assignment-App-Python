import mysql.connector

from src.repository.inmemory.assignmentRepo import AssignmentRepository
from src.domain.assignment import Assignment


class AssignmentDatabaseRepository(AssignmentRepository):
    """
    Class that represents an assignment repository that uses a database for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for AssignmentDatabaseRepository class
        :param file_name: path to file for storage
        """
        AssignmentRepository.__init__(self)
        self.connection = mysql.connector.connect(host='localhost', user='root', password='1234', port='3306', database=file_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS assignments (assignment_id INTEGER PRIMARY KEY, description VARCHAR(30),deadline VARCHAR(10))""")
        self.connection.commit()

    @property
    def assignments(self):
        self.cursor.execute('SELECT * FROM assignments;')
        assignments = self.cursor.fetchall()
        return [Assignment(a[0], a[1], a[2]) for a in assignments]

    def search_by_id(self, assignment_id):
        self.cursor.execute('SELECT * FROM assignments WHERE assignment_id=%s;', (assignment_id,))
        assignments = self.cursor.fetchall()
        if len(assignments) == 0:
            return None
        self._assignment_data = [Assignment(a[0], a[1], a[2]) for a in assignments]
        return [Assignment(a[0], a[1], a[2]) for a in assignments][0]

    def add_assignment(self, new_assignment):
        self.cursor.execute('INSERT INTO `student_lab_assignment_database`.`assignments` (`assignment_id`,`description`,`deadline`) VALUES (%s, %s, %s);',
            (new_assignment.assignment_id, new_assignment.description, new_assignment.deadline))
        AssignmentRepository.add_assignment(self, new_assignment)
        self.connection.commit()

    def remove_assignment_by_id(self, assign_id):
        self.cursor.execute('DELETE FROM assignments WHERE assignment_id=%s;', (assign_id,))
        AssignmentRepository.remove_assignment_by_id(self, assign_id)
        self.connection.commit()

    def update_assignment_description(self, assign_id, new_description):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`assignments` SET `description`= %s, WHERE `assignment_id`= %s;', (new_description, assign_id))
        AssignmentRepository.update_assignment_description(self, assign_id, new_description)
        self.connection.commit()

    def update_assignment_deadline(self, assign_id, new_deadline):
        self.cursor.execute('UPDATE `student_lab_assignment_database`.`assignments` SET `deadline`= %s, WHERE `assignment_id`= %s;', (new_deadline, assign_id))
        AssignmentRepository.update_assignment_deadline(self, assign_id, new_deadline)
        self.connection.commit()
