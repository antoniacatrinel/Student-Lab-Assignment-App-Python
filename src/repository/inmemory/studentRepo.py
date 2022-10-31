from src.domain.student import Student
from src.exceptions.exceptions import RepositoryError
from src.utils.utils import IterableStructure


class StudentRepository:
    """
    Class that represents a student repository
    """
    def __init__(self):
        """
        Constructor for the StudentRepository class
        """
        self._student_data = IterableStructure()

    def get_all_students(self):
        """
        :return: the list of all students
        """
        return self._student_data

    def search_by_id(self, stud_id):
        """
        Searches a student by given ID (stud_id)
        :param stud_id: ID of searched student, integer
        :return: Student if found
        :raises: RepositoryError in case of nonexistent student
        """
        ok = True
        for _stud in self._student_data:
            if int(_stud.student_id) == int(stud_id):
                return _stud

        if ok:
            raise RepositoryError("Nonexistent student id!\n")

    def add_student(self, new_student):
        """
        Adds a new student to the list of students
        :param new_student: a new student, Student
        :raises: RepositoryError in case of already existent student
        """
        for _stud in self._student_data:
            if int(_stud.student_id) == int(new_student.student_id):
                raise RepositoryError("Duplicate student id!\n")

        self._student_data.append(new_student)

    def remove_student_by_id(self, stud_id):
        """
        Removes a student by ID (stud_id) from the list of students
        :param stud_id: ID of the student, integer
        """
        for i in range(len(self._student_data)):
            _stud = self._student_data[i]
            if int(_stud.student_id) == int(stud_id):
                self._student_data.__delitem__(i)
                return

    def update_student_name(self, stud_id, new_name):
        """
        Updates the name of the student having ID <stud_id> with <new_name>
        :param stud_id: ID of the student, integer
        :param new_name: new name, string
        :raises: RepositoryError in case of nonexistent student
        """
        ok = False
        for i in range(len(self._student_data)):
            _stud = self._student_data[i]
            if int(_stud.student_id) == int(stud_id):
                new_stud = Student(stud_id, new_name, _stud.group)
                self._student_data.__setitem__(i, new_stud)            # or setattr(stud, 'name', new_name) - builtins
                ok = True

        if ok is False:
            raise RepositoryError("Nonexistent student id!\n")

    def update_student_group(self, stud_id, new_group):
        """
        Updates the group of the student having ID <stud_id> with <new_group>
        :param stud_id: ID of the student,integer
        :param new_group: new group, integer
        :raises: RepositoryError in case of nonexistent student
        """
        ok = False
        for i in range(len(self._student_data)):
            _stud = self._student_data[i]
            if int(_stud.student_id) == int(stud_id):
                new_stud = Student(stud_id, _stud.name, new_group)
                self._student_data.__setitem__(i, new_stud)          # or setattr(stud, 'group', new_group) - builtins
                ok = True

        if ok is False:
            raise RepositoryError("Nonexistent student id!\n")
