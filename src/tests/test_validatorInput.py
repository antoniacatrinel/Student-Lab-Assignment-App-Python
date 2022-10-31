import unittest

from src.validation.validators import ValidatorInput
from src.exceptions.exceptions import ValidationError, InputError


class TestValidatorInput(unittest.TestCase):
    def setUp(self) -> None:
        """
        Runs before every test method
        """
        self._valid = ValidatorInput()

    def tearDown(self) -> None:
        """
        Runs after every test method
        """
        pass

    def test_validate_student_id(self):
        student_id = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_student_id(student_id)
        self.assertEqual(str(ie.exception), "Id cannot be empty!\n")

        student_id = 10
        self._valid.validate_student_id(student_id)

        student_id = -10
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_student_id(student_id)
        self.assertEqual(str(ve.exception), "Invalid student id! Must be positive integer!\n")

        student_id = 'aaa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_student_id(student_id)
        self.assertEqual(str(ie.exception), "Invalid student id! Must be a numerical value!\n")

    def test_validate_student_group(self):
        group = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_student_group(group)
        self.assertEqual(str(ie.exception), "Group cannot be empty!\n")

        group = 916
        self._valid.validate_student_group(group)

        group = 918
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_student_group(group)
        self.assertEqual(str(ve.exception), "Invalid student group! Must be an integer between 911 and 917!\n")

        group = 'aaa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_student_group(group)
        self.assertEqual(str(ie.exception), "Invalid group! Must be a numerical value!\n")

    def test_validate_student_name(self):
        name = 'aaa'
        self._valid.validate_student_name(name)

        name = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_student_name(name)
        self.assertEqual(str(ie.exception), "Student name cannot be empty!\n")

    def test_validate_assignment_id(self):
        assignment_id = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_assignment_id(assignment_id)
        self.assertEqual(str(ie.exception), "Id cannot be empty!\n")

        assignment_id = 10
        self._valid.validate_assignment_id(assignment_id)

        assignment_id = -10
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_assignment_id(assignment_id)
        self.assertEqual(str(ve.exception), "Invalid assignment id! Must be positive integer!\n")

        assignment_id = 'aaa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_assignment_id(assignment_id)
        self.assertEqual(str(ie.exception), "Invalid assignment id! Must be a numerical value!\n")

    def test_validate_assignment_description(self):
        desc = 'aaa'
        self._valid.validate_assignment_description(desc)

        desc = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_assignment_description(desc)
        self.assertEqual(str(ie.exception), "Assignment description cannot be empty!\n")

    def test_validate_deadline_day(self):
        day = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_day(day)
        self.assertEqual(str(ie.exception), "Deadline day cannot be empty!\n")

        day = 12
        self._valid.validate_deadline_day(day)

        day = 222
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_deadline_day(day)
        self.assertEqual(str(ve.exception), "Invalid deadline day! Must be an integer between 1 and 30!\n")

        day = 'aa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_day(day)
        self.assertEqual(str(ie.exception), "Invalid deadline day! Must be a numerical value!\n")

    def test_validate_deadline_month(self):
        month = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_month(month)
        self.assertEqual(str(ie.exception), "Deadline month cannot be empty!\n")

        month = 12
        self._valid.validate_deadline_month(month)

        month = 23
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_deadline_month(month)
        self.assertEqual(str(ve.exception), "Invalid deadline month! Must be an integer between 1 and 12!\n")

        month = 'aa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_month(month)
        self.assertEqual(str(ie.exception), "Invalid deadline month! Must be a numerical value!\n")

    def test_validate_deadline_year(self):
        year = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_year(year)
        self.assertEqual(str(ie.exception), "Deadline year cannot be empty!\n")

        year = 2021
        self._valid.validate_deadline_year(year)

        year = 3000
        with self.assertRaises(ValidationError) as ve:
            self._valid.validate_deadline_year(year)
        self.assertEqual(str(ve.exception), "Invalid deadline year! Must be an integer between 2000 and 2100!\n")

        year = 'aa'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_deadline_year(year)
        self.assertEqual(str(ie.exception), "Invalid deadline year! Must be a numerical value!\n")

    def test_validate_grade_value(self):
        value = ''
        with self.assertRaises(InputError) as ie:
            self._valid.validate_grade_value(value)
        self.assertEqual(str(ie.exception), "Grade value cannot be empty!\n")

        value = 10
        self._valid.validate_grade_value(value)

        value = 9.67
        self._valid.validate_grade_value(value)

        value = 'no'
        with self.assertRaises(InputError) as ie:
            self._valid.validate_grade_value(value)
        self.assertEqual(str(ie.exception), "Invalid grade value! Must be a numerical value!\n")