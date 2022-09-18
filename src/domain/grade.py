class Grade:
    """
    Class that represents an Grade by assignment ID, student ID and grade value
    """
    def __init__(self, assignment_id, student_id, grade_value=-1):
        """
        Constructor for Assignment class
        :param assignment_id: ID of the assignment, integer
        :param student_id: ID of the student, integer
        :param grade_value: group of the assignment, integer, initially -1
        """
        self.__assignment_id = assignment_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def assignment_id(self):
        return self.__assignment_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, new_grade_value):
        self.__grade_value = new_grade_value

    def __eq__(self, other):
        """
        :param other: another Grade
        :return: True if the two Grade entities are equal, False otherwise
        """
        return isinstance(other, Grade) and int(self.assignment_id) == int(other.assignment_id) and int(self.student_id == other.student_id)

    def __str__(self):
        """
        :return: string representation of a Grade
        """
        grade = self.grade_value
        if float(self.grade_value) == -1:
            grade = "Not graded yet"
        return f"   Assignment ID: {self.assignment_id}, Student ID: {self.student_id}, Grade value: {grade}"
