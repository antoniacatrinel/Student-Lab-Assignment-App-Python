from exceptions.exceptions import UndoError


class UndoRedoService:
    """
    Class that handles undo/redo operations for the application
    """
    def __init__(self, student_service, assignment_service, grade_service):
        self.__student_service = student_service
        self.__assignment_service = assignment_service
        self.__grade_service = grade_service
        self.__command_stack_top = -1
        self.__command_stack = []
        self.__undo_dict = {"add_student": self.undo_add_student, "remove_student": self.undo_remove_student, "cascade_remove": self.undo_cascade_remove,
                            "update_student_name": self.undo_update_student_name, "update_student_group": self.undo_update_student_group, "add_assignment": self.undo_add_assignment, "remove_assignment": self.undo_remove_assignment,
                            "update_assignment_description": self.undo_update_assignment_description, "update_assignment_deadline": self.undo_update_assignment_deadline,
                            "give_student": self.undo_assign_to_student, "give_group": self.undo_cascade_assign_to_group,
                            "add_grade": self.undo_delete_grade, "grade_student": self.undo_grade_student}
        self.__redo_dict = {"add_student": self.redo_add_student, "remove_student": self.redo_remove_student, "cascade_remove": self.redo_cascade_remove,
                            "update_student_name": self.redo_update_student_name, "update_student_group": self.redo_update_student_group, "add_assignment": self.redo_add_assignment,
                            "remove_assignment": self.redo_remove_assignment, "update_assignment_description": self.redo_update_assignment_description,
                            "update_assignment_deadline": self.redo_update_assignment_deadline, "give_student": self.redo_assign_to_student,
                            "give_group": self.redo_assign_to_group, "add_grade": self.redo_delete_grade, "grade_student": self.redo_grade_student}

    def add_command_to_stack(self, action, object):
        """
        Adds a new operation to the stack
        """
        self.__command_stack_top += 1
        self.__command_stack.insert(self.__command_stack_top, [action, object])
        del self.__command_stack[self.__command_stack_top+1:]

    def get_last_operation(self):
        """
        Gets the last operation from the stack
        """
        operation = self.__command_stack[self.__command_stack_top]
        self.__command_stack_top -= 1
        return operation

    def get_stack(self):
        return self.__command_stack

    @staticmethod
    def get_last_operation_command(operation):
        return operation[0]

    @staticmethod
    def get_last_operation_object(operation):
        return operation[1]

    def get_next_operation(self):
        """
        Gets the next operation from the stack
        """
        operation = self.__command_stack[self.__command_stack_top+1]
        self.__command_stack_top += 1
        return operation

    def call_undo(self):
        """
        Method that handles the undo call
        :raises UndoError if there is no operation to undo
        """
        if self.__command_stack_top == -1:
            raise UndoError("No operation to undo!")
        last_operation = self.get_last_operation()
        action = self.get_last_operation_command(last_operation)
        object = self.get_last_operation_object(last_operation)
        self.__undo_dict[action](object)

    def undo_add_student(self, student):
        """
        Undoes the add student operation
        """
        self.__student_service.remove_student_run(student.student_id)

    def undo_add_assignment(self, assignment):
        """
        Undoes the add assignment operation
        """
        self.__assignment_service.remove_assignment_run(assignment.assignment_id)

    def undo_remove_student(self, student):
        """
        Undoes the remove student operation
        """
        self.__student_service.add_student_run(student.student_id, student.name, student.group)

    def undo_cascade_remove(self, operations):
        """
        Undoes the cascade remove operation
        """
        new_operations = operations[:]
        while len(new_operations) > 0:
            last_op = new_operations.pop()
            action = self.get_last_operation_command(last_op)
            object = self.get_last_operation_object(last_op)
            self.__undo_dict[action](object)

    def undo_remove_assignment(self, assignment):
        """
        Undoes the remove assignment operation
        """
        self.__assignment_service.add_assignment_run(assignment.assignment_id, assignment.description, assignment.deadline)

    def undo_update_student_name(self, param):
        """
        Undoes the update student name operation
        """
        student = param[0]
        stud_id = int(student.student_id)
        stud_name = student.name
        self.__student_service.update_student_name_run(stud_id, stud_name)

    def undo_update_student_group(self, param):
        """
        Undoes the update student group operation
        """
        student = param[0]
        student_id = int(student.student_id)
        group = int(student.group)
        self.__student_service.update_student_group_run(student_id, group)

    def undo_update_assignment_description(self, param):
        """
        Undoes the update assignment description operation
        """
        assignment = param[0]
        assignment_id = int(assignment.assignment_id)
        description = assignment.description
        self.__assignment_service.update_assignment_description_run(assignment_id, description)

    def undo_update_assignment_deadline(self, param):
        """
        Undoes the update assignment deadline operation
        """
        assignment = param[0]
        assignment_id = int(assignment.assignment_id)
        deadline = assignment.deadline
        self.__assignment_service.update_assignment_deadline_run(assignment_id, deadline)

    def undo_delete_grade(self, grade):
        """
        Undoes the delete grade operation
        """
        self.__grade_service.repo.add_grade(grade)

    def undo_assign_to_student(self, grade):
        """
        Undoes the assign to student operation
        """
        assignment_id = grade.assignment_id
        student_id = grade.student_id
        self.__grade_service.remove_assign_to_student(assignment_id, student_id)

    def undo_cascade_assign_to_group(self, operations):
        """
        Undoes the cascading assign to group operation
        """
        new_operations = operations[:]
        while len(new_operations) > 0:
            last_op = new_operations.pop()
            action = self.get_last_operation_command(last_op)
            object = self.get_last_operation_object(last_op)
            self.__undo_dict[action](object)

    def undo_grade_student(self, param):
        """
        Undoes the grade student operation
        """
        grade = param[0]
        assignment_id = grade.assignment_id
        student_id = grade.student_id
        self.__grade_service.ungrade_student(assignment_id, student_id)

    def call_redo(self):
        """
        Method that handles the redo call
        :raises UndoError if there is no operation to redo
        """
        if self.__command_stack_top == len(self.__command_stack) - 1:
            raise UndoError("No operation to redo!")
        next_operation = self.get_next_operation()
        action = self.get_last_operation_command(next_operation)
        object = self.get_last_operation_object(next_operation)
        self.__redo_dict[action](object)

    def redo_add_student(self, student):
        """
        Redoes the add student operation
        """
        self.undo_remove_student(student)

    def redo_add_assignment(self, assignment):
        """
        Redoes the add student operation
        """
        self.undo_remove_assignment(assignment)

    def redo_remove_student(self, student):
        """
        Redoes the remove student operation
        """
        self.undo_add_student(student)

    def redo_cascade_remove(self, operations):
        """
        Redoes the cascade remove operation
        """
        for op in operations:
            action = self.get_last_operation_command(op)
            object = self.get_last_operation_object(op)
            self.__redo_dict[action](object)

    def redo_remove_assignment(self, assignment):
        """
        Redoes the remove assignment operation
        """
        self.undo_add_assignment(assignment)

    def redo_update_student_name(self, param):
        """
        Redoes the update student name operation
        """
        student = param[1]
        self.__student_service.update_student_name_run(student.student_id, student.name)

    def redo_update_student_group(self, param):
        """
        Redoes the update student group operation
        """
        student = param[1]
        self.__student_service.update_student_group_run(student.student_id, student.group)

    def redo_update_assignment_description(self, param):
        """
        Redoes the update assignment description operation
        """
        assignment = param[1]
        self.__assignment_service.update_assignment_description_run(assignment.assignment_id, assignment.description)

    def redo_update_assignment_deadline(self, param):
        """
        Redoes the update assignment deadline operation
        """
        assignment = param[1]
        self.__assignment_service.update_assignment_deadline_run(assignment.assignment_id, assignment.deadline)

    def redo_assign_to_student(self, grade):
        """
        Redoes the assign to student operation
        """
        assignment_id = grade.assignment_id
        student_id = grade.student_id
        self.__grade_service.assign_to_student(assignment_id, student_id)

    def redo_assign_to_group(self, operations):
        """
        Redoes the assign to group operation
        """
        for op in operations:
            action = self.get_last_operation_command(op)
            object = self.get_last_operation_object(op)
            self.__redo_dict[action](object)

    def redo_grade_student(self, param):
        """
        Redoes the grade student operation
        """
        grade = param[1]
        assignment_id = grade.assignment_id
        student_id = grade.student_id
        grade_value = grade.grade_value
        self.__grade_service.grade_student(student_id, assignment_id, grade_value)

    def redo_delete_grade(self, grade):
        """
        Redoes the delete grade operation
        """
        self.__grade_service.repo.remove_grade(grade)
