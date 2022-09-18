from domain.assignment import Assignment
from repository.inmemory.assignmentRepo import AssignmentRepository


class AssignmentTextFileRepository(AssignmentRepository):
    """
    Class that represents an assignment repository that uses text files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for AssignmentTextFileRepository class
        :param file_name: path to file for storage
        """
        AssignmentRepository.__init__(self)
        self.__file_name = file_name

    def _read_all_from_file(self):
        """
        Reads lines from the file and converts them into Assignment objects
        """
        f = open(self.__file_name, "rt")
        self._assignment_data.clear()
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                assignment_id, description, deadline = line.split(sep=",", maxsplit=2)
                assign = Assignment(int(assignment_id), description, deadline)
                self._assignment_data.append(assign)
        f.close()

    def _append_to_file(self, new_assignment):
        """
        Appends a new line to file
        """
        f = open(self.__file_name, "at")
        f.write(str(new_assignment.assignment_id) + "," + new_assignment.description + "," + str(new_assignment.deadline) + "\n")
        f.close()

    def _write_all_to_file(self):
        """
        Saves all assignments to file
        """
        f = open(self.__file_name, "wt")
        for assignment in self._assignment_data:
            f.write(str(assignment.assignment_id) + "," + assignment.description + "," + str(assignment.deadline) + "\n")
        f.close()

    def get_all_assignments(self):
        """
        Gets all assignments from the file
        """
        self._read_all_from_file()
        return AssignmentRepository.get_all_assignments(self)

    def search_by_id(self, assign_id):
        """
        Searches an assignment by given ID (assign_id)
        :param assign_id: ID of the searched assignment, integer
        :return: Assignment if found
        """
        self._read_all_from_file()
        return AssignmentRepository.search_by_id(self, assign_id)

    def add_assignment(self, new_assignment):
        """
        Adds a new assignment to the list of assignments
        :param new_assignment: new assignment, Assignment
        """
        self._read_all_from_file()
        AssignmentRepository.add_assignment(self, new_assignment)
        self._append_to_file(new_assignment)

    def remove_assignment_by_id(self, assign_id):
        """
        Removes an assignment by ID (assign_id) from the list of assignments
        :param assign_id: ID of the assignment, integer
        """
        self._read_all_from_file()
        AssignmentRepository.remove_assignment_by_id(self, assign_id)
        self._write_all_to_file()

    def update_assignment_description(self, assign_id, new_description):
        """
        Updates the description of the assignment having ID <assign_id> with <new_description>
        :param assign_id: ID of the assignment, integer
        :param new_description: new description, string
        """
        self._read_all_from_file()
        AssignmentRepository.update_assignment_description(self, assign_id, new_description)
        self._write_all_to_file()

    def update_assignment_deadline(self, assign_id, new_deadline):
        """
        Updates the deadline of the assignment having ID <assign_id> with <new_deadline>
        :param assign_id: ID of the assignment, integer
        :param new_deadline: new deadline, string
        """
        self._read_all_from_file()
        AssignmentRepository.update_assignment_deadline(self, assign_id, new_deadline)
        self._write_all_to_file()
