from configparser import ConfigParser
from exceptions.exceptions import SettingsError
from repository.database.database_assignmentRepo import AssignmentDatabaseRepository
from repository.database.database_gradeRepo import GradeDatabaseRepository
from repository.database.database_studentRepo import StudentDatabaseRepository
from repository.inmemory.assignmentRepo import AssignmentRepository
from repository.inmemory.gradeRepo import GradeRepository
from repository.inmemory.studentRepo import StudentRepository
from repository.json.jsonfile_assignmentRepo import AssignmentJsonFileRepository
from repository.json.jsonfile_gradeRepo import GradeJsonFileRepository
from repository.json.jsonfile_studentRepo import StudentJsonFileRepository
from services.assignmentService import AssignmentService
from services.gradeService import GradeService
from services.studentService import StudentService
from services.undoRedoService import UndoRedoService
from ui.ui import Ui
from ui.gui import Gui
from validation.validators import ValidatorStudent, ValidatorAssignment, ValidatorGrade
from repository.csv.textfile_studentRepo import StudentTextFileRepository
from repository.csv.textfile_assignmentRepo import AssignmentTextFileRepository
from repository.csv.textfile_gradeRepo import GradeTextFileRepository
from repository.binary.binaryfile_studentRepo import StudentBinFileRepository
from repository.binary.binaryfile_assignmentRepo import AssignmentBinFileRepository
from repository.binary.binaryfile_gradeRepo import GradeBinFileRepository
import os


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
