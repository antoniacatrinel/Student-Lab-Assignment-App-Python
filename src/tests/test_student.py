from domain.student import Student
from repository.inmemory.studentRepo import StudentRepository
from validation.validators import ValidatorStudent
from exceptions.exceptions import RepositoryError, ValidationError
from services.studentService import StudentService
import unittest
from repository.csv.textfile_studentRepo import StudentTextFileRepository
from repository.binary.binaryfile_studentRepo import StudentBinFileRepository

"""
TESTS FOR ALL FUNCTIONALITIES RELATED TO STUDENTS
"""


class TestStudentDomain(unittest.TestCase):
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

    def test_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 915
        student = Student(stud_id, name, group)
        self.assertEqual(student.student_id, stud_id)
        self.assertEqual(student.name, name)
        self.assertEqual(student.group, group)
        self.assertEqual(student.__str__(), "   Student Id: 24, Name: Gigel, Group: 915")
        other_name = 'Ionel'
        other_group = 917
        student_same_id = Student(stud_id, other_name, other_group)
        self.assertTrue(student.__eq__(student_same_id))
        student.name = 'Florica'
        student.group = 914
        self.assertEqual(student.student_id, stud_id)
        self.assertEqual(student.name, 'Florica')
        self.assertEqual(student.group, 914)
        self.assertEqual(student.__str__(), "   Student Id: 24, Name: Florica, Group: 914")


class TestStudentValidator(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._valid = ValidatorStudent()

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_validate_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._valid.validate_student(student)
        wrong_id = -27
        student = Student(wrong_id, name, group)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_student(student)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\n")
        wrong_group = 920
        student = Student(stud_id, name, wrong_group)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_student(student)
        self.assertEqual(str(ve.exception), "Invalid student group! Must be an integer between 911 and 917!\n")
        student = Student(wrong_id, name, wrong_group)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_student(student)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\nInvalid student group! "
                                            "Must be an integer between 911 and 917!\n")


class TestStudentRepository(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._repo = StudentRepository()
        self._text_file_Repo = StudentTextFileRepository('students_test.txt')
        self._bin_file_Repo = StudentBinFileRepository('students_test.pickle')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_search_student_by_id(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        found_student = self._repo.search_by_id(25)
        self.assertEqual(found_student, student)
        self.assertEqual(found_student.student_id, student.student_id)
        self.assertEqual(found_student.name, 'Ionel')
        self.assertEqual(int(found_student.group), 913)
        with self.assertRaises(RepositoryError) as re:
            self._repo.search_by_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    """
    def test_text_search_student_by_id(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        found_student = self._text_file_Repo.search_by_id(25)
        self.assertEqual(found_student, student)
        self.assertEqual(found_student.student_id, student.student_id)
        self.assertEqual(found_student.name, 'Ionel')
        self.assertEqual(int(found_student.group), 913)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_Repo.search_by_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.txt', 'w').close()

    def test_bin_search_student_by_id(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        found_student = self._bin_file_Repo.search_by_id(25)
        self.assertEqual(found_student, student)
        self.assertEqual(found_student.student_id, student.student_id)
        self.assertEqual(found_student.name, 'Ionel')
        self.assertEqual(int(found_student.group), 913)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_Repo.search_by_id(26)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.pickle', 'w').close()

    """
    def test_add_repo_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self.assertEqual(len(self._repo.get_all_students()), 0)
        self._repo.add_student(student)
        self.assertEqual(len(self._repo.get_all_students()), 1)
        name = 'Ionel'
        group = 916
        student = Student(stud_id, name, group)
        with self.assertRaises(RepositoryError) as re:
            self._repo.add_student(student)
        self.assertEqual(str(re.exception), "Duplicate student id!\n")

    """
    def test_text_add_repo_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self.assertEqual(len(self._text_file_Repo.get_all_students()), 0)
        self._text_file_Repo.add_student(student)
        self.assertEqual(len(self._text_file_Repo.get_all_students()), 1)
        name = 'Ionel'
        group = 916
        student = Student(stud_id, name, group)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_Repo.add_student(student)
        self.assertEqual(str(re.exception), "Duplicate student id!\n")
        open('students_test.txt', 'w').close()

    def test_bin_add_repo_student(self):
        open('students_test.pickle', 'w').close()
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self.assertEqual(len(self._bin_file_Repo.get_all_students()), 0)
        self._bin_file_Repo.add_student(student)
        self.assertEqual(len(self._bin_file_Repo.get_all_students()), 1)
        name = 'Ionel'
        group = 916
        student = Student(stud_id, name, group)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_Repo.add_student(student)
        self.assertEqual(str(re.exception), "Duplicate student id!\n")
        open('students_test.pickle', 'w').close()

    """
    def test_remove_repo_student_by_id(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        self.assertEqual(len(self._repo.get_all_students()), 2)
        self._repo.remove_student_by_id(25)
        self.assertEqual(len(self._repo.get_all_students()), 1)
        self._repo.remove_student_by_id(24)
        self.assertEqual(len(self._repo.get_all_students()), 0)

    """
    def test_text_remove_repo_student_by_id(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        self.assertEqual(len(self._text_file_Repo.get_all_students()), 2)
        self._text_file_Repo.remove_student_by_id(25)
        self.assertEqual(len(self._text_file_Repo.get_all_students()), 1)
        self._text_file_Repo.remove_student_by_id(24)
        self.assertEqual(len(self._text_file_Repo.get_all_students()), 0)
        open('students_test.txt', 'w').close()

    def test_bin_remove_repo_student_by_id(self):
        open('students_test.pickle', 'w').close()
        stud_id = 24
        name = 'Gigel'
        group = 912
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud_id = 25
        name = 'Ionel'
        group = 913
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        self.assertEqual(len(self._bin_file_Repo.get_all_students()), 22)
        self._bin_file_Repo.remove_student_by_id(25)
        self.assertEqual(len(self._bin_file_Repo.get_all_students()), 21)
        self._bin_file_Repo.remove_student_by_id(24)
        self.assertEqual(len(self._bin_file_Repo.get_all_students()), 20)
        open('students_test.pickle', 'w').close()

    """
    def test_repo_update_student_name(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud = self._repo.search_by_id(45)
        self.assertEqual(stud.name, 'Marian')
        self._repo.update_student_name(45, 'Ionel')
        stud = self._repo.search_by_id(45)
        self.assertEqual(stud.name, 'Ionel')
        with self.assertRaises(RepositoryError) as re:
            self._repo.update_student_name(30, 'Gigel')
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    """
    def test_text_repo_update_student_name(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud = self._text_file_Repo.search_by_id(45)
        self.assertEqual(stud.name, 'Marian')
        self._text_file_Repo.update_student_name(45, 'Ionel')
        stud = self._text_file_Repo.search_by_id(45)
        self.assertEqual(stud.name, 'Ionel')
        with self.assertRaises(RepositoryError) as re:
            self._text_file_Repo.update_student_name(30, 'Gigel')
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.txt', 'w').close()

    def test_bin_repo_update_student_name(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud = self._bin_file_Repo.search_by_id(45)
        self.assertEqual(stud.name, 'Marian')
        self._bin_file_Repo.update_student_name(45, 'Ionel')
        stud = self._bin_file_Repo.search_by_id(45)
        self.assertEqual(stud.name, 'Ionel')
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_Repo.update_student_name(30, 'Gigel')
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.pickle', 'w').close()
    """
    def test_repo_update_student_group(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._repo.add_student(student)
        stud = self._repo.search_by_id(45)
        self.assertEqual(stud.group, 915)
        self._repo.update_student_group(45, 917)
        stud = self._repo.search_by_id(45)
        self.assertEqual(stud.group, 917)
        with self.assertRaises(RepositoryError) as re:
            self._repo.update_student_name(30, 915)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    """
    def test_text_repo_update_student_group(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._text_file_Repo.add_student(student)
        stud = self._text_file_Repo.search_by_id(45)
        self.assertEqual(stud.group, 915)
        self._text_file_Repo.update_student_group(45, 917)
        stud = self._text_file_Repo.search_by_id(45)
        self.assertEqual(stud.group, 917)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_Repo.update_student_name(30, 915)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.txt', 'w').close()

    def test_bin_repo_update_student_group(self):
        stud_id = 60
        name = 'Maria'
        group = 916
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud_id = 45
        name = 'Marian'
        group = 915
        student = Student(stud_id, name, group)
        self._bin_file_Repo.add_student(student)
        stud = self._bin_file_Repo.search_by_id(45)
        self.assertEqual(stud.group, 915)
        self._bin_file_Repo.update_student_group(45, 917)
        stud = self._bin_file_Repo.search_by_id(45)
        self.assertEqual(stud.group, 917)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_Repo.update_student_name(30, 915)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        open('students_test.pickle', 'w').close()
    """


class TestStudentService(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._repo = StudentRepository()
        self._valid = ValidatorStudent()
        self._srv = StudentService(self._repo, self._valid)

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_generate_students_list(self):
        self.assertEqual(len(self._repo.get_all_students()), 0)
        self._srv.generate_students_list()
        self.assertEqual(len(self._repo.get_all_students()), 20)

    def test_service_add_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        self.assertEqual(self._srv.no_of_students(), 0)
        self.assertEqual(len(self._srv.students), 0)
        self._srv.add_student_run(stud_id, name, group)
        self.assertEqual(self._srv.no_of_students(), 1)
        name = 'Ionel'
        group = 914
        with self.assertRaises(RepositoryError) as re:
            self._srv.add_student_run(stud_id, name, group)
        self.assertEqual(str(re.exception), "Duplicate student id!\n")
        wrong_id = -75
        with self.assertRaises(ValidationError) as ve:
            self._srv.add_student_run(wrong_id, name, group)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\n")
        wrong_id = -89
        wrong_group = 900
        with self.assertRaises(ValidationError) as ve:
            self._srv.add_student_run(wrong_id, name, wrong_group)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\nInvalid student group! "
                                            "Must be an integer between 911 and 917!\n")

    def test_service_remove_student(self):
        stud_id = 24
        name = 'Gigel'
        group = 912
        self._srv.add_student_run(stud_id, name, group)
        stud_id = 25
        name = 'Ionel'
        group = 913
        self._srv.add_student_run(stud_id, name, group)
        self.assertEqual(self._srv.no_of_students(), 2)
        self._srv.remove_student_run(stud_id)
        self.assertEqual(self._srv.no_of_students(), 1)
        wrong_id = 44
        with self.assertRaises(RepositoryError) as re:
            self._srv.remove_student_run(wrong_id)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
        self.assertEqual(self._srv.no_of_students(), 1)

    def test_service_update_student_group(self):
        stud_id = 45
        name = 'Marian'
        group = 915
        self._srv.add_student_run(stud_id, name, group)
        stud = self._srv.repo.search_by_id(stud_id)
        self.assertEqual(stud.group, 915)
        self._srv.update_student_group_run(45, 913)
        stud = self._srv.repo.search_by_id(45)
        self.assertEqual(stud.group, 913)
        with self.assertRaises(RepositoryError) as re:
            self._srv.update_student_group_run(30, 916)
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")

    def test_service_update_student_name(self):
        stud_id = 45
        name = 'Marian'
        group = 915
        self._srv.add_student_run(stud_id, name, group)
        stud = self._srv.repo.search_by_id(stud_id)
        self.assertEqual(stud.name, 'Marian')
        self._srv.update_student_name_run(45, 'Ionel')
        stud = self._srv.repo.search_by_id(45)
        self.assertEqual(stud.name, 'Ionel')
        with self.assertRaises(RepositoryError) as re:
            self._srv.update_student_name_run(30, 'Gigel')
        self.assertEqual(str(re.exception), "Nonexistent student id!\n")
