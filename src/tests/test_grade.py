import datetime
import unittest

from src.services.studentService import StudentService
from src.repository.inmemory.gradeRepo import GradeRepository
from src.domain.grade import Grade
from src.domain.student import Student
from src.domain.assignment import Assignment
from src.validation.validators import ValidatorGrade, ValidatorStudent
from src.exceptions.exceptions import RepositoryError, ValidationError
from src.services.gradeService import GradeService
from src.repository.inmemory.studentRepo import StudentRepository
from src.repository.inmemory.assignmentRepo import AssignmentRepository
from src.repository.csv.textfile_gradeRepo import GradeTextFileRepository
from src.repository.binary.binaryfile_gradeRepo import GradeBinFileRepository

"""
TESTS FOR ALL FUNCTIONALITIES RELATED TO GRADES
"""


class TestGradeDomain(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        pass

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_grade(self):
        assign_id = 4
        stud_id = 56
        grade = Grade(assign_id, stud_id)
        self.assertEqual(grade.assignment_id, assign_id)
        self.assertEqual(grade.student_id, stud_id)
        self.assertEqual(float(grade.grade_value), -1)
        self.assertEqual(grade.__str__(), "   Assignment ID: 4, Student ID: 56, Grade value: Not graded yet")

        assign_id = 90
        stud_id = 24
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(grade.assignment_id, assign_id)
        self.assertEqual(grade.student_id, stud_id)
        self.assertEqual(grade.grade_value, value)

        self.assertEqual(grade.__str__(), "   Assignment ID: 90, Student ID: 24, Grade value: 10")
        other_value = 9
        grade_same_value = Grade(assign_id, stud_id, other_value)
        self.assertTrue(grade.__eq__(grade_same_value))

        grade.grade_value = 6.7
        self.assertEqual(grade.student_id, stud_id)
        self.assertEqual(grade.assignment_id, assign_id)
        self.assertEqual(float(grade.grade_value), 6.7)
        self.assertEqual(grade.__str__(), "   Assignment ID: 90, Student ID: 24, Grade value: 6.7")


class TestGradeValidator(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._valid = ValidatorGrade()

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_validate_grade(self):
        assign_id = 90
        stud_id = 24
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._valid.validate_grade(grade)

        wrong_id = -27
        grade = Grade(wrong_id, stud_id, value)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_grade(grade)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n")

        wrong_stud_id = -9
        grade = Grade(assign_id, wrong_stud_id, value)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_grade(grade)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\n")

        grade = Grade(wrong_id, wrong_stud_id, value)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_grade(grade)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n"
                                            "Invalid student id! Must be positive integer!\n")

        wrong_value = -10
        grade = Grade(wrong_id, wrong_stud_id, wrong_value)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_grade(grade)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n"
                                            "Invalid student id! Must be positive integer!\n" 
                                            "Invalid grade value! must be a float number between 1 and 10!\n")


class TestGradeRepository(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._repo = GradeRepository()
        self._text_file_repo = GradeTextFileRepository('test_files/grades_test.txt')
        self._bin_file_repo = GradeBinFileRepository('test_files/grades_test.pickle')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_repo_search_by_student_id(self):
        assign_id = 19
        stud_id = 3
        value = 4
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        assign_id = 34
        stud_id = 5
        value = 1
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        found_grade = self._repo.search_by_student_id(5)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.student_id), 5)
        self.assertEqual(int(found_grade.assignment_id), 34)
        self.assertEqual(float(found_grade.grade_value), 1)
        with self.assertRaises(RepositoryError) as re:
            self._repo.search_by_student_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    def test_text_repo_search_by_student_id(self):
        open('test_files/grades_test.txt', 'w').close()
        assign_id = 19
        stud_id = 3
        value = 4
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        assign_id = 34
        stud_id = 5
        value = 1
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        found_grade = self._text_file_repo.search_by_student_id(5)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.student_id), 5)
        self.assertEqual(int(found_grade.assignment_id), 34)
        self.assertEqual(float(found_grade.grade_value), 1)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.search_by_student_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('test_files/grades_test.txt', 'w').close()
    
    def test_bin_repo_search_by_student_id(self):
        open('test_files/grades_test.pickle', 'w').close()
        grade = Grade(78, 24, 4)
        self._bin_file_repo.add_grade(grade)
        grade = Grade(34, 88, 1)
        self._bin_file_repo.add_grade(grade)
        found_grade = self._bin_file_repo.search_by_student_id(24)
        self.assertEqual(int(found_grade.student_id), 24)
        self.assertEqual(int(found_grade.assignment_id), 78)
        self.assertEqual(float(found_grade.grade_value), 4)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.search_by_student_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('test_files/grades_test.pickle', 'w').close()

    def test_repo_search_by_assignment_id(self):
        assign_id = 78
        stud_id = 5
        value = 2
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        assign_id = 34
        stud_id = 55
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        found_grade = self._repo.search_by_assignment_id(34)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.student_id), 55)
        self.assertEqual(int(found_grade.assignment_id), 34)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._repo.search_by_assignment_id(26)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    def test_text_repo_search_by_assignment_id(self):
        open('test_files/grades_test.txt', 'w').close()
        assign_id = 78
        stud_id = 5
        value = 2
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        assign_id = 34
        stud_id = 55
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        found_grade = self._text_file_repo.search_by_assignment_id(34)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.student_id), 55)
        self.assertEqual(int(found_grade.assignment_id), 34)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.search_by_assignment_id(26)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_repo_search_by_assignment_id(self):
        open('test_files/grades_test.pickle', 'w').close()
        assign_id = 78
        stud_id = 5
        value = 2
        grade = Grade(assign_id, stud_id, value)
        self._bin_file_repo.add_grade(grade)

        assign_id = 34
        stud_id = 55
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._bin_file_repo.add_grade(grade)

        found_grade = self._bin_file_repo.search_by_assignment_id(34)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.student_id), 55)
        self.assertEqual(int(found_grade.assignment_id), 34)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.search_by_assignment_id(26)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('test_files/grades_test.pickle', 'w').close()
    
    def test_search_student_and_assignment(self):
        stud_id = 10
        assign_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        stud_id = 10
        assign_id = 12
        value = 1
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        found_grade = self._repo.search_student_and_assignment(10, 12)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.assignment_id), 12)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 1)

        found_grade = self._repo.search_student_and_assignment(10, 11)
        self.assertEqual(int(found_grade.assignment_id), 11)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._repo.search_student_and_assignment(11, 1)
        self.assertEqual(str(re.exception), "Nonexistent assignment id in student's ungraded assignments!\n")

    def test_text_search_student_and_assignment(self):
        open('test_files/grades_test.txt', 'w').close()
        stud_id = 10
        assign_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        stud_id = 10
        assign_id = 12
        value = 1
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        found_grade = self._text_file_repo.search_student_and_assignment(10, 12)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.assignment_id), 12)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 1)

        found_grade = self._text_file_repo.search_student_and_assignment(10, 11)
        self.assertEqual(int(found_grade.assignment_id), 11)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.search_student_and_assignment(11, 1)
        self.assertEqual(str(re.exception), "Nonexistent assignment id in student's ungraded assignments!\n")
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_search_student_and_assignment(self):
        open('test_files/grades_test.pickle', 'w').close()
        stud_id = 10
        assign_id = 88
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._bin_file_repo.add_grade(grade)

        stud_id = 10
        assign_id = 89
        value = 1
        grade = Grade(assign_id, stud_id, value)
        self._bin_file_repo.add_grade(grade)

        found_grade = self._bin_file_repo.search_student_and_assignment(10, 89)
        self.assertEqual(found_grade, grade)
        self.assertEqual(int(found_grade.assignment_id), 89)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 1)

        found_grade = self._bin_file_repo.search_student_and_assignment(10, 88)
        self.assertEqual(int(found_grade.assignment_id), 88)
        self.assertEqual(int(found_grade.student_id), 10)
        self.assertEqual(float(found_grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.search_student_and_assignment(10, 99)
        self.assertEqual(str(re.exception), "Nonexistent assignment id in student's ungraded assignments!\n")
        open('test_files/grades_test.pickle', 'w').close()

    def test_repo_add_grade(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)

        self.assertEqual(len(self._repo.get_all_grades()), 0)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 2)
        with self.assertRaises(RepositoryError) as re:
            self._repo.add_grade(grade)
        self.assertEqual(str(re.exception), "Duplicate grade!\n")

    def test_text_repo_add_grade(self):
        open('test_files/grades_test.txt', 'w').close()
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 2)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.add_grade(grade)
        self.assertEqual(str(re.exception), "Duplicate grade!\n")

    def test_bin_repo_add_grade(self):
        open('test_files/grades_test.pickle', 'w').close()
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)

        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 0)
        self._bin_file_repo.add_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 1)

        assign_id = 70
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._bin_file_repo.add_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 2)
        open('test_files/grades_test.pickle', 'w').close()


    def test_update_grade(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(float(grade.grade_value), 10)
        self._repo.add_grade(grade)
        self._repo.update_grade(assign_id, stud_id)

        new_grade = self._repo.search_by_assignment_id(assign_id)
        self.assertEqual(float(new_grade.grade_value), -1)
        with self.assertRaises(RepositoryError) as re:
            self._repo.update_grade(10, 12)
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")

    def test_text_update_grade(self):
        open('test_files/grades_test.txt', 'w').close()
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(float(grade.grade_value), 10)
        self._text_file_repo.add_grade(grade)
        self._text_file_repo.update_grade(assign_id, stud_id)

        new_grade = self._text_file_repo.search_by_assignment_id(assign_id)
        self.assertEqual(float(new_grade.grade_value), -1)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.update_grade(10, 12)
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_update_grade(self):
        open('test_files/grades_test.pickle', 'w').close()
        assign_id = 67
        stud_id = 56
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(float(grade.grade_value), 10)
        self._bin_file_repo.add_grade(grade)
        self._bin_file_repo.update_grade(assign_id, stud_id)

        new_grade = self._bin_file_repo.search_by_assignment_id(67)
        self.assertEqual(float(new_grade.grade_value), -1)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.update_grade(10, 12)
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")
        open('test_files/grades_test.pickle', 'w').close()

    def test_remove_grade(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 1)
        self._repo.remove_grade(grade)

        self.assertEqual(len(self._repo.get_all_grades()), 0)
        with self.assertRaises(RepositoryError) as re:
            self._repo.remove_grade(Grade(10, 12, 4))
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")

    def test_text_remove_grade(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)
        self._text_file_repo.remove_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.remove_grade(Grade(10, 12, 4))
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_remove_grade(self):
        open('test_files/grades_test.pickle', 'w').close()
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        open('test_files/grades_test.pickle', 'w').close()
        self._bin_file_repo.add_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 21)
        self._bin_file_repo.remove_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 20)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.remove_grade(Grade(10, 12, 4))
        self.assertEqual(str(re.exception), "Nonexistent grade!\n")
        open('test_files/grades_test.pickle', 'w').close()

    def test_remove_grade_with_student_id(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(len(self._repo.get_all_grades()), 0)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._repo.add_grade(grade)

        self.assertEqual(len(self._repo.get_all_grades()), 2)
        self._repo.remove_grade_with_student_id(11)
        self.assertEqual(len(self._repo.get_all_grades()), 1)
        self._repo.remove_grade_with_student_id(13)
        self.assertEqual(len(self._repo.get_all_grades()), 0)

    def test_text_remove_grade_with_student_id(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._text_file_repo.add_grade(grade)

        self.assertEqual(len(self._text_file_repo.get_all_grades()), 2)
        self._text_file_repo.remove_grade_with_student_id(11)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)
        self._text_file_repo.remove_grade_with_student_id(13)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_remove_grade_with_student_id(self):
        open('test_files/grades_test.pickle', 'w').close()
        assign_id = 88
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 0)
        self._bin_file_repo.add_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 1)

        assign_id = 90
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._bin_file_repo.add_grade(grade)

        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 2)
        self._bin_file_repo.remove_grade_with_student_id(11)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 1)
        self._bin_file_repo.remove_grade_with_student_id(13)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 0)
        open('test_files/grades_test.pickle', 'w').close()

    def test_remove_grade_with_assignment_id(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)

        self.assertEqual(len(self._repo.get_all_grades()), 0)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._repo.add_grade(grade)
        self.assertEqual(len(self._repo.get_all_grades()), 2)
        self._repo.remove_grade_with_assignment_id(10)
        self.assertEqual(len(self._repo.get_all_grades()), 1)
        self._repo.remove_grade_with_assignment_id(1)
        self.assertEqual(len(self._repo.get_all_grades()), 0)

    def test_text_remove_grade_with_assignment_id(self):
        assign_id = 10
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)

        assign_id = 1
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._text_file_repo.add_grade(grade)

        self.assertEqual(len(self._text_file_repo.get_all_grades()), 2)
        self._text_file_repo.remove_grade_with_assignment_id(10)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 1)
        self._text_file_repo.remove_grade_with_assignment_id(1)
        self.assertEqual(len(self._text_file_repo.get_all_grades()), 0)
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_remove_grade_with_assignment_id(self):
        assign_id = 88
        stud_id = 11
        value = 10
        grade = Grade(assign_id, stud_id, value)
        open('test_files/grades_test.pickle', 'w').close()
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 20)
        self._bin_file_repo.add_grade(grade)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 21)

        assign_id = 89
        stud_id = 13
        grade = Grade(assign_id, stud_id)
        self._bin_file_repo.add_grade(grade)

        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 22)
        self._bin_file_repo.remove_grade_with_assignment_id(10)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 21)
        self._bin_file_repo.remove_grade_with_assignment_id(1)
        self.assertEqual(len(self._bin_file_repo.get_all_grades()), 20)
        open('test_files/grades_test.pickle', 'w').close()

    def test_repo_grade_student(self):
        stud_id = 12
        assign_id = 80
        grade = Grade(assign_id, stud_id)
        self._repo.add_grade(grade)
        self.assertEqual(float(grade.grade_value), -1)
        self._repo.repo_grade_student(80, 12, 10)

        grade = self._repo.search_by_student_id(12)
        self.assertEqual(float(grade.grade_value), 10)
        stud_id = 11
        assign_id = 14
        value = 5
        grade = Grade(assign_id, stud_id, value)
        self._repo.add_grade(grade)

        self.assertEqual(float(grade.grade_value), 5)
        self._repo.repo_grade_student(14, 11, 2)
        grade = self._repo.search_by_student_id(11)
        self.assertEqual(float(grade.grade_value), 2)

    def test_text_repo_grade_student(self):
        stud_id = 34
        assign_id = 80
        grade = Grade(assign_id, stud_id)
        self._text_file_repo.add_grade(grade)
        self.assertEqual(float(grade.grade_value), -1)
        self._text_file_repo.repo_grade_student(80, 34, 10)

        grade = self._text_file_repo.search_by_student_id(34)
        self.assertEqual(float(grade.grade_value), 10)
        stud_id = 90
        assign_id = 78
        value = 5
        grade = Grade(assign_id, stud_id, value)
        self._text_file_repo.add_grade(grade)

        self.assertEqual(float(grade.grade_value), 5)
        self._text_file_repo.repo_grade_student(78, 90, 2)
        grade = self._text_file_repo.search_by_student_id(90)
        self.assertEqual(float(grade.grade_value), 2)
        open('test_files/grades_test.txt', 'w').close()

    def test_bin_repo_grade_student(self):
        open('test_files/grades_test.pickle', 'w').close()
        stud_id = 24
        assign_id = 80
        grade = Grade(assign_id, stud_id)
        self._bin_file_repo.add_grade(grade)

        self.assertEqual(float(grade.grade_value), -1)
        self._bin_file_repo.repo_grade_student(80, 24, 10)
        grade = self._bin_file_repo.search_by_student_id(24)
        self.assertEqual(float(grade.grade_value), 10)

        stud_id = 45
        assign_id = 90
        value = 5
        grade = Grade(assign_id, stud_id, value)
        self._bin_file_repo.add_grade(grade)

        self.assertEqual(float(grade.grade_value), 5)
        self._bin_file_repo.repo_grade_student(90, 45, 2)
        grade = self._bin_file_repo.search_by_student_id(45)
        self.assertEqual(float(grade.grade_value), 2)
        open('test_files/grades_test.pickle', 'w').close()


class TestGradeService(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._student_repo = StudentRepository()
        self._assignment_repo = AssignmentRepository()
        self._grade_repo = GradeRepository()
        self._valid = ValidatorGrade()
        self._srv = GradeService(self._grade_repo, self._valid, self._student_repo, self._assignment_repo)

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_generate_grade_value(self):   # generate many in order to check every line of generator
        grade = self._srv.generate_grade_value()
        self.assertNotEqual(float(grade), 0)
        self.assertGreater(float(grade), 1)
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))
        grade = self._srv.generate_grade_value()
        self.assertTrue(isinstance(float(grade), float))

    def test_generate_grades_list(self):
        student_val = ValidatorStudent()
        student_srv = StudentService(self._student_repo, student_val)
        student_srv.generate_students_list()
        self.assertEqual(self._srv.no_of_grades(), 0)
        self._srv.generate_grades_list()
        self.assertEqual(self._srv.no_of_grades(), 20)

    def test__srv_assign_to_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 0)
        self.assertEqual(len(self._srv.grades), 0)
        self._srv.assign_to_student(assign_id, stud_id)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 1)
        with self.assertRaises(RepositoryError) as re:
            self._srv.assign_to_student(assign_id, stud_id)
        self.assertEqual(str(re.exception), "Student has already received that assignment!\n")

    def test__srv_assign_to_group(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        stud_id = 25
        name = 'Marcel'
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        self.assertEqual(self._srv.no_of_grades(), 0)
        self._srv.assign_to_group(assign_id, group)
        self.assertEqual(self._srv.no_of_grades(), 2)
        self.assertEqual(len(self._srv.repo.get_all_grades()), 2)
        stud_id = 30
        name = 'Bula'
        group = 913
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        stud_id = 31
        name = 'Gigi'
        group = 913
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        self._srv.assign_to_student(assign_id, 30)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 3)
        self._srv.assign_to_group(assign_id, 913)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 4)
        with self.assertRaises(RepositoryError) as re:
            self._srv.assign_to_student(assign_id, 30)
        self.assertEqual(str(re.exception), "Student has already received that assignment!\n")

    def test_remove_assign_to_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 0)
        self._srv.assign_to_student(assign_id, stud_id)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 1)
        self._srv.remove_assign_to_student(99, 24)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 0)
        with self.assertRaises(RepositoryError) as re:
            self._srv.remove_assign_to_student(90, 24)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        with self.assertRaises(RepositoryError) as re:
            self._srv.remove_assign_to_student(99, 25)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    def test_remove_assign_to_group(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        stud_id = 25
        name = 'Marcel'
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        self.assertEqual(self._srv.no_of_grades(), 0)
        self._srv.assign_to_group(assign_id, group)
        self.assertEqual(self._srv.no_of_grades(), 2)
        self._srv.remove_assign_to_group(99, 912)
        self.assertEqual(self._srv.no_of_grades(), 0)
        with self.assertRaises(RepositoryError) as re:
            self._srv.remove_assign_to_group(900, 912)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    def test_grade_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        stud_id = 25
        name = 'Marcel'
        student = Student(stud_id, name, group)
        self._student_repo.add_student(student)
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        assign_id = 98
        desc = 'problem 3'
        deadline = datetime.date(2011, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._assignment_repo.add_assignment(assignment)
        self._srv.assign_to_student(99, 24)
        self._srv.assign_to_student(98, 24)
        grade = self._grade_repo.search_student_and_assignment(24, 99)
        self.assertEqual(float(grade.grade_value), -1)
        self._srv.grade_student(24, 99, 10)
        grade = self._grade_repo.search_by_student_id(24)
        self.assertEqual(float(grade.grade_value), 10)
        with self.assertRaises(RepositoryError) as re:
            self._srv.grade_student(24, 90, 10)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    def test_ungrade_student(self):
        student = Student(24, 'Gigel', 912)
        self._student_repo.add_student(student)
        student = Student(25, 'Marcel', 912)
        self._student_repo.add_student(student)
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(99, 'problem 2', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2011, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(98, 'problem 3', deadline)
        self._assignment_repo.add_assignment(assignment)
        self._srv.assign_to_student(99, 24)
        self._srv.assign_to_student(98, 24)
        grade = self._grade_repo.search_student_and_assignment(24, 99)
        self.assertEqual(float(grade.grade_value), -1)
        self._srv.grade_student(24, 99, 10)
        grade = self._grade_repo.search_by_student_id(24)
        self.assertEqual(float(grade.grade_value), 10)
        self._srv.ungrade_student(99, 24)
        grade = self._grade_repo.search_student_and_assignment(24, 99)
        self.assertEqual(float(grade.grade_value), -1)
        with self.assertRaises(RepositoryError) as re:
            self._srv.ungrade_student(900, 24)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        with self.assertRaises(RepositoryError) as re:
            self._srv.ungrade_student(99, 2222)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    def test_order_list_descending_by_grade_float(self):
        listt = [{'id': 15, 'grade': 4.75}, {'id': 19, 'grade': 3.00}, {'id': 5, 'grade': 9.10}, {'id': 13, 'grade': 10.00},
                 {'id': 3, 'grade': 7.33}, {'id': 16, 'grade': 1.00}, {'id': 20, 'grade': 1.50}]
        self.assertEqual(float(listt[0]['grade']), 4.75)
        self.assertEqual(float(listt[6]['grade']), 1.50)
        self._srv.order_list_descending_by_grade_float(listt)
        self.assertEqual(float(listt[0]['grade']), 10.00)
        self.assertEqual(float(listt[6]['grade']), 1.00)

    def test_search_in_list(self):
        listt = [{'id': 15, 'grade': 4}, {'id': 19, 'grade': 3}, {'id': 5, 'grade': 9}, {'id': 13, 'grade': 10},
                 {'id': 3, 'grade': 7}, {'id': 16, 'grade': 1}, {'id': 20, 'grade': 1}]
        self.assertTrue(self._srv.search_in_list(listt, 15))
        self.assertTrue(self._srv.search_in_list(listt, 16))
        self.assertFalse(self._srv.search_in_list(listt, 100))
        self.assertFalse(self._srv.search_in_list(listt, 101))

    def test_average_grade_for_student(self):
        grade = Grade(80, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 12, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(11, 12, 4)
        self._grade_repo.add_grade(grade)
        average = self._srv.average_grade_for_student(12)
        self.assertEqual(float(average), 6.00)
        grade = Grade(16, 12, 8)
        self._grade_repo.add_grade(grade)
        average = self._srv.average_grade_for_student(12)
        self.assertEqual(float(average), 6.50)
        average = self._srv.average_grade_for_student(67)
        self.assertEqual(float(average), -1)

    def test_filter_graded_grades_by_student_id(self):
        grade = Grade(80, 11, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 11, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(11, 11, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(80, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 12, 5)
        self._grade_repo.add_grade(grade)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 5)
        student = self._grade_repo.search_by_student_id(11)
        list_grades = list(self._srv.filter_graded_grades_by_student_id(student))
        self.assertEqual(len(list_grades), 3)
        grade = Grade(15, 11)
        self._grade_repo.add_grade(grade)
        grade = Grade(55, 11)
        self._grade_repo.add_grade(grade)
        student = self._grade_repo.search_by_student_id(11)
        list_grades = list(self._srv.filter_graded_grades_by_student_id(student))
        self.assertEqual(len(list_grades), 5)

    def test_filter_grades_by_assignment_id(self):
        grade = Grade(80, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(80, 11, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(80, 10, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 11, 5)
        self._grade_repo.add_grade(grade)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 5)
        assign = self._grade_repo.search_by_assignment_id(80)
        list_grades = list(self._srv.filter_grades_by_assignment_id(assign))
        self.assertEqual(len(list_grades), 3)
        assign = self._grade_repo.search_by_assignment_id(14)
        list_grades = list(self._srv.filter_grades_by_assignment_id(assign))
        self.assertEqual(len(list_grades), 2)

    def test_count_ungraded_assignments_for_student(self):
        deadline = datetime.date(2021, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(80, 'problem 1', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2021, 11, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(20, 'problem 2', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2021, 12, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(50, 'problem 3', deadline)
        self._assignment_repo.add_assignment(assignment)
        student = Student(12, 'ionel', 912)
        self._student_repo.add_student(student)
        student = Student(11, 'gigel', 912)
        self._student_repo.add_student(student)
        self._srv.assign_to_group(80, 912)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 2)
        no = self._srv.count_ungraded_late_assignments_for_student(12)
        self.assertEqual(int(no), 1)
        no = self._srv.count_ungraded_late_assignments_for_student(11)
        self.assertEqual(int(no), 1)
        self._srv.assign_to_student(20, 12)
        self._srv.assign_to_student(50, 12)
        no = self._srv.count_ungraded_late_assignments_for_student(12)
        self.assertEqual(int(no), 3)
        no = self._srv.count_ungraded_late_assignments_for_student(10)
        self.assertEqual(int(no), 0)

    def test_remove_student_and_assignments(self):
        grade = Grade(80, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(14, 12, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(11, 12, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(11, 15, 4)
        self._grade_repo.add_grade(grade)
        self.assertEqual(self._srv.no_of_grades(), 4)
        student = Student(12, 'Iana', 917)
        undo_list = []
        self._srv.remove_student_and_assignments(student, 12, undo_list)
        self.assertEqual(self._srv.no_of_grades(), 1)

    def test_remove_assignment_and_students(self):
        grade = Grade(80, 12, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(80, 11, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(80, 15, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(12, 15, 4)
        self._grade_repo.add_grade(grade)
        self.assertEqual(self._srv.no_of_grades(), 4)
        deadline = datetime.date(2011, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(80, 'problem 5', deadline)
        undo_list = []
        self._srv.remove_assignment_and_students(assignment, 80, undo_list)
        self.assertEqual(self._srv.no_of_grades(), 1)

    def test_create_list_of_given_assignment_ordered(self):
        deadline = datetime.date(2011, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(1, 'problem 1', deadline)
        self._assignment_repo.add_assignment(assignment)
        grade = Grade(1, 12, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 13, 7)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 14, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 15, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 16, 5)
        self._grade_repo.add_grade(grade)
        list_given = self._srv.create_list_of_given_assignment_ordered(1)
        self.assertEqual(len(list_given), 5)
        with self.assertRaises(RepositoryError) as re:
            self._srv.create_list_of_given_assignment_ordered(2)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    def test_create_list_of_late_students(self):
        student = Student(12, 'ionel', 912)
        self._student_repo.add_student(student)
        student = Student(13, 'gigel', 911)
        self._student_repo.add_student(student)
        deadline = datetime.date(2021, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(1, 'problem 1', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2021, 11, 21)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(2, 'problem 2', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2022, 1, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(3, 'problem 3', deadline)
        self._assignment_repo.add_assignment(assignment)
        self._srv.assign_to_student(1, 12)
        self._srv.assign_to_student(2, 13)
        self._srv.assign_to_student(3, 12)
        self.assertEqual(len(self._grade_repo.get_all_grades()), 3)
        list_late = self._srv.create_list_of_late_students()
        self.assertEqual(len(list_late), 2)
        self.assertEqual(int(list_late[0]['ungraded']), 2)
        self.assertEqual(int(list_late[1]['ungraded']), 1)

    def test_create_list_of_best_school_situation(self):
        student = Student(12, 'ionel', 912)
        self._student_repo.add_student(student)
        student = Student(13, 'gigel', 911)
        self._student_repo.add_student(student)
        student = Student(14, 'vasile', 913)
        self._student_repo.add_student(student)
        student = Student(15, 'alex', 911)
        self._student_repo.add_student(student)
        student = Student(16, 'maria', 917)
        self._student_repo.add_student(student)
        student = Student(17, 'marian', 914)
        self._student_repo.add_student(student)
        deadline = datetime.date(2021, 9, 18)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(1, 'problem 1', deadline)
        self._assignment_repo.add_assignment(assignment)
        deadline = datetime.date(2021, 6, 13)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(2, 'problem 2', deadline)
        self._assignment_repo.add_assignment(assignment)
        grade = Grade(1, 12, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 13, 7)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 14, 4)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 15, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 16, 5)
        self._grade_repo.add_grade(grade)
        grade = Grade(2, 12, 3)
        self._grade_repo.add_grade(grade)
        grade = Grade(2, 13, 2)
        self._grade_repo.add_grade(grade)
        grade = Grade(2, 14, 6)
        self._grade_repo.add_grade(grade)
        grade = Grade(2, 15, 8)
        self._grade_repo.add_grade(grade)
        grade = Grade(2, 16, 9)
        self._grade_repo.add_grade(grade)
        grade = Grade(1, 17)
        self._grade_repo.add_grade(grade)
        list_best = self._srv.create_list_of_best_school_situation()
        self.assertEqual(len(list_best), 5)
        self.assertEqual(float(list_best[0]['grade']), 8.50)
        self.assertEqual(float(list_best[1]['grade']), 7.00)
        self.assertEqual(float(list_best[2]['grade']), 5.00)
        self.assertEqual(float(list_best[3]['grade']), 4.50)
        self.assertEqual(float(list_best[4]['grade']), 4.00)
