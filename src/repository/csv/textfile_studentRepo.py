from src.domain.student import Student
from src.repository.inmemory.studentRepo import StudentRepository


class StudentTextFileRepository(StudentRepository):
    """
    Class that represents a student repository that uses text files for persistent storage
    """
    def __init__(self, file_name):
        """
        Constructor for StudentTextFileRepository class
        :param file_name: path to file for storage
        """
        StudentRepository.__init__(self)
        self.__file_name = file_name

    def _read_all_from_file(self):
        """
        Reads lines from the students file and converts them into Student objects
        """
        f = open(self.__file_name, "rt")
        self._student_data.clear()
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                student_id, name, group = line.split(sep=",", maxsplit=2)
                stud = Student(int(student_id), name, int(group))
                self._student_data.append(stud)
        f.close()

    def _append_to_file(self, new_student):
        """
        Appends a new line to file
        """
        f = open(self.__file_name, "at")
        f.write(str(new_student.student_id) + "," + new_student.name + "," + str(new_student.group) + "\n")
        f.close()

    def _write_all_to_file(self):
        """
        Saves all students to file
        """
        f = open(self.__file_name, "wt")
        for student in self._student_data:
            f.write(str(student.student_id) + "," + student.name + "," + str(student.group) + "\n")
        f.close()

    def get_all_students(self):
        """
        Gets all students from the file
        """
        self._read_all_from_file()
        return StudentRepository.get_all_students(self)

    def search_by_id(self, stud_id):
        """
        Searches a student by ID
        :param stud_id: ID of the student, integer
        """
        self._read_all_from_file()
        return StudentRepository.search_by_id(self, stud_id)

    def add_student(self, new_student):
        """
        Adds a new student to the list of students
        :param new_student: a new student, Student
        """
        self._read_all_from_file()
        StudentRepository.add_student(self, new_student)
        self._append_to_file(new_student)

    def remove_student_by_id(self, stud_id):
        """
        Removes a student by ID (stud_id) from the list of students
        :param stud_id: ID of the student, integer
        """
        self._read_all_from_file()
        StudentRepository.remove_student_by_id(self, stud_id)
        self._write_all_to_file()

    def update_student_name(self, stud_id, new_name):
        """
        Updates the name of the student having ID <stud_id> with <new_name>
        :param stud_id: ID of the student, integer
        :param new_name: new name, string
        """
        self._read_all_from_file()
        StudentRepository.update_student_name(self, stud_id, new_name)
        self._write_all_to_file()

    def update_student_group(self, stud_id, new_group):
        """
        Updates the group of the student having ID <stud_id> with <new_group>
        :param stud_id: ID of the student,integer
        :param new_group: new group, integer
        """
        self._read_all_from_file()
        StudentRepository.update_student_group(self, stud_id, new_group)
        self._write_all_to_file()
