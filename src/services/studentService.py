from domain.student import Student
from random import shuffle, randint


class StudentService:
    """
    Service class for the StudentRepository class
    """
    def __init__(self, student_repo, student_val):
        """
        Constructor for StudentService class
        :param student_repo: student repository
        :param student_val: student validator
        """
        self.__student_repo = student_repo
        self.__student_val = student_val

    @property
    def repo(self):
        return self.__student_repo

    @property
    def students(self):
        """
        :return: list of all students from the repository
        """
        return self.__student_repo.get_all_students()

    def generate_students_list(self):
        """
        Randomly generates a list of students and populates the repository
        :return:
        """
        name_choices = ['Diana', 'Mihai', 'Roxana', 'Agata', 'Amalia', 'Luca', 'Nadia', 'Marian', 'Teona', 'Cosmin',
                        'Mircea', 'Liviu', 'Tudor', 'Matei', 'Ioana', 'Irina', 'Elena', 'Daria', 'Claudiu', 'Vlad']
        for i in range(1, 21):
            student_id = int(i)
            shuffle(name_choices)
            name = name_choices[0]
            name_choices.pop(0)
            group = randint(911, 917)
            student = Student(student_id, name, group)
            self.__student_repo.add_student(student)

    def no_of_students(self):
        """
        :return: the number of students currently in the repository
        """
        return len(self.__student_repo.get_all_students())

    def add_student_run(self, student_id, name, group):
        """
        Creates a new student, validates it and adds it to the list of students using the add function from
        the repository
        :param student_id: ID of the student, integer
        :param name: name of student, string
        :param group: group of student, integer
        """
        student = Student(student_id, name, group)
        self.__student_val.validate_student(student)
        self.__student_repo.add_student(student)

    def remove_student_run(self, student_id):
        """
        Searches a student with <student_id> in the repository and if it exists, removes the student using
        the remove function from the repository
        :param student_id: ID of the student, integer
        """
        self.__student_repo.search_by_id(student_id)
        self.__student_repo.remove_student_by_id(student_id)

    def update_student_name_run(self, student_id, new_name):
        """
        Updates a student's name using the update function from the repository
        :param student_id: ID of the student, integer
        :param new_name: new name of student, string
        """
        self.__student_repo.update_student_name(student_id, new_name)

    def update_student_group_run(self, student_id, new_group):
        """
        Updates a student's group using the update function from the repository
        :param student_id: ID of the student, integer
        :param new_group: new group of student, integer
        """
        self.__student_repo.update_student_group(student_id, new_group)
