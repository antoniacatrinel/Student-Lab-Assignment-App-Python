from domain.grade import Grade
from exceptions.exceptions import RepositoryError
from utils.utils import IterableStructure


class GradeRepository:
    """
    Class that represents a grade repository
    """
    def __init__(self):
        """
        Constructor for GradeRepository class
        """
        self._grade_data = IterableStructure()

    def get_all_grades(self):
        """
        :return: the list of all grades
        """
        return self._grade_data

    def add_grade(self, new_grade):
        """
        Adds a new student to the list of grades
        :param new_grade: a new grade, Grade
        :raises: RepositoryError in case of already existent grade
        """
        for _grade in self._grade_data:
            if int(_grade.assignment_id) == int(new_grade.assignment_id) and int(_grade.student_id) == int(new_grade.student_id):
                raise RepositoryError("Duplicate grade!\n")
        self._grade_data.append(new_grade)

    def update_grade(self, assignment_id, student_id):
        """
        Removes the grade value from a grade by resetting the value to -1
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        """
        ok = True
        for _grade in self._grade_data:
            if int(_grade.assignment_id) == int(assignment_id) and int(_grade.student_id) == int(student_id):
                _grade.grade_value = float(-1)
                return
        if ok:
            raise RepositoryError("Nonexistent grade!\n")

    def remove_grade(self, grade):
        """
        Removes an certain grade from the list of grades
        :param grade: grade to be removed, Grade
        """
        ok = True
        for i in range(len(self._grade_data)):
            _grade = self._grade_data[i]
            if int(_grade.assignment_id) == int(grade.assignment_id) and int(_grade.student_id) == int(grade.student_id):
                self._grade_data.__delitem__(i)
                return
        if ok:
            raise RepositoryError("Nonexistent grade!\n")

    def search_by_student_id(self, stud_id):
        """
        Searches a grade by given student ID (stud_id)
        :param stud_id: ID of the student, integer
        :return: Grade if found
        :raises: RepositoryError in case of nonexistent student id
        """
        ok = True
        for _grade in self._grade_data:
            if int(_grade.student_id) == int(stud_id):
                return _grade
        if ok:
            raise RepositoryError("Nonexistent student id!\n")

    def search_by_assignment_id(self, assign_id):
        """
        Searches a grade by given assignment ID (assign_id)
        :param assign_id: integer
        :return: Grade if found
        :raises: RepositoryError in case of nonexistent assignment id
        """
        ok = True
        for _grade in self._grade_data:
            if int(_grade.assignment_id) == int(assign_id):
                return _grade
        if ok:
            raise RepositoryError("Nonexistent assignment id!\n")

    def search_student_and_assignment(self, student_id, assignment_id):
        """
        Searches a grade by given student ID and assignment ID
        :param student_id: ID of the student, integer
        :param assignment_id: ID of the assignment, integer
        :return: Grade if found
        :raises: RepositoryError in case of nonexistent assignment id in student's list of ungraded assignments
        """
        ok = True
        for _grade in self._grade_data:
            if int(_grade.student_id) == int(student_id) and int(_grade.assignment_id) == int(assignment_id):
                return _grade
        if ok:
            raise RepositoryError("Nonexistent assignment id in student's ungraded assignments!\n")

    def remove_grade_with_student_id(self, student_id):
        """
        Removes a grade by student ID (student_id) from the list of grades
        :param student_id: ID of the student, integer
        """
        for i in range(len(self._grade_data)):
            _grade = self._grade_data[i]
            if int(_grade.student_id) == int(student_id):
                self._grade_data.__delitem__(i)
                return

    def remove_grade_with_assignment_id(self, assignment_id):
        """
        Removes a grade by assignment ID (assignment_id) from the list of grades
        :param assignment_id: ID of the assignment, integer
        """
        for i in range(len(self._grade_data)):
            _grade = self._grade_data[i]
            if int(_grade.assignment_id) == int(assignment_id):
                self._grade_data.__delitem__(i)
                return

    def repo_grade_student(self, assignment_id, student_id, grade_value):
        """
        Grades a student with <grade_value>, given student and assignment IDs
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        :param grade_value: value of the grade, integer
        """
        for i in range(len(self._grade_data)):
            _grade = self._grade_data[i]
            if int(_grade.student_id) == int(student_id) and int(_grade.assignment_id) == int(assignment_id):
                new_grade = Grade(assignment_id, student_id, float(grade_value))
                self._grade_data.__setitem__(i, new_grade)
