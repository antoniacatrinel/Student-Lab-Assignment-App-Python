import os

from configparser import ConfigParser
from src.exceptions.exceptions import SettingsError
from src.repository.database.database_assignmentRepo import AssignmentDatabaseRepository
from src.repository.database.database_gradeRepo import GradeDatabaseRepository
from src.repository.database.database_studentRepo import StudentDatabaseRepository
from src.repository.inmemory.assignmentRepo import AssignmentRepository
from src.repository.inmemory.gradeRepo import GradeRepository
from src.repository.inmemory.studentRepo import StudentRepository
from src.repository.json.jsonfile_assignmentRepo import AssignmentJsonFileRepository
from src.repository.json.jsonfile_gradeRepo import GradeJsonFileRepository
from src.repository.json.jsonfile_studentRepo import StudentJsonFileRepository
from src.services.assignmentService import AssignmentService
from src.services.gradeService import GradeService
from src.services.studentService import StudentService
from src.services.undoRedoService import UndoRedoService
from src.ui.ui import Ui
from src.ui.gui import Gui
from src.validation.validators import ValidatorStudent, ValidatorAssignment, ValidatorGrade
from src.repository.csv.textfile_studentRepo import StudentTextFileRepository
from src.repository.csv.textfile_assignmentRepo import AssignmentTextFileRepository
from src.repository.csv.textfile_gradeRepo import GradeTextFileRepository
from src.repository.binary.binaryfile_studentRepo import StudentBinFileRepository
from src.repository.binary.binaryfile_assignmentRepo import AssignmentBinFileRepository
from src.repository.binary.binaryfile_gradeRepo import GradeBinFileRepository


class Settings:
    def __init__(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'settings.properties')
        parser = ConfigParser()
        parser.read(initfile)
        repo_style = parser.get("settings", "repository")
        students = parser.get("settings", "students")
        assignments = parser.get("settings", "assignments")
        grades = parser.get("settings", "grades")
        ui_style = parser.get("settings", "ui")

        if repo_style == "inmemory":
            valid_student = ValidatorStudent()
            valid_assignment = ValidatorAssignment()
            valid_grade = ValidatorGrade()

            student_repo = StudentRepository()
            assignment_repo = AssignmentRepository()
            grade_repo = GradeRepository()

            student_service = StudentService(student_repo, valid_student)
            assignment_service = AssignmentService(assignment_repo, valid_assignment)
            grade_service = GradeService(grade_repo, valid_grade, student_repo, assignment_repo)
            undo_redo_service = UndoRedoService(student_service, assignment_service, grade_service)

            if ui_style == "ui":
                self._ui = Ui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=True)
            elif ui_style == "gui":
                self._ui = Gui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=True)
            else:
                raise SettingsError("Invalid user interface!")

        elif repo_style == "textfiles":
            valid_student = ValidatorStudent()
            valid_assignment = ValidatorAssignment()
            valid_grade = ValidatorGrade()

            student_repo = StudentTextFileRepository(students)
            assignment_repo = AssignmentTextFileRepository(assignments)
            grade_repo = GradeTextFileRepository(grades)

            student_service = StudentService(student_repo, valid_student)
            assignment_service = AssignmentService(assignment_repo, valid_assignment)
            grade_service = GradeService(grade_repo, valid_grade, student_repo, assignment_repo)
            undo_redo_service = UndoRedoService(student_service, assignment_service, grade_service)

            if ui_style == "ui":
                self._ui = Ui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            elif ui_style == "gui":
                self._ui = Gui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            else:
                raise SettingsError("Invalid user interface!")

        elif repo_style == "binaryfiles":
            valid_student = ValidatorStudent()
            valid_assignment = ValidatorAssignment()
            valid_grade = ValidatorGrade()

            student_repo = StudentBinFileRepository(students)
            assignment_repo = AssignmentBinFileRepository(assignments)
            grade_repo = GradeBinFileRepository(grades)

            student_service = StudentService(student_repo, valid_student)
            assignment_service = AssignmentService(assignment_repo, valid_assignment)
            grade_service = GradeService(grade_repo, valid_grade, student_repo, assignment_repo)
            undo_redo_service = UndoRedoService(student_service, assignment_service, grade_service)

            if ui_style == "ui":
                self._ui = Ui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            elif ui_style == "gui":
                self._ui = Gui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            else:
                raise SettingsError("Invalid user interface!")

        elif repo_style == "jsonfiles":
            valid_student = ValidatorStudent()
            valid_assignment = ValidatorAssignment()
            valid_grade = ValidatorGrade()

            student_repo = StudentJsonFileRepository(students)
            assignment_repo = AssignmentJsonFileRepository(assignments)
            grade_repo = GradeJsonFileRepository(grades)

            student_service = StudentService(student_repo, valid_student)
            assignment_service = AssignmentService(assignment_repo, valid_assignment)
            grade_service = GradeService(grade_repo, valid_grade, student_repo, assignment_repo)
            undo_redo_service = UndoRedoService(student_service, assignment_service, grade_service)

            if ui_style == "ui":
                self._ui = Ui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            elif ui_style == "gui":
                self._ui = Gui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            else:
                raise SettingsError("Invalid user interface!")

        elif repo_style == "database":
            valid_student = ValidatorStudent()
            valid_assignment = ValidatorAssignment()
            valid_grade = ValidatorGrade()

            student_repo = StudentDatabaseRepository(students)
            assignment_repo = AssignmentDatabaseRepository(assignments)
            grade_repo = GradeDatabaseRepository(grades)

            student_service = StudentService(student_repo, valid_student)
            assignment_service = AssignmentService(assignment_repo, valid_assignment)
            grade_service = GradeService(grade_repo, valid_grade, student_repo, assignment_repo)
            undo_redo_service = UndoRedoService(student_service, assignment_service, grade_service)

            if ui_style == "ui":
                self._ui = Ui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            elif ui_style == "gui":
                self._ui = Gui(student_service, assignment_service, grade_service, undo_redo_service, inmemory=False)
            else:
                raise SettingsError("Invalid user interface!")

        else:
            raise SettingsError("Invalid repository!")

    @property
    def ui(self):
        return self._ui
