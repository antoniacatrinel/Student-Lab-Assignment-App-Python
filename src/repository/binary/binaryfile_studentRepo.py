from domain.student import Student
from repository.inmemory.studentRepo import StudentRepository
import pickle
from random import shuffle, randint
import os


class StudentBinFileRepository(StudentRepository):
    """
    Class that represents a student repository that uses binary files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for StudentBinFileRepository class
        :param file_name: path to file for storage
        """
        StudentRepository.__init__(self)
        self.__file_name = file_name
        self.generate_students_list_and_save()

    def __read_all_from_file(self):
        """
        Reads lines from the students file and converts them into Student objects
        """
        f = open(self.__file_name, "rb")
        try:
            self._student_data = pickle.load(f)
        except EOFError:
            pass
        f.close()

    def __write_all_to_file(self):
        """
        Saves all students to file
        """
        f = open(self.__file_name, "wb")
        pickle.dump(self._student_data, f)
        f.close()

    def get_all_students(self):
        """
        Gets all students from the file
        """
        self.__read_all_from_file()
        return StudentRepository.get_all_students(self)

    def search_by_id(self, stud_id):
        """
        Searches a student by ID
        :param stud_id: ID of the student, integer
        """
        self.__read_all_from_file()
        return StudentRepository.search_by_id(self, stud_id)

    def add_student(self, new_student):
        """
        Adds a new student to the list of students
        :param new_student: a new student, Student
        """
        self.__read_all_from_file()
        StudentRepository.add_student(self, new_student)
        self.__write_all_to_file()

    def remove_student_by_id(self, stud_id):
        """
        Removes a student by ID (stud_id) from the list of students
        :param stud_id: ID of the student, integer
        """
        self.__read_all_from_file()
        StudentRepository.remove_student_by_id(self, stud_id)
        self.__write_all_to_file()

    def update_student_name(self, stud_id, new_name):
        """
        Updates the name of the student having ID <stud_id> with <new_name>
        :param stud_id: ID of the student, integer
        :param new_name: new name, string
        """
        self.__read_all_from_file()
        StudentRepository.update_student_name(self, stud_id, new_name)
        self.__write_all_to_file()

    def update_student_group(self, stud_id, new_group):
        """
        Updates the group of the student having ID <stud_id> with <new_group>
        :param stud_id: ID of the student,integer
        :param new_group: new group, integer
        """
        self.__read_all_from_file()
        StudentRepository.update_student_group(self, stud_id, new_group)
        self.__write_all_to_file()

    def generate_students_list_and_save(self):
        """
        Generates a list of students and populates the file
        """
        filesize = os.path.getsize(self.__file_name)
        if filesize == 0:
            name_choices = ['Diana', 'Mihai', 'Roxana', 'Agata', 'Amalia', 'Luca', 'Nadia', 'Marian', 'Teona', 'Cosmin',
                            'Mircea', 'Liviu', 'Tudor', 'Matei', 'Ioana', 'Irina', 'Elena', 'Daria', 'Claudiu', 'Vlad']
            for i in range(1, 21):
                student_id = int(i)
                shuffle(name_choices)
                name = name_choices[0]
                name_choices.pop(0)
                group = randint(911, 917)
                student = Student(student_id, name, group)
                self.add_student(student)
