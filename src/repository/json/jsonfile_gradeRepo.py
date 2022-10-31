import json

from src.domain.grade import Grade
from src.repository.inmemory.gradeRepo import GradeRepository


class GradeJsonFileRepository(GradeRepository):
    """
    Class that represents a grade repository that uses json files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for GradeJsonFileRepository class
        :param file_name: path to file for storage
        """
        GradeRepository.__init__(self)
        self.__file_name = file_name

    def __read_from_file(self):
        """
        Reads lines from the grades file and converts them into Grade objects
        """
        f = open(self.__file_name, "r")
        self._grade_data.clear()
        grades = json.loads(f.read())
        for grade in grades:
            gr = Grade(int(grade["assignment_id"]), int(grade["student_id"]), float(grade["grade_value"]))
            self._grade_data.append(gr)
        f.close()

    def __write_all_to_file(self):
        """
        Saves all grades to file
        """
        f = open(self.__file_name, "w")
        grades = []
        for grade in self._grade_data:
            grade = {"assignment_id": grade.assignment_id, "student_id": grade.student_id, "grade_value": grade.grade_value}
            grades.append(grade)
        json.dump(grades, f)
        f.close()

    def get_all_grades(self):
        """
        Gets all grades from the file
        """
        self.__read_from_file()
        return GradeRepository.get_all_grades(self)

    def search_by_student_id(self, stud_id):
        """
        Searches a grade by given student ID (stud_id)
        :param stud_id: ID of the student, integer
        :return: Grade if found
        """
        self.__read_from_file()
        return GradeRepository.search_by_student_id(self, stud_id)

    def search_by_assignment_id(self, assign_id):
        """
        Searches a grade by given assignment ID (assign_id)
        :param assign_id: integer
        :return: Grade if found
        """
        self.__read_from_file()
        return GradeRepository.search_by_assignment_id(self, assign_id)

    def search_student_and_assignment(self, student_id, assignment_id):
        """
        Searches a grade by given student ID and assignment ID
        :param student_id: ID of the student, integer
        :param assignment_id: ID of the assignment, integer
        :return: Grade if found
        """
        self.__read_from_file()
        return GradeRepository.search_student_and_assignment(self, student_id, assignment_id)

    def add_grade(self, new_grade):
        """
        Adds a new student to the list of grades
        :param new_grade: a new grade, Grade
        """
        self.__read_from_file()
        GradeRepository.add_grade(self, new_grade)
        self.__write_all_to_file()

    def remove_grade(self, grade):
        """
        Removes an certain grade from the list of grades
        :param grade: grade to be removed, Grade
        """
        self.__read_from_file()
        GradeRepository.remove_grade(self, grade)
        self.__write_all_to_file()

    def remove_grade_with_student_id(self, student_id):
        """
        Removes a grade by student ID (student_id) from the list of grades
        :param student_id: ID of the student, integer
        """
        self.__read_from_file()
        GradeRepository.remove_grade_with_student_id(self, student_id)
        self.__write_all_to_file()

    def remove_grade_with_assignment_id(self, assignment_id):
        """
        Removes a grade by assignment ID (assignment_id) from the list of grades
        :param assignment_id: ID of the assignment, integer
        """
        self.__read_from_file()
        GradeRepository.remove_grade_with_assignment_id(self, assignment_id)
        self.__write_all_to_file()

    def update_grade(self, assignment_id, student_id):
        """
        Removes the grade value from a grade by resetting the value to -1
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        """
        self.__read_from_file()
        GradeRepository.update_grade(self, assignment_id, student_id)
        self.__write_all_to_file()

    def repo_grade_student(self, assignment_id, student_id, grade_value):
        """
        Grades a student with <grade_value>, given student and assignment IDs
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        :param grade_value: value of the grade, integer
        """
        self.__read_from_file()
        GradeRepository.repo_grade_student(self, assignment_id, student_id, grade_value)
        self.__write_all_to_file()

