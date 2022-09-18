from domain.grade import Grade
from repository.inmemory.gradeRepo import GradeRepository
import pickle
import random
import os


class GradeBinFileRepository(GradeRepository):
    """
    Class that represents a grade repository that uses binary files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for GradeBinFileRepository class
        :param file_name: path to file for storage
        """
        GradeRepository.__init__(self)
        self.__file_name = file_name
        self.generate_grades_list()

    def __read_from_file(self):
        """
        Reads lines from the grades file and converts them into Grade objects
        """
        f = open(self.__file_name, "rb")
        try:
            self._grade_data = pickle.load(f)
        except EOFError:
            pass
        f.close()

    def __write_all_to_file(self):
        """
        Saves all grades to file
        """
        f = open(self.__file_name, "wb")
        pickle.dump(self._grade_data, f)
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

    @staticmethod
    def generate_grade_value():
        """
        Procedurally generates an integer or a float with exactly two non-zero decimals
        :return: string
        """
        grade_int = random.randint(1, 10)
        if int(grade_int) != 10:
            grade_dec = random.randint(0, 99)
            if int(grade_dec) < 10:
                grade_dec = "0" + str(grade_dec)
            grade_dec = "." + str(grade_dec)
            if grade_dec == ".00":
                grade_dec = ""
        else:
            grade_dec = ""

        return str(grade_int) + str(grade_dec)

    def generate_grades_list(self):
        filesize = os.path.getsize(self.__file_name)
        if filesize == 0:
            for i in range(1, 21):
                student_id = random.randint(1, 20)
                grade_value = self.generate_grade_value()
                grade = Grade(int(i), int(student_id), grade_value)
                self.add_grade(grade)

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
