from domain.grade import Grade
from exceptions.exceptions import RepositoryError
import random
from utils.utils import *


class GradeService:
    """
    Service class for the GradeRepository class
    """
    def __init__(self, grade_repo, grade_val, student_repo, assignment_repo):
        """
        Constructor for GradeService class
        :param grade_repo: grade repository
        :param grade_val: grade validator
        :param student_repo: student repository
        :param assignment_repo: assignment repository
        """
        self.__grade_repo = grade_repo
        self.__grade_val = grade_val
        self.__student_repo = student_repo
        self.__assignment_repo = assignment_repo
        self._assignment_to_be_filtered = None
        self._student_to_be_filtered = None

    @property
    def repo(self):
        return self.__grade_repo

    @property
    def grades(self):
        """
        :return: list of all grades from the repository
        """
        return self.__grade_repo.get_all_grades()

    @staticmethod
    def generate_grade_value():
        """
        Procedurally generates an integer or a float with exactly two non-zero decimals.
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
        """
        Generates a list of grades using the existing students and assignments and populates the repository
        :return:
        """
        students_list = self.__student_repo.get_all_students()
        for i in range(1, 21):
            _student = random.choice(students_list)
            student_id = _student.student_id
            grade_value = self.generate_grade_value()
            grade = Grade(int(i), student_id, grade_value)
            self.__grade_repo.add_grade(grade)

    def no_of_grades(self):
        """
        :return: the number of grades currently in the repository
        """
        return len(self.__grade_repo.get_all_grades())

    def remove_student_and_assignments(self, student, student_id, undo_list):
        """
        Function used in cascading remove for undo/redo functionality
        Removes all assignments of that student
        :param student: student, Student
        :param student_id: ID of the student, integer
        :param undo_list: list of reverse operations
        :return: undo_list
        """
        for grade in self.__grade_repo.get_all_grades():
            if int(grade.student_id) == int(student_id):
                self.__grade_repo.remove_grade_with_student_id(student_id)
                undo_list.append(["add_grade", grade])
                self.remove_student_and_assignments(student, student_id, undo_list)  # recall
        return undo_list

    def remove_assignment_and_students(self, assignment, assignment_id, undo_list):
        """
        Function used in cascading remove for undo/redo functionality
        Removes all students that have received that assignment
        :param assignment: assignment, Assignment
        :param assignment_id: ID of the assignment_id, integer
        :param undo_list: list of reverse operations
        :return: undo_list
        """
        for grade in self.__grade_repo.get_all_grades():
            if int(grade.assignment_id) == int(assignment_id):
                self.__grade_repo.remove_grade_with_assignment_id(assignment_id)
                undo_list.append(["add_grade", grade])
                self.remove_assignment_and_students(assignment, assignment_id, undo_list)  # recall
        return undo_list

    def assign_to_student(self, assignment_id, student_id):
        """
        Assigns the assignment with ID <assignment_id> to the student with <student_id>
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        :raises: RepositoryError in case that student already received that assignment
        """
        students = self.__student_repo.get_all_students()
        grades = self.__grade_repo.get_all_grades()
        for _grade in grades:
            if int(_grade.assignment_id) == int(assignment_id) and int(_grade.student_id) == int(student_id):
                raise RepositoryError("Student has already received that assignment!\n")
        for _stud in students:
            if int(_stud.student_id) == int(student_id):
                grade = Grade(assignment_id, student_id)
                self.__grade_val.validate_grade(grade)
                self.__grade_repo.add_grade(grade)

    def assign_to_group(self, assignment_id, group):
        """
        Assigns the assignment with ID <assignment_id> to a group of students <group>
        :param assignment_id: ID of the assignment, integer
        :param group: group of the student, integer
        """
        undo_list = []
        students = self.__student_repo.get_all_students()
        grades = self.__grade_repo.get_all_grades()
        for _student in students:
            if int(_student.group) == int(group):
                ok = True
                try:
                    for _grade in grades:
                        if int(_grade.assignment_id) == int(assignment_id) and int(_grade.student_id) == int(_student.student_id):
                            ok = False
                    if ok is True:        # do not give again same assignment to a student
                        grade = Grade(assignment_id, _student.student_id)
                        self.__grade_val.validate_grade(grade)
                        self.__grade_repo.add_grade(grade)
                        undo_list.append(["give_student", grade])
                except RepositoryError:   # do not raise error
                    continue
        return undo_list

    def grade_student(self, student_id, assignment_id, grade_value):
        """
        Grades a student for a certain assignment
        :param student_id: ID of the student, integer
        :param assignment_id: ID of the assignment, integer
        :param grade_value: value of the grade, integer
        """
        self.__assignment_repo.search_by_id(assignment_id)
        self.__student_repo.search_by_id(student_id)
        grade = Grade(assignment_id, student_id, grade_value)
        self.__grade_val.validate_grade(grade)
        grades = self.__grade_repo.get_all_grades()
        # if grade not in grades:
            # raise RepositoryError("Nonexistent assignment id in student's ungraded assignments!\n")
        self.__grade_repo.repo_grade_student(assignment_id, student_id, grade_value)

    def remove_assign_to_student(self, assignment_id, student_id):
        """
        Removes a certain assignment for a student
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        """
        self.__assignment_repo.search_by_id(assignment_id)
        self.__student_repo.search_by_id(student_id)
        self.__grade_repo.remove_grade(Grade(assignment_id, student_id))

    def remove_assign_to_group(self, assignment_id, group):
        """
        Removes a certain assignment for a group of students
        :param assignment_id: ID of the assignment, integer
        :param group: ID of the student, integer
        """
        self.__assignment_repo.search_by_id(assignment_id)
        ok = True
        while ok is True:
            ok = False
            for _grade in self.__grade_repo.get_all_grades():
                if int(_grade.assignment_id) == int(assignment_id):
                    student = self.__student_repo.search_by_id(_grade.student_id)
                    if int(student.group) == int(group):
                        try:
                            self.__grade_repo.remove_grade(_grade)
                            ok = True
                        except RepositoryError:
                            continue

    def ungrade_student(self, assignment_id, student_id):
        """
        Removes the value of the grade for a student for a certain assignment, by setting it to -1
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        """
        self.__assignment_repo.search_by_id(assignment_id)
        self.__student_repo.search_by_id(student_id)
        self.__grade_repo.update_grade(assignment_id, student_id)

    """
    FUNCTIONS FOR STATISTICS
    """
    @staticmethod
    def order_list_descending_by_grade_float(listt):
        """
        Sorts a list descending by grade, using a lambda function
        :param listt: list to be sorted
        """
        listt.sort(reverse=True, key=lambda x: float(x.get('grade')))

    @staticmethod
    def search_in_list(list_stud, student_id):
        """
        Searches in a given list of students the ID <student_id>
        :param list_stud: list of students, list
        :param student_id: ID of the student, integer
        :return: True if the ID is in the list, False otherwise
        """
        for i in range(0, len(list_stud)):
            if int(list_stud[i]['id']) == int(student_id):
                return True
        return False

    def average_grade_for_student(self, student_id):
        """
        Computes the average grade for a student with ID <student_id>
        :param student_id: ID of the student, integer
        :return: -1 if there are no grades with ID <student_id>
                 the average grade for the student with ID <student_id> at all assignments
        """
        s = 0.0
        nr = 0
        grades = self.__grade_repo.get_all_grades()
        for grade in grades:
            if int(student_id) == int(grade.student_id) and float(grade.grade_value) != -1:
                s += float(grade.grade_value)
                nr += 1
        if nr:
            return float(s / nr)
        return -1

    def filter_assignment(self, grade):
        """
        Filter function used for filtering the assignments with a certain grade
        :param grade: grade, Grade
        :return: True if the grade is for the desired assignment, False otherwise
        """
        return int(grade.assignment_id) == int(self._assignment_to_be_filtered.assignment_id)

    def filter_student(self, grade):
        """
        Filter function used for filtering the student with a certain grade
        :param grade: grade, Grade
        :return: True if the grade is for the desired student, False otherwise
        """
        return int(grade.student_id) == int(self._student_to_be_filtered.student_id)

    def filter_graded_grades_by_student_id(self, student):
        """
        Filter function used for filtering the grades for a certain student
        :param student: student, Student
        :return: list of grades for a certain student
        """
        grades = self.__grade_repo.get_all_grades()
        self._student_to_be_filtered = student
        grades = filter_list(grades, self.filter_student)
        return grades[:]

    def filter_grades_by_assignment_id(self, assignment):
        """
        Filter function used for filtering the grades for a certain assignment
        :param assignment: assignment, Assignment
        :return: list of grades for a certain assignment
        """
        grades = self.__grade_repo.get_all_grades()
        self._assignment_to_be_filtered = assignment
        grades = filter_list(grades, self.filter_assignment)
        return grades[:]

    def count_ungraded_late_assignments_for_student(self, stud_id):
        """
        Counts for the student with ID <stud_id> the number of late assignments (ungraded assignments for which the
        deadline has passed)
        :param stud_id: ID of the student, integer
        :return: number of late assignments, integer
        """
        ungraded = 0
        grades = self.__grade_repo.get_all_grades()
        for grade in grades:
            if int(grade.student_id) == int(stud_id) and float(grade.grade_value) == -1:
                assign_id = grade.assignment_id
                assignment = self.__assignment_repo.search_by_id(assign_id)
                if self.__grade_val.validate_late_deadline(assignment.deadline) is True:
                    ungraded += 1
        return int(ungraded)

    @staticmethod
    def compare_grade_value(student1, student2):
        """
        Compares the grade value of 2 students for an assignment
        :param student1: first student
        :param student2: second student
        :return: True if first grade is greater and False otherwise
        """
        return float(student1.grade_value) >= float(student2.grade_value)

    @staticmethod
    def compare_average_grade_value(student1, student2):
        """
        Compares the average grade of 2 students
        :param student1: first student
        :param student2: second student
        :return: True if first grade is greater and False otherwise
        """
        return float(student1.get('grade')) >= float(student2.get('grade'))

    def create_list_of_given_assignment_ordered(self, assignment_id):
        """
        Creates a sorted list of students who have been given the assignment with ID <assignment_id>
        :param assignment_id: ID of the assignment, integer
        :return: a list of students with late assignments
        """
        self.__assignment_repo.search_by_id(assignment_id)
        assignment = self.__grade_repo.search_by_assignment_id(assignment_id)
        list_given = list(self.filter_grades_by_assignment_id(assignment))
        comb_sort(list_given, self.compare_grade_value)
        return list_given

    def create_list_of_late_students(self):
        """
        Creates a list of students who at least an ungraded assignment for which the deadline has passed
        :return: a list of students with late assignments
        """
        list_late = []
        grades = self.__grade_repo.get_all_grades()
        for grade in grades:
            assign_id = grade.assignment_id
            assignment = self.__assignment_repo.search_by_id(assign_id)
            if self.__grade_val.validate_late_deadline(assignment.deadline) is True and float(grade.grade_value) == -1 and self.search_in_list(list_late, grade.student_id) is False:
                ungraded = self.count_ungraded_late_assignments_for_student(grade.student_id)
                dict_stud = {'id': int(grade.student_id), 'ungraded': int(ungraded)}
                list_late.append(dict_stud)
        return list_late

    def create_list_of_best_school_situation(self):
        """
        Creates a list of students with the best school situation by computing the average grade for each student and then
        sorting the list
        :return: a list of students with the best school situation
        """
        list_best = []
        students = self.__student_repo.get_all_students()
        for student in students:
            student_id = student.student_id
            average_grade = self.average_grade_for_student(student_id)
            if float(average_grade) != -1:                    # only students who have graded assignments
                average_grade = "{:.2f}".format(average_grade)
                dict_stud = {'id': int(student_id), 'grade': average_grade}
                list_best.append(dict_stud)
        comb_sort(list_best, self.compare_average_grade_value)
        return list_best
