from domain.assignment import Assignment
from repository.inmemory.assignmentRepo import AssignmentRepository
import pickle
from random import randint
from datetime import datetime
import os


class AssignmentBinFileRepository(AssignmentRepository):
    """
    Class that represents an assignment repository that uses binary files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for AssignmentBinFileRepository class
        :param file_name: path to file for storage
        """
        AssignmentRepository.__init__(self)
        self.__file_name = file_name
        self.generate_assignments_list()

    def __read_all_from_file(self):
        """
        Reads lines from the file and converts them into Assignment objects
        """
        f = open(self.__file_name, "rb")
        try:
            self._assignment_data = pickle.load(f)
        except EOFError:
            pass
        f.close()

    def __write_all_to_file(self):
        """
        Saves all assignments to file
        """
        f = open(self.__file_name, "wb")
        pickle.dump(self._assignment_data, f)
        f.close()

    def get_all_assignments(self):
        """
        Gets all assignments from the file
        """
        self.__read_all_from_file()
        return AssignmentRepository.get_all_assignments(self)

    def search_by_id(self, assign_id):
        """
        Searches an assignment by given ID (assign_id)
        :param assign_id: ID of the searched assignment, integer
        :return: Assignment if found
        """
        self.__read_all_from_file()
        return AssignmentRepository.search_by_id(self, assign_id)

    def add_assignment(self, new_assignment):
        """
        Adds a new assignment to the list of assignments
        :param new_assignment: new assignment, Assignment
        """
        self.__read_all_from_file()
        AssignmentRepository.add_assignment(self, new_assignment)
        self.__write_all_to_file()

    def remove_assignment_by_id(self, assign_id):
        """
        Removes an assignment by ID (assign_id) from the list of assignments
        :param assign_id: ID of the assignment, integer
        """
        self.__read_all_from_file()
        AssignmentRepository.remove_assignment_by_id(self, assign_id)
        self.__write_all_to_file()

    def update_assignment_description(self, assign_id, new_description):
        """
        Updates the description of the assignment having ID <assign_id> with <new_description>
        :param assign_id: ID of the assignment, integer
        :param new_description: new description, string
        """
        self.__read_all_from_file()
        AssignmentRepository.update_assignment_description(self, assign_id, new_description)
        self.__write_all_to_file()

    def update_assignment_deadline(self, assign_id, new_deadline):
        """
        Updates the deadline of the assignment having ID <assign_id> with <new_deadline>
        :param assign_id: ID of the assignment, integer
        :param new_deadline: new deadline, string
        """
        self.__read_all_from_file()
        AssignmentRepository.update_assignment_deadline(self, assign_id, new_deadline)
        self.__write_all_to_file()

    def generate_assignments_list(self):
        """
        Generates a list of assignments and populates the file
        """
        filesize = os.path.getsize(self.__file_name)
        if filesize == 0:
            for i in range(1, 21):
                deadline = datetime(randint(2021, 2022), randint(1, 12), randint(1, 28))
                assignment = Assignment(int(i), 'problem ' + str(i), deadline.strftime('%d/%m/%Y'))
                self.add_assignment(assignment)
