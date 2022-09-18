import datetime
from domain.assignment import Assignment
from validation.validators import ValidatorAssignment
from repository.inmemory.assignmentRepo import AssignmentRepository
from exceptions.exceptions import RepositoryError, ValidationError
from services.assignmentService import AssignmentService
import unittest
from repository.csv.textfile_assignmentRepo import AssignmentTextFileRepository
from repository.binary.binaryfile_assignmentRepo import AssignmentBinFileRepository

"""
TESTS FOR ALL FUNCTIONALITIES RELATED TO ASSIGNMENTS
"""


class TestAssignmentDomain(unittest.TestCase):
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

    def test_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self.assertEqual(int(assignment.assignment_id), int(assign_id))
        self.assertEqual(assignment.description, desc)
        self.assertEqual(assignment.deadline, deadline)
        self.assertEqual(assignment.__str__(), "   Assignment Id: 99, Description: problem 2, Deadline: 14/12/2010")
        other_desc = 'problem 3'
        other_deadline = datetime.date(2011, 1, 19)
        other_deadline = other_deadline.strftime('%d/%m/%Y')
        assignment_same_id = Assignment(assign_id, other_desc, other_deadline)
        self.assertTrue(assignment.__eq__(assignment_same_id))
        assignment.description = 'problem 999'
        new_deadline = datetime.date(2021, 4, 6)
        new_deadline = new_deadline.strftime('%d/%m/%Y')
        assignment.deadline = new_deadline
        self.assertEqual(assignment.description, 'problem 999')
        self.assertEqual(assignment.deadline, new_deadline)
        self.assertEqual(assignment.__str__(), "   Assignment Id: 99, Description: problem 999, Deadline: 06/04/2021")


class TestAssignmentValidator(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._valid = ValidatorAssignment()

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_validate_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._valid.validate_assignment(assignment)
        wrong_id = -27
        assignment = Assignment(wrong_id, desc, deadline)
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_assignment(assignment)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n")


class TestAssignmentRepository(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._repo = AssignmentRepository()
        self._text_file_repo = AssignmentTextFileRepository('assignments_test.txt')
        self._bin_file_repo = AssignmentBinFileRepository('assignments_test.pickle')

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_search_assignment__by_id(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        found_assign = self._repo.search_by_id(assign_id)
        self.assertEqual(found_assign, assignment)
        self.assertEqual(found_assign.assignment_id, assignment.assignment_id)
        self.assertEqual(found_assign.description, assignment.description)
        self.assertEqual(found_assign.deadline, assignment.deadline)
        assign_id = 26
        with self.assertRaises(RepositoryError) as re:
            self._repo.search_by_id(assign_id)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    """
    def test_text_search_assignment__by_id(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        found_assign = self._text_file_repo.search_by_id(assign_id)
        self.assertEqual(found_assign, assignment)
        self.assertEqual(found_assign.assignment_id, assignment.assignment_id)
        self.assertEqual(found_assign.description, assignment.description)
        self.assertEqual(found_assign.deadline, assignment.deadline)
        assign_id = 26
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.search_by_id(assign_id)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.txt', 'w').close()

    def test_bin_search_assignment__by_id(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        found_assign = self._bin_file_repo.search_by_id(assign_id)
        self.assertEqual(found_assign, assignment)
        self.assertEqual(found_assign.assignment_id, assignment.assignment_id)
        self.assertEqual(found_assign.description, assignment.description)
        self.assertEqual(found_assign.deadline, assignment.deadline)
        assign_id = 26
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.search_by_id(assign_id)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.pickle', 'w').close()

    """
    def test_add_repo_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self.assertEqual(len(self._repo.get_all_assignments()), 0)
        self._repo.add_assignment(assignment)
        self.assertEqual(len(self._repo.get_all_assignments()), 1)
        desc = 'pb 45'
        assignment = Assignment(assign_id, desc, deadline)
        with self.assertRaises(RepositoryError) as re:
            self._repo.add_assignment(assignment)
        self.assertEqual(str(re.exception), "Duplicate assignment id!\n")

    """
    def test_text_add_repo_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        open('assignments_test.txt', 'w').close()
        self.assertEqual(len(self._text_file_repo.get_all_assignments()), 0)
        self._text_file_repo.add_assignment(assignment)
        self.assertEqual(len(self._text_file_repo.get_all_assignments()), 1)
        desc = 'pb 45'
        assignment = Assignment(assign_id, desc, deadline)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.add_assignment(assignment)
        self.assertEqual(str(re.exception), "Duplicate assignment id!\n")
        open('assignments_test.txt', 'w').close()

    def test_bin_add_repo_assignment(self):
        open('assignments_test.pickle', 'w').close()
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        open('assignments_test.pickle', 'w').close()
        self.assertEqual(len(self._bin_file_repo.get_all_assignments()), 0)
        self._bin_file_repo.add_assignment(assignment)
        self.assertEqual(len(self._bin_file_repo.get_all_assignments()), 1)
        desc = 'pb 45'
        assignment = Assignment(assign_id, desc, deadline)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.add_assignment(assignment)
        self.assertEqual(str(re.exception), "Duplicate assignment id!\n")
        open('assignments_test.pickle', 'w').close()

    """
    def test_remove_repo_assignment_by_id(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        assign_id = 33
        desc = 'problem 3'
        deadline = datetime.date(2011, 11, 11)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        self.assertEqual(len(self._repo.get_all_assignments()), 2)
        self._repo.remove_assignment_by_id(33)
        self.assertEqual(len(self._repo.get_all_assignments()), 1)
        self._repo.remove_assignment_by_id(99)
        self.assertEqual(len(self._repo.get_all_assignments()), 0)

    """
    def test_text_remove_repo_assignment_by_id(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        assign_id = 33
        desc = 'problem 3'
        deadline = datetime.date(2011, 11, 11)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        self.assertEqual(len(self._text_file_repo.get_all_assignments()), 2)
        self._text_file_repo.remove_assignment_by_id(33)
        self.assertEqual(len(self._text_file_repo.get_all_assignments()), 1)
        self._text_file_repo.remove_assignment_by_id(99)
        self.assertEqual(len(self._text_file_repo.get_all_assignments()), 0)
        open('assignments_test.txt', 'w').close()

    def test_bin_remove_repo_assignment_by_id(self):
        open('assignments_test.pickle', 'w').close()
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        assign_id = 33
        desc = 'problem 3'
        deadline = datetime.date(2011, 11, 11)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        self.assertEqual(len(self._bin_file_repo.get_all_assignments()), 22)
        self._bin_file_repo.remove_assignment_by_id(33)
        self.assertEqual(len(self._bin_file_repo.get_all_assignments()), 21)
        self._bin_file_repo.remove_assignment_by_id(99)
        self.assertEqual(len(self._bin_file_repo.get_all_assignments()), 20)
        open('assignments_test.pickle', 'w').close()

    """
    def test_repo_update_assignment_description(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        assign = self._repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 4')
        self._repo.update_assignment_description(56, 'problem 44')
        assign = self._repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 44')
        self.assertEqual(int(assign.assignment_id), 56)
        with self.assertRaises(RepositoryError) as re:
            self._repo.update_assignment_description(30, 'problem 6')
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    """
    def test_text_repo_update_assignment_description(self):
        open('assignments_test.txt', 'w').close()
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        assign = self._text_file_repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 4')
        self._text_file_repo.update_assignment_description(56, 'problem 44')
        assign = self._text_file_repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 44')
        self.assertEqual(int(assign.assignment_id), 56)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.update_assignment_description(30, 'problem 6')
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.txt', 'w').close()

    def test_bin_repo_update_assignment_description(self):
        open('assignments_test.pickle', 'w').close()
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        assign = self._bin_file_repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 4')
        self._bin_file_repo.update_assignment_description(56, 'problem 44')
        assign = self._bin_file_repo.search_by_id(56)
        self.assertEqual(assign.description, 'problem 44')
        self.assertEqual(int(assign.assignment_id), 56)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.update_assignment_description(30, 'problem 6')
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.pickle', 'w').close()

    """
    def test_repo_update_assignment_deadline(self):
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._repo.add_assignment(assignment)
        assign = self._repo.search_by_id(56)
        self.assertEqual(assign.deadline, deadline)
        new_deadline = datetime.date(2016, 2, 6)
        new_deadline = new_deadline.strftime('%d/%m/%Y')
        self._repo.update_assignment_deadline(56, new_deadline)
        assign = self._repo.search_by_id(56)
        self.assertEqual(assign.deadline, new_deadline)
        with self.assertRaises(RepositoryError) as re:
            self._repo.update_assignment_deadline(30, new_deadline)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    """
    def test_text_repo_update_assignment_deadline(self):
        open('assignments_test.txt', 'w').close()
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._text_file_repo.add_assignment(assignment)
        assign = self._text_file_repo.search_by_id(56)
        self.assertEqual(assign.deadline, deadline)
        new_deadline = datetime.date(2016, 2, 6)
        new_deadline = new_deadline.strftime('%d/%m/%Y')
        self._text_file_repo.update_assignment_deadline(56, new_deadline)
        assign = self._text_file_repo.search_by_id(56)
        self.assertEqual(assign.deadline, new_deadline)
        with self.assertRaises(RepositoryError) as re:
            self._text_file_repo.update_assignment_deadline(30, new_deadline)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.txt', 'w').close()

    def test_bin_repo_update_assignment_deadline(self):
        open('assignments_test.pickle', 'w').close()
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        assignment = Assignment(assign_id, desc, deadline)
        self._bin_file_repo.add_assignment(assignment)
        assign = self._bin_file_repo.search_by_id(56)
        self.assertEqual(assign.deadline, deadline)
        new_deadline = datetime.date(2016, 2, 6)
        new_deadline = new_deadline.strftime('%d/%m/%Y')
        self._bin_file_repo.update_assignment_deadline(56, new_deadline)
        assign = self._bin_file_repo.search_by_id(56)
        self.assertEqual(assign.deadline, new_deadline)
        with self.assertRaises(RepositoryError) as re:
            self._bin_file_repo.update_assignment_deadline(30, new_deadline)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        open('assignments_test.pickle', 'w').close()

    """


class TestAssignmentService(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._repo = AssignmentRepository()
        self._valid = ValidatorAssignment()
        self._srv = AssignmentService(self._repo, self._valid)

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_generate_assignments_list(self):
        self.assertEqual(self._srv.no_of_assignments(), 0)
        self._srv.generate_assignments_list()
        self.assertEqual(self._srv.no_of_assignments(), 20)

    def test_service_add_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        self.assertEqual(self._srv.no_of_assignments(), 0)
        self.assertEqual(len(self._srv.assignments), 0)
        self._srv.add_assignment_run(assign_id, desc, deadline)
        self.assertEqual(self._srv.no_of_assignments(), 1)
        with self.assertRaises(RepositoryError) as re:
            self._srv.add_assignment_run(assign_id, desc, deadline)
        self.assertEqual(str(re.exception), "Duplicate assignment id!\n")
        wrong_id = -75
        with self.assertRaises(ValidationError) as ve:
            self._srv.add_assignment_run(wrong_id, desc, deadline)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n")

    def test_service_remove_assignment(self):
        assign_id = 99
        desc = 'problem 2'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        assign_id = 33
        desc = 'problem 3'
        deadline = datetime.date(2010, 12, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        self.assertEqual(self._srv.no_of_assignments(), 2)
        self._srv.remove_assignment_run(33)
        self.assertEqual(self._srv.no_of_assignments(), 1)
        wrong_id = 44
        with self.assertRaises(RepositoryError) as re:
            self._srv.remove_assignment_run(wrong_id)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
        self.assertEqual(self._srv.no_of_assignments(), 1)
        self._srv.remove_assignment_run(99)
        self.assertEqual(self._srv.no_of_assignments(), 0)

    def test_service_update_assignment_description(self):
        assign_id = 56
        desc = 'problem 4'
        deadline = datetime.date(2013, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        assign_id = 43
        desc = 'problem 60'
        deadline = datetime.date(2013, 1, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        assign = self._srv.repo.search_by_id(43)
        self.assertEqual(assign.description, 'problem 60')
        self._srv.update_assignment_description_run(43, 'problem 6')
        assign = self._srv.repo.search_by_id(43)
        self.assertEqual(assign.description, 'problem 6')
        with self.assertRaises(RepositoryError) as re:
            self._srv.update_assignment_description_run(30, 'problem 24')
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")

    def test_service_update_assignment_deadline(self):
        assign_id = 29
        desc = 'problem 78'
        deadline = datetime.date(2020, 12, 1)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        assign_id = 78
        desc = 'problem 20'
        deadline = datetime.date(2022, 1, 14)
        deadline = deadline.strftime('%d/%m/%Y')
        self._srv.add_assignment_run(assign_id, desc, deadline)
        assign = self._srv.repo.search_by_id(78)
        self.assertEqual(assign.deadline, deadline)
        new_deadline = datetime.date(2023, 2, 11)
        new_deadline = new_deadline.strftime('%d/%m/%Y')
        self._srv.update_assignment_deadline_run(78, new_deadline)
        assign = self._srv.repo.search_by_id(78)
        self.assertEqual(assign.deadline, new_deadline)
        with self.assertRaises(RepositoryError) as re:
            self._srv.update_assignment_deadline_run(30, new_deadline)
        self.assertEqual(str(re.exception), "Nonexistent assignment id!\n")
