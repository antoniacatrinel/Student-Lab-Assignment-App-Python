from domain.assignment import Assignment
from domain.grade import Grade
from domain.student import Student
from exceptions.exceptions import ValidationError, RepositoryError, InputError, UndoError
from validation.validators import ValidatorInput
import datetime


class Ui:
    """
    Class that represents the console user interface of the application
    """
    def __init__(self, student_service, assignment_service, grade_service, undo_service, inmemory):
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._validinput = ValidatorInput()
        self._undo_redo_service = undo_service
        self._inmemory = inmemory

    def ui_add_student(self):
        """
        Method that gets student_id, name and group from user, validates them and calls function from service in order
        to add the student to the list of students
        """
        student_id = input("Input student id: ")
        self._validinput.validate_student_id(student_id)
        name = input("Input student name: ")
        self._validinput.validate_student_name(name)
        group = input("Input student group: ")
        self._validinput.validate_student_group(group)
        self._student_service.add_student_run(student_id, name, group)
        self._undo_redo_service.add_command_to_stack("add_student", Student(student_id, name, group))
        print("Student added successfully!\n")

    def ui_remove_student(self):
        """
        Method that gets student_id from user, validates it and calls function from service in order to remove student
        with <student_id> from the list of students
        """
        student_id = input("Input student id: ")
        self._validinput.validate_student_id(student_id)
        student = self._student_service.repo.search_by_id(student_id)
        self._student_service.remove_student_run(student_id)
        undo_list = []
        undo_list = list(self._grade_service.remove_student_and_assignments(student, student_id, undo_list))  # cascade remove
        undo_list.append(["remove_student", student])
        self._undo_redo_service.add_command_to_stack("cascade_remove", undo_list)
        print("Student removed successfully!\n")

    def ui_update_student(self):
        """
        Method that gets student_id and update option (name, group) from user, validates it and calls function from service
        in order to update student with <student_id> from the list of students
        """
        student_id = input("Input id of student you want to update: ")
        self._validinput.validate_student_id(student_id)
        try:
            self._student_service.repo.search_by_id(student_id)
        except RepositoryError as re:
            raise RepositoryError(re)
        old_student = self._student_service.repo.search_by_id(student_id)
        user_input = input("What do you want to update? ")
        user_input = user_input.strip().lower()
        if user_input == 'name':
            new_name = input("Input student's new name: ")
            self._validinput.validate_student_name(new_name)
            param = list()
            param.append(Student(student_id, old_student.name, old_student.group))
            param.append(Student(student_id, new_name, old_student.group))
            self._undo_redo_service.add_command_to_stack("update_student_name", param)
            self._student_service.update_student_name_run(student_id, new_name)
            print("Student name updated successfully!\n")
        elif user_input == 'group':
            new_group = input("Input student's new group: ")
            self._validinput.validate_student_group(new_group)
            param = list()
            param.append(Student(student_id, old_student.name, old_student.group))
            param.append(Student(student_id, old_student.name, new_group))
            self._undo_redo_service.add_command_to_stack("update_student_group", param)
            self._student_service.update_student_group_run(student_id, new_group)
            print("Student group updated successfully!\n")
        else:
            raise InputError("Invalid attribute! You can only update a student's name or group!\n")

    def ui_list_students(self):
        """
        Method that displays the list of students
        """
        no = self._student_service.no_of_students()
        if int(no) == 0:
            print("No students in the list!")
        else:
            print("List of students contains " + str(no) + " students:")
            for stud in self._student_service.students:
                print(stud.__str__())
        print()

    def ui_add_assignment(self):
        """
        Method that gets assignment_id, description and deadline day, month and year from user, validates them and calls
        function from service in order to add assignment to the list of assignments
        """
        assignment_id = input("Input assignment id: ")
        self._validinput.validate_assignment_id(assignment_id)
        description = input("Input assignment description: ")
        self._validinput.validate_assignment_description(description)
        deadline_day = input("Input deadline day: ")
        self._validinput.validate_deadline_day(deadline_day)
        deadline_month = input("Input deadline month: ")
        self._validinput.validate_deadline_month(deadline_month)
        deadline_year = input("Input deadline year: ")
        self._validinput.validate_deadline_year(deadline_year)

        deadline = datetime.datetime(int(deadline_year), int(deadline_month), int(deadline_day))
        deadline = deadline.strftime('%d/%m/%Y')
        self._assignment_service.add_assignment_run(assignment_id, description, deadline)
        self._undo_redo_service.add_command_to_stack("add_assignment", Assignment(assignment_id, description, deadline))
        print("Assignment added successfully!\n")

    def ui_remove_assignment(self):
        """
        Method that gets assignment_id from user, validates it and calls function from service in order to remove
        assignment with <assignment_id> from the list of assignments
        """
        assignment_id = input("Input assignment id: ")
        self._validinput.validate_assignment_id(assignment_id)
        assignment = self._assignment_service.repo.search_by_id(assignment_id)
        self._assignment_service.remove_assignment_run(assignment_id)
        undo_list = []
        undo_list = list(self._grade_service.remove_assignment_and_students(assignment, assignment_id, undo_list))  # cascade remove
        undo_list.append(["remove_assignment", assignment])
        self._undo_redo_service.add_command_to_stack("cascade_remove", undo_list)
        print("Assignment removed successfully!\n")

    def ui_update_assignment(self):
        """
        Method that gets assignment_id and update option (description, deadline) from user, validates it and calls
        function from service in order to update assignment with <assignment_id> from the list of assignments
        """
        assignment_id = input("Input id of assignment you want to update: ")
        self._validinput.validate_assignment_id(assignment_id)
        try:
            self._assignment_service.repo.search_by_id(assignment_id)
        except RepositoryError as re:
            raise RepositoryError(re)
        old_assignment = self._assignment_service.repo.search_by_id(assignment_id)
        user_input = input("What do you want to update? ")
        user_input = user_input.strip().lower()
        if user_input == 'description':
            new_desc = input("Input assignment's new description: ")
            self._validinput.validate_assignment_description(new_desc)
            param = list()
            param.append(Assignment(assignment_id, old_assignment.description, old_assignment.deadline))
            param.append(Assignment(assignment_id, new_desc, old_assignment.deadline))
            self._undo_redo_service.add_command_to_stack("update_assignment_description", param)
            self._assignment_service.update_assignment_description_run(assignment_id, new_desc)
            print("Assignment description updated successfully!\n")
        elif user_input == 'deadline':
            new_deadline_day = input("Input new deadline day: ")
            self._validinput.validate_deadline_day(new_deadline_day)
            new_deadline_month = input("Input new deadline month: ")
            self._validinput.validate_deadline_month(new_deadline_month)
            new_deadline_year = input("Input new deadline year: ")
            self._validinput.validate_deadline_year(new_deadline_year)

            new_deadline = datetime.datetime(int(new_deadline_year), int(new_deadline_month), int(new_deadline_day))
            new_deadline = new_deadline.strftime('%d/%m/%Y')
            param = list()
            param.append(Assignment(assignment_id, old_assignment.description, old_assignment.deadline))
            param.append(Assignment(assignment_id, old_assignment.description, new_deadline))
            self._undo_redo_service.add_command_to_stack("update_assignment_deadline", param)
            self._assignment_service.update_assignment_deadline_run(assignment_id, new_deadline)
            print("Assignment deadline updated successfully!\n")
        else:
            raise InputError("Invalid attribute! You can only update an assignment's description or deadline!\n")

    def ui_list_assignments(self):
        """
        Method that displays the list of assignments
        """
        no = self._assignment_service.no_of_assignments()
        if int(no) == 0:
            print("No assignments in the list!")
        else:
            print("List of assignments contains " + str(no) + " assignments:")
            for assign in self._assignment_service.assignments:
                print(assign.__str__())
        print()

    def ui_list_given(self):
        """
        Method that displays the list of given assignments & grades
        """
        no = self._grade_service.no_of_grades()
        if int(no) == 0:
            print("No grades in the list!")
        else:
            print("List of given assignments contains " + str(no) + " assignments:")
            for grade in self._grade_service.grades:
                print(grade.__str__())
        print()

    def ui_list_not_graded(self, stud_id):
        """
        Method that displays the list of ungraded assignments of a student with ID <stud_id>
        """
        cnt = 0
        for grade in self._grade_service.grades:
            if int(grade.student_id) == int(stud_id) and float(grade.grade_value) == -1:
                if int(cnt) == 0:
                    print("Student's list of ungraded assignments:")
                print(grade.__str__())
                cnt += 1
        if int(cnt) == 0:
            raise RepositoryError("Student does not have any ungraded assignments!")
        print()

    def ui_give_assignment_to_student(self):
        """
        Method that gives an assignment to a student
        """
        assignment_id = input("Input id of assignment you want to give: ")
        self._validinput.validate_assignment_id(assignment_id)
        try:
            self._assignment_service.repo.search_by_id(assignment_id)
        except RepositoryError:
            raise RepositoryError("Nonexistent assignment id!\n")
        student_id = input("Input student id: ")
        self._validinput.validate_student_id(student_id)
        try:
            self._student_service.repo.search_by_id(student_id)
        except RepositoryError:
            raise RepositoryError("Nonexistent student id!\n")
        self._grade_service.assign_to_student(assignment_id, student_id)
        self._undo_redo_service.add_command_to_stack("give_student", Grade(assignment_id, student_id))
        print("Assignment given successfully!\n")

    def ui_give_assignment_to_group(self):
        """
        Method that gives an assignment to a group of students
        """
        assignment_id = input("Input id of assignment you want to give: ")
        self._validinput.validate_assignment_id(assignment_id)
        try:
            self._assignment_service.repo.search_by_id(assignment_id)
        except RepositoryError:
            raise RepositoryError("Nonexistent assignment id!\n")
        group = input("Input group: ")
        self._validinput.validate_student_group(group)
        undo_list = self._grade_service.assign_to_group(assignment_id, group)
        self._undo_redo_service.add_command_to_stack("give_group", undo_list)
        print("Assignment given successfully!\n")

    def ui_grade_student(self):
        """
        Method that grades a student for an assignment
        """
        student_id = input("Input id of student you want to grade: ")
        self._validinput.validate_student_id(student_id)
        self.ui_list_not_graded(student_id)
        print("Please select an assignment from list!")
        assignment_id = input("Input id of assignment you want to grade: ")
        self._validinput.validate_assignment_id(assignment_id)
        grade_value = input("Input value of grade: ")
        self._validinput.validate_grade_value(grade_value)
        self._grade_service.grade_student(student_id, assignment_id, grade_value)
        param = list()
        param.append(Grade(assignment_id, student_id))
        param.append(Grade(assignment_id, student_id, grade_value))
        self._undo_redo_service.add_command_to_stack("grade_student", param)
        print("Student graded successfully!\n")

    def ui_statistics_assignment(self):
        """
        Method that displays statistics for a certain assignment
        """
        assignment_id = input("Input id of given assignment: ")
        self._validinput.validate_assignment_id(assignment_id)
        statistics = list(self._grade_service.create_list_of_given_assignment_ordered(assignment_id))
        self.print_statistics_assignment(assignment_id, statistics)

    def print_statistics_assignment(self, assignment_id, statistics):
        """
        Method that prints the statistics for a certain assignment
        """
        if len(statistics) == 0:
            print("No students who received assignment " + str(assignment_id) + " !")
            return
        print("List of all students who received assignment " + str(assignment_id) + " ordered descending by grade:")
        for statistic in statistics:
            if float(statistic.grade_value) == -1:
                statistic.grade_value = "Not graded yet"
            student = self._student_service.repo.search_by_id(statistic.student_id)
            print("  Student id: " + str(student.student_id) + ", Student name: " + str(student.name)
                  + ", Grade: " + str(statistic.grade_value))

    def print_statistics_late(self, list_late):
        """
        Method that prints all late assignments
        """
        if len(list_late) == 0:
            print("No students who are late in handing in any assignment!")
            return
        print("List of all students who are late in handing in at least one assignment:")
        for i in range(0, len(list_late)):
            stud_id = list_late[int(i)]['id']
            student = self._student_service.repo.search_by_id(stud_id)
            print("  Student id: " + str(list_late[int(i)]['id']) + ", Student name: " + str(student.name)
                  + ", Number of late assignments: " + str(list_late[int(i)]['ungraded']))

    def print_statistics_best(self, list_best_situation):
        """
        Method that prints the statistics of the best school situation
        """
        print("List of students with the best school situation, sorted in descending order of the average grade:")
        for i in range(0, len(list_best_situation)):
            stud_id = list_best_situation[int(i)]['id']
            student = self._student_service.repo.search_by_id(stud_id)
            print("  Student id: " + str(list_best_situation[int(i)]['id']) + ", Student name: " + str(student.name)
                  + ", Average grade: " + str(list_best_situation[int(i)]['grade']))

    def ui_statistics_late(self):
        """
        Method that prints the statistics of the late assignments
        """
        list_late = list(self._grade_service.create_list_of_late_students())
        self.print_statistics_late(list_late)

    def ui_statistics_best_school_situation(self):
        """
        Method that prints the statistics of the best school situation
        """
        list_best_situation = list(self._grade_service.create_list_of_best_school_situation())
        self.print_statistics_best(list_best_situation)

    def ui_undo_last_op(self):
        """
        Method that handles the undo operation functionality
        """
        self._undo_redo_service.call_undo()
        print("Operation undone successfully!\n")

    def ui_redo_last_op(self):
        """
        Method that handles the redo operation functionality
        """
        self._undo_redo_service.call_redo()
        print("Operation redone successfully!\n")

    @staticmethod
    def print_menu():
        print("Menu:")
        print("Student commands:")
        print("  Type 'add_student' to add a student to the list of students")
        print("  Type 'remove_student' to remove a student from the list of students")
        print("  Type 'update_student' to update the list of students")
        print("  Type 'list_students' to display list of students")
        print("-" * 70)
        print("Assignment commands:")
        print("  Type 'add_assignment' to add an assignment to the list of assignments")
        print("  Type 'remove_assignment' to remove an assignment from the list of assignments")
        print("  Type 'update_assignment' to update the list of assignments")
        print("  Type 'list_assignments' to display the list of assignments")
        print("-" * 70)
        print("Assigning/grading commands:")
        print("  Type 'give_student' to give a certain assignment to a student")
        print("  Type 'give_group' to give a certain assignment to a group of students")
        print("  Type 'grade_student' to grade a student for a certain assignment")
        print("  Type 'list_given' to list all assignments given & grades")
        print("-" * 70)
        print("Statistics commands:")
        print("  Type 'stat_assignment' to list all students who received a given assignment, ordered descending by grade")
        print("  Type 'stat_late' to list all students who are late in handing in at least one assignment")
        print("  Type 'stat_best' to list students with the best school situation, sorted in descending order of the \n"
              "average grade received for all graded assignments")
        print("-" * 70)
        print("Undo/redo commands:")
        print("  Type 'undo' to undo last performed operation")
        print("  Type 'redo' to redo last performed operation")
        print("-" * 70)
        print("Utilities:")
        print("  Type 'help' to view menu")
        print("  Type 'exit' to exit application")

    def start(self):
        if self._inmemory is True:
            self._student_service.generate_students_list()
            self._assignment_service.generate_assignments_list()
            self._grade_service.generate_grades_list()
        self.print_menu()
        while True:
            option = input("Option: ").strip().lower()
            if option == "":
                continue
            elif option == "help":
                self.print_menu()
            elif option == 'exit':
                return
            elif option == 'add_student':
                try:
                    self.ui_add_student()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'add_assignment':
                try:
                    self.ui_add_assignment()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'remove_student':
                try:
                    self.ui_remove_student()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'remove_assignment':
                try:
                    self.ui_remove_assignment()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'update_student':
                try:
                    self.ui_update_student()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'update_assignment':
                try:
                    self.ui_update_assignment()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'list_students':
                self.ui_list_students()
            elif option == 'list_assignments':
                self.ui_list_assignments()
            elif option == 'give_student':
                try:
                    self.ui_give_assignment_to_student()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'give_group':
                try:
                    self.ui_give_assignment_to_group()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'list_given':
                self.ui_list_given()
            elif option == 'grade_student':
                try:
                    self.ui_grade_student()
                except InputError as ie:
                    print("Input error: " + str(ie))
                except RepositoryError as re:
                    print("Repository error: " + str(re))
                except ValidationError as ve:
                    print("Validation error: " + str(ve))
            elif option == 'stat_assignment':
                try:
                    self.ui_statistics_assignment()
                except RepositoryError as re:
                    print("Repository error: " + str(re))
            elif option == 'stat_late':
                try:
                    self.ui_statistics_late()
                except RepositoryError as re:
                    print("Repository error: " + str(re))
            elif option == 'stat_best':
                try:
                    self.ui_statistics_best_school_situation()
                except RepositoryError as re:
                    print("Repository error: " + str(re))
            elif option == 'undo':
                try:
                    self.ui_undo_last_op()
                except UndoError as ue:
                    print("Undo error: " + str(ue))
            elif option == 'redo':
                try:
                    self.ui_redo_last_op()
                except UndoError as ue:
                    print("Undo error: " + str(ue))
            else:
                print("Invalid option!\n")
