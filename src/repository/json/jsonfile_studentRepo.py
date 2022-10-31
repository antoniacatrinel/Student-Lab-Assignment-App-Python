import json

from src.domain.student import Student
from src.repository.inmemory.studentRepo import StudentRepository


class StudentJsonFileRepository(StudentRepository):
    """
    Class that represents a student repository that uses json files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for StudentJsonFileRepository class
        :param file_name: path to file for storage
        """
        StudentRepository.__init__(self)
        self.__file_name = file_name

    def __read_all_from_file(self):
        """
        Reads lines from the students file and converts them into Student objects
        """
        f = open(self.__file_name, "r")
        self._student_data.clear()
        students = json.loads(f.read())
        for student in students:
            stud = Student(int(student["student_id"]), student["name"], int(student["group"]))
            self._student_data.append(stud)
        f.close()

    def __write_all_to_file(self):
        """
        Saves all students to file
        """
        f = open(self.__file_name, "w")
        students = []
        for student in self._student_data:
            student = {"student_id": student.student_id, "name": student.name, "group": student.group}
            students.append(student)
        json.dump(students, f)
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
