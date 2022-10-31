class Assignment:
    """
    Class that represents an Assignment by ID, description and deadline
    """
    def __init__(self, assignment_id, description, deadline):
        """
        Constructor for Assignment class
        :param assignment_id: ID of the assignment, integer
        :param description: description of the assignment, string
        :param deadline: group of the assignment, string
        """
        self.__assignment_id = assignment_id
        self.__description = description
        self.__deadline = deadline

    @property
    def assignment_id(self):
        """
        :return: ID of the assignment
        """
        return self.__assignment_id

    @property
    def description(self):
        """
        :return: description of the assignment
        """
        return self.__description

    @property
    def deadline(self):
        """
        :return: deadline of the assignment
        """
        return self.__deadline

    @description.setter
    def description(self, new_description):
        """
        Sets the description of an assignment to a given value
        """
        self.__description = new_description

    @deadline.setter
    def deadline(self, new_deadline):
        """
        Sets the deadline of an assignment to a given value
        """
        self.__deadline = new_deadline

    def __eq__(self, other):
        """
        Checks if two Assignment entities are equal
        :param other: another Assignment
        :return: True if the two Assignment entities are equal, False otherwise
        """
        return isinstance(other, Assignment) and int(self.assignment_id) == int(other.assignment_id)

    def __str__(self):
        """
        :return: string representation of an Assignment
        """
        return f"   Assignment ID: {self.assignment_id}, Description: {self.description}, Deadline: {self.deadline}"
