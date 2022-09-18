from domain.assignment import Assignment
from datetime import datetime
from random import randint


class AssignmentService:
    """
    Service class for the AssignmentRepository class
    """
    def __init__(self, assignment_repo, assignment_val):
        """
        Constructor for AssignmentService class
        :param assignment_repo: assignment repository
        :param assignment_val: assignment validator
        """
        self.__assignment_repo = assignment_repo
        self.__assignment_val = assignment_val

    @property
    def repo(self):
        return self.__assignment_repo

    @property
    def assignments(self):
        """
        :return: list of all assignments from the repository
        """
        return self.__assignment_repo.get_all_assignments()

    def generate_assignments_list(self):
        """
        Randomly generates a list of assignments and populates the repository
        :return:
        """
        for i in range(1, 21):
            deadline = datetime(randint(2021, 2022), randint(1, 12), randint(1, 28))
            assignment = Assignment(int(i), 'problem ' + str(i), deadline.strftime('%d/%m/%Y'))
            self.__assignment_repo.add_assignment(assignment)

    def no_of_assignments(self):
        """
        :return: the number of assignments currently in the repository
        """
        return len(self.__assignment_repo.get_all_assignments())

    def add_assignment_run(self, assignment_id, description, deadline):
        """
        Creates a new assignment, validates it and adds it to the list of assignments using the add function from
        the repository
        :param assignment_id: ID of the assignment, integer
        :param description: description of assignment, string
        :param deadline: deadline of assignment, string
        """
        assignment = Assignment(assignment_id, description, deadline)
        self.__assignment_val.validate_assignment(assignment)
        self.__assignment_repo.add_assignment(assignment)

    def remove_assignment_run(self, assign_id):
        """
        Searches a assignment with <assign_id> in the repository and if it exists, removes the assignment using
        the remove function from the repository
        :param assign_id: ID of the assignment, integer
        """
        self.__assignment_repo.search_by_id(assign_id)
        self.__assignment_repo.remove_assignment_by_id(assign_id)

    def update_assignment_description_run(self, assign_id, new_description):
        """
        Updates a assignment's description using the update function from the repository
        :param assign_id: ID of the assignment, integer
        :param new_description: new description of assignment, string
        """
        self.__assignment_repo.update_assignment_description(assign_id, new_description)

    def update_assignment_deadline_run(self, assign_id, new_deadline):
        """
        Updates a assignment's deadline using the update function from the repository
        :param assign_id: ID of the assignment, integer
        :param new_deadline: new deadline of assignment, string
        """
        self.__assignment_repo.update_assignment_deadline(assign_id, new_deadline)
