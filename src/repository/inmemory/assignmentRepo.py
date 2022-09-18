from domain.assignment import Assignment
from exceptions.exceptions import RepositoryError
from utils.utils import IterableStructure


class AssignmentRepository:
    """
    Class that represents an assignment repository
    """
    def __init__(self):
        """
        Constructor for AssignmentRepository class
        """
        self._assignment_data = IterableStructure()

    def get_all_assignments(self):
        """
        :return: the list of all assignments
        """
        return self._assignment_data

    def search_by_id(self, assign_id):
        """
        Searches an assignment by given ID (assign_id)
        :param assign_id: ID of the searched assignment, integer
        :return: Assignment if found
        :raises: RepositoryError in case of nonexistent assignment
         """
        ok = True
        for _assign in self._assignment_data:
            if int(_assign.assignment_id) == int(assign_id):
                return _assign
        if ok:
            raise RepositoryError("Nonexistent assignment id!\n")

    def add_assignment(self, new_assignment):
        """
        Adds a new assignment to the list of assignments
        :param new_assignment: new assignment, Assignment
        :raises: RepositoryError in case of already existent assignment
        """
        for assign in self._assignment_data:
            if int(assign.assignment_id) == int(new_assignment.assignment_id):
                raise RepositoryError("Duplicate assignment id!\n")
        self._assignment_data.append(new_assignment)

    def remove_assignment_by_id(self, assign_id):
        """
        Removes an assignment by ID (assign_id) from the list of assignments
        :param assign_id: ID of the assignment, integer
        """
        for i in range(len(self._assignment_data)):
            _assign = self._assignment_data[i]
            if int(_assign.assignment_id) == int(assign_id):
                self._assignment_data.__delitem__(i)
                return

    def update_assignment_description(self, assign_id, new_description):
        """
        Updates the description of the assignment having ID <assign_id> with <new_description>
        :param assign_id: ID of the assignment, integer
        :param new_description: new description, string
        :raises: RepositoryError in case of nonexistent assignment
        """
        ok = False
        for i in range(len(self._assignment_data)):
            _assign = self._assignment_data[i]
            if int(_assign.assignment_id) == int(assign_id):
                new_assign = Assignment(assign_id, new_description, _assign.deadline)
                self._assignment_data.__setitem__(i, new_assign)  # or setattr(stud, 'name', new_name) - builtins
                ok = True
        if ok is False:
            raise RepositoryError("Nonexistent assignment id!\n")

    def update_assignment_deadline(self, assign_id, new_deadline):
        """
        Updates the deadline of the assignment having ID <assign_id> with <new_deadline>
        :param assign_id: ID of the assignment, integer
        :param new_deadline: new deadline, string
        :raises: RepositoryError in case of nonexistent assignment
        """
        ok = False
        for i in range(len(self._assignment_data)):
            _assign = self._assignment_data[i]
            if int(_assign.assignment_id) == int(assign_id):
                new_assign = Assignment(assign_id, _assign.description, new_deadline)
                self._assignment_data.__setitem__(i, new_assign)              # or setattr(stud, 'group', new_group) - builtins
                ok = True
        if ok is False:
            raise RepositoryError("Nonexistent assignment id!\n")
