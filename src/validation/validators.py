from exceptions.exceptions import ValidationError, InputError
import datetime


class ValidatorStudent:
    @staticmethod
    def validate_student(student):
        err = ""
        if int(student.student_id) < 0:
            err += "Invalid student id! Must be positive integer!\n"
        if int(student.group) < 911 or int(student.group) > 917:
            err += "Invalid student group! Must be an integer between 911 and 917!\n"
        if len(err) > 0:
            raise ValidationError(err)


class ValidatorAssignment:
    @staticmethod
    def validate_assignment(assignment):
        if int(assignment.assignment_id) < 0:
            raise ValidationError("Invalid assignment id! Must be positive integer!\n")


class ValidatorGrade:
    @staticmethod
    def validate_grade(grade):
        err = ""
        if int(grade.assignment_id) < 0:
            err += "Invalid assignment id! Must be positive integer!\n"
        if int(grade.student_id) < 0:
            err += "Invalid student id! Must be positive integer!\n"
        if float(grade.grade_value) != -1 and float(grade.grade_value) <= 0 or float(grade.grade_value) > 10:
            err += "Invalid grade value! must be a float number between 1 and 10!\n"
        if len(err) > 0:
            raise ValidationError(err)

    @staticmethod
    def validate_late_deadline(deadline):
        deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y')
        today = datetime.datetime.now()
        if deadline < today:
            return True
        return False


class ValidatorInput:
    @staticmethod
    def validate_student_id(student_id):
        if len(str(student_id)) == 0:
            raise InputError("Id cannot be empty!\n")
        try:
            student_id = int(student_id)
            if int(student_id) < 0:
                raise ValidationError("Invalid student id! Must be positive integer!\n")
        except ValueError:
            raise InputError("Invalid student id! Must be a numerical value!\n")

    @staticmethod
    def validate_student_name(name):
        if len(name) == 0:
            raise InputError("Student name cannot be empty!\n")

    @staticmethod
    def validate_student_group(group):
        if len(str(group)) == 0:
            raise InputError("Group cannot be empty!\n")
        try:
            group = int(group)
            if int(group) < 911 or int(group) > 917:
                raise ValidationError("Invalid student group! Must be an integer between 911 and 917!\n")
        except ValueError:
            raise InputError("Invalid group! Must be a numerical value!\n")

    @staticmethod
    def validate_assignment_id(assignment_id):
        if len(str(assignment_id)) == 0:
            raise InputError("Id cannot be empty!\n")
        try:
            assignment_id = int(assignment_id)
            if int(assignment_id) < 0:
                raise ValidationError("Invalid assignment id! Must be positive integer!\n")
        except ValueError:
            raise InputError("Invalid assignment id! Must be a numerical value!\n")

    @staticmethod
    def validate_assignment_description(description):
        if len(description) == 0:
            raise InputError("Assignment description cannot be empty!\n")

    @staticmethod
    def validate_deadline_day(deadline_day):
        if len(str(deadline_day)) == 0:
            raise InputError("Deadline day cannot be empty!\n")
        try:
            deadline_day = int(deadline_day)
            if int(deadline_day) > 30 or int(deadline_day) < 1:
                raise ValidationError("Invalid deadline day! Must be an integer between 1 and 30!\n")
        except ValueError:
            raise InputError("Invalid deadline day! Must be a numerical value!\n")

    @staticmethod
    def validate_deadline_month(deadline_month):
        if len(str(deadline_month)) == 0:
            raise InputError("Deadline month cannot be empty!\n")
        try:
            deadline_month = int(deadline_month)
            if int(deadline_month) > 12 or int(deadline_month) < 1:
                raise ValidationError("Invalid deadline month! Must be an integer between 1 and 12!\n")
        except ValueError:
            raise InputError("Invalid deadline month! Must be a numerical value!\n")

    @staticmethod
    def validate_deadline_year(deadline_year):
        if len(str(deadline_year)) == 0:
            raise InputError("Deadline year cannot be empty!\n")
        try:
            deadline_year = int(deadline_year)
            if int(deadline_year) > 2100 or int(deadline_year) < 2000:
                raise ValidationError("Invalid deadline year! Must be an integer between 2000 and 2100!\n")
        except ValueError:
            raise InputError("Invalid deadline year! Must be a numerical value!\n")

    @staticmethod
    def validate_grade_value(grade_value):
        if len(str(grade_value)) == 0:
            raise InputError("Grade value cannot be empty!\n")
        try:
            float(grade_value)
        except ValueError:
            raise InputError("Invalid grade value! Must be a numerical value!\n")
