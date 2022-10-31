class Student:
    """
    Class that represents a Student by ID, name and group
    """
    def __init__(self, student_id, name, group):
        """
        Constructor for Student class
        :param student_id: ID of the student, integer
        :param name: name of the student, string
        :param group: group of the student, integer
        """
        self.__student_id = student_id
        self.__name = name
        self.__group = group

    @property
    def student_id(self):
        """
        :return: ID of the student
        """
        return self.__student_id

    @property
    def name(self):
        """
        :return: name of the student
        """
        return self.__name

    @property
    def group(self):
        """
        :return: group of the student
        """
        return self.__group

    @name.setter
    def name(self, new_name):
        """
        Sets the name of a student to a given value
        """
        self.__name = new_name

    @group.setter
    def group(self, new_group):
        """
        Sets the group of a student to a given value
        """
        self.__group = new_group

    def __eq__(self, other):
        """
        Checks if two Student entities are equal
        :param other: another Student
        :return: True if the two Student entities are equal, False otherwise
        """
        return isinstance(other, Student) and int(self.student_id) == int(other.student_id)

    def __str__(self):
        """
        :return: string representation of a Student
        """
        return f"   Student ID: {self.student_id}, Name: {self.name}, Group: {self.group}"
