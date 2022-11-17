import tkinter as tk
import traceback
from tkinter import *
from tkinter import messagebox

from src.domain.assignment import Assignment
from src.domain.grade import Grade
from src.domain.student import Student
from src.validation.validators import ValidatorInput

MAIN_COLOR = "#ccccff"
BG_COLOR = "#99ccff"


def show_error(*args):
    err = traceback.format_exception(*args)
    messagebox.showerror(f'Exception {err}')


tk.Tk.report_callback_exception = show_error


class Gui:
    """
    Class that represents the graphical user interface of the application
    """
    def __init__(self, student_service, assignment_service, grade_service, undo_service, inmemory):
        self.__window = tk.Tk()
        self.__window.geometry("800x600")
        self.__window.title("Student Lab Assignment App")
        self.__background = PhotoImage(file="")

        self.__font_family = ("Times New Roman", 16, "bold")
        self.__button_paddingX = 200
        self.__button_paddingY = 5
        self.__button_border = 3
        self.__button_active_background = "#ccccff"
        self.__button_background = "#99ccff"
        self.__button_relief = RAISED

        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._validinput = ValidatorInput()
        self._undo_redo_service = undo_service
        self._inmemory = inmemory

        self.set_background()
        self.create_main_labels()
        self.create_main_buttons()

    def start(self):
        if self._inmemory is True:
            self._student_service.generate_students_list()
            self._assignment_service.generate_assignments_list()
            self._grade_service.generate_grades_list()
        self.__window.mainloop()

    def create_main_labels(self):
        Label(self.__window, text="Student Lab Assignment Application", bg=self.__button_background).pack()
        Label(self.__window, text="You may choose to:", bg=self.__button_background).pack()
        Label(self.__window, text="").pack()

    def create_main_buttons(self):
        Label(self.__window, text="").pack()
        Label(self.__window, text="").pack()
        Button(self.__window, text="Manage students and assignments", bd=self.__button_border, padx=self.__button_paddingX,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               activebackground=self.__button_active_background, command=lambda: self.manage_window()).pack()

        Label(self.__window, text="").pack()
        Label(self.__window, text="").pack()
        Button(self.__window, text="Give assignments to students", bd=self.__button_border, padx=self.__button_paddingX,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               activebackground=self.__button_active_background, command=lambda: self.assign_to_students_window()).pack()

        Label(self.__window, text="").pack()
        Label(self.__window, text="").pack()
        Button(self.__window, text="Grade students", bd=self.__button_border, padx=self.__button_paddingX,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               activebackground=self.__button_active_background, command=lambda: self.grade_students_window()).pack()

        Label(self.__window, text="").pack()
        Label(self.__window, text="").pack()
        Button(self.__window, text="Statistics", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.statistics_window()).pack()

        Label(self.__window, text="").pack()
        Label(self.__window, text="").pack()
        Button(self.__window, text="Undo & Redo", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.undo_redo_window()).pack()

    def set_background(self):
        bg_label = Label(self.__window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def manage_window(self):
        window = Toplevel(self.__window)
        window.geometry("800x700")
        window.title("Manage students and assignments")
        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Students: ", bg=self.__button_background, font=self.__font_family).pack()
        Label(window, text="").pack()

        Button(window, text="Add student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.add_student(window)).pack()
        Label(window, text="").pack()

        Button(window, text="Remove student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.remove_student()).pack()
        Label(window, text="").pack()

        Button(window, text="Update student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.update_student(window)).pack()
        Label(window, text="").pack()

        Button(window, text="List students", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.list_students(window)).pack()
        Label(window, text="").pack()

        Label(window, text="Assignments: ", bg=self.__button_background, font=self.__font_family).pack()
        Label(window, text="").pack()

        Button(window, text="Add assignment", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.add_assignment(window)).pack()
        Label(window, text="").pack()

        Button(window, text="Remove assignment", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.remove_assignment()).pack()
        Label(window, text="").pack()

        Button(window, text="Update assignment", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.update_assignment(window)).pack()
        Label(window, text="").pack()

        Button(window, text="List assignments", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.list_assignments(window)).pack()

    def add_student(self, main):
        student_id = IntVar()
        student_name = StringVar()
        student_group = IntVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Add student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=student_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        Label(window, text="Name:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        second_entry = Entry(window, textvariable=student_name, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        Label(window, text="Group:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=2)

        third_entry = Entry(window, textvariable=student_group, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)
        second_entry.grid(row=1, column=1)
        third_entry.grid(row=2, column=1)

        Button(window, text="Add student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.add_student_run(window, student_id, student_name, student_group)).grid(row=3)

    def add_student_run(self, main, stud_id, stud_name, stud_group):
        window = Toplevel(self.__window)
        main.destroy()
        window.title("Add student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        student_id = stud_id.get()
        name = stud_name.get()
        group = stud_group.get()

        self._student_service.add_student_run(student_id, name, group)
        self._undo_redo_service.add_command_to_stack("add_student", Student(student_id, name, group))

        Label(window, text="Student added successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def remove_student(self):
        window = Toplevel(self.__window)
        window.title("Remove student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        student_id = IntVar()
        Label(window, text="Id:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=student_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)

        Button(window, text="Remove student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.remove_student_run(window, student_id)).grid(row=1)

    def remove_student_run(self, main, stud_id):
        student_id = stud_id.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Remove student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        student = self._student_service.repo.search_by_id(student_id)
        self._student_service.remove_student_run(student_id)
        undo_list = []
        undo_list = list(
            self._grade_service.remove_student_and_assignments(student, student_id, undo_list))  # cascade remove
        undo_list.append(["remove_student", student])
        self._undo_redo_service.add_command_to_stack("cascade_remove", undo_list)

        Label(window, text="Student removed successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
              bg=self.__button_background).pack()

    def update_student(self, main):
        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        stud_id = IntVar()
        Label(window, text="Student id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=stud_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry .grid(row=0, column=1)

        Button(window, text="Proceed", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_student_run(window, stud_id)).grid(row=1)

    def update_student_run(self, main, stud_id):
        student_id = stud_id.get()
        student_name = StringVar()
        student_group = IntVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Name:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        second_entry = Entry(window, textvariable=student_name, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        Label(window, text="Group:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        third_entry = Entry(window, textvariable=student_group, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        second_entry.grid(row=0, column=1)
        third_entry.grid(row=1, column=1)

        Button(window, text="Update name", bd=self.__button_border, padx=self.__button_paddingX - 150,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_student_name(window, student_id, student_name)).grid(row=2, column=1)

        Button(window, text="Update group", bd=self.__button_border, padx=self.__button_paddingX - 150, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_student_group(main, student_id, student_group)).grid(row=2, column=2)

    def update_student_name(self, main, stud_id, stud_name):
        new_name = stud_name.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        old_student = self._student_service.repo.search_by_id(stud_id)
        param = list()
        param.append(Student(stud_id, old_student.name, old_student.group))
        param.append(Student(stud_id, new_name, old_student.group))
        self._undo_redo_service.add_command_to_stack("update_student_name", param)
        self._student_service.update_student_name_run(stud_id, new_name)

        Label(window, text="Student updated successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def update_student_group(self, main, stud_id, stud_group):
        new_group = stud_group.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        old_student = self._student_service.repo.search_by_id(stud_id)
        param = list()
        param.append(Student(stud_id, old_student.name, old_student.group))
        param.append(Student(stud_id, old_student.name, new_group))
        self._undo_redo_service.add_command_to_stack("update_student_group", param)
        self._student_service.update_student_group_run(stud_id, new_group)

        Label(window, text="Student updated successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def list_students(self, main):
        window = Toplevel(self.__window)
        main.destroy()
        window.geometry("1140x420")
        window.title("Students List")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        my_list = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        for item in self._student_service.students:
            my_list.insert(END, item.__str__())

        my_list.pack(side=TOP, fill=BOTH)
        scroll.config(command=my_list.yview)

    def add_assignment(self, main):
        assign_id = IntVar()
        assign_description = StringVar()
        assign_deadline = StringVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Add assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Id:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=assign_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        Label(window, text="Description:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        second_entry = Entry(window, textvariable=assign_description, bd=self.__button_border,
                             relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        Label(window, text="Deadline:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=2)

        third_entry = Entry(window, textvariable=assign_deadline, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)
        second_entry.grid(row=1, column=1)
        third_entry.grid(row=2, column=1)

        Button(window, text="Add assignment", bd=self.__button_border, padx=self.__button_paddingX,
               pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.add_assignment_run(window, assign_id, assign_description, assign_deadline)).grid(
            row=3)

    def add_assignment_run(self, main, assign_id, assign_desc, assign_deadline):
        window = Toplevel(self.__window)
        main.destroy()
        window.title("Add assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        assignment_id = assign_id.get()
        description = assign_desc.get()
        deadline = assign_deadline.get()

        self._assignment_service.add_assignment_run(assignment_id, description, deadline)
        self._undo_redo_service.add_command_to_stack("add_assignment", Assignment(assignment_id, description, deadline))

        Label(window, text="Assignment added successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
              bg=self.__button_background).pack()

    def remove_assignment(self):
        window = Toplevel(self.__window)
        window.title("Remove assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        assign_id = IntVar()
        Label(window, text="Id:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=assign_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)

        Button(window, text="Remove assignment", bd=self.__button_border, padx=self.__button_paddingX,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.remove_assignment_run(window, assign_id)).grid(row=1)

    def remove_assignment_run(self, main, assign_id):
        assignment_id = assign_id.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Remove assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        assignment = self._assignment_service.repo.search_by_id(assignment_id)
        self._assignment_service.remove_assignment_run(assignment_id)
        undo_list = []
        undo_list = list(
            self._grade_service.remove_assignment_and_students(assignment, assignment_id, undo_list))  # cascade remove
        undo_list.append(["remove_assignment", assignment])
        self._undo_redo_service.add_command_to_stack("cascade_remove", undo_list)

        Label(window, text="Assignment removed successfully!", bd=self.__button_border,
              padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
              bg=self.__button_background).pack()

    def update_assignment(self, main):
        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        assign_id = IntVar()
        Label(window, text="Assignment id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=assign_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)

        Button(window, text="Proceed", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_assignment_run(window, assign_id)).grid(row=1)

    def update_assignment_run(self, main, assign_id):
        assignment_id = assign_id.get()
        assignment_description = StringVar()
        assignment_deadline = StringVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Description:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        second_entry = Entry(window, textvariable=assignment_description, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        Label(window, text="Deadline:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        third_entry = Entry(window, textvariable=assignment_deadline, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        second_entry.grid(row=0, column=1)
        third_entry.grid(row=1, column=1)

        Button(window, text="Update description", bd=self.__button_border, padx=self.__button_paddingX - 150,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_assignment_description(window, assignment_id, assignment_description)).grid(row=2, column=1)

        Button(window, text="Update deadline", bd=self.__button_border, padx=self.__button_paddingX - 150,
               pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.update_assignment_deadline(main, assignment_id, assignment_deadline)).grid(row=2, column=2)

    def update_assignment_description(self, main, assign_id, assign_desc):
        new_description = assign_desc.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        old_assignment = self._assignment_service.repo.search_by_id(assign_id)
        param = list()
        param.append(Assignment(assign_id, old_assignment.description, old_assignment.deadline))
        param.append(Assignment(assign_id, new_description, old_assignment.deadline))
        self._undo_redo_service.add_command_to_stack("update_assignment_description", param)
        self._assignment_service.update_assignment_description_run(assign_id, new_description)

        Label(window, text="Assignment updated successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def update_assignment_deadline(self, main, assign_id, assign_deadline):
        new_deadline = assign_deadline.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Update assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        old_assignment = self._assignment_service.repo.search_by_id(assign_id)
        param = list()
        param.append(Assignment(assign_id, old_assignment.description, old_assignment.deadline))
        param.append(Assignment(assign_id, old_assignment.description, new_deadline))
        self._undo_redo_service.add_command_to_stack("update_assignment_deadline", param)
        self._assignment_service.update_assignment_deadline_run(assign_id, new_deadline)

        Label(window, text="Assignment updated successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def list_assignments(self, main):
        window = Toplevel(self.__window)
        main.destroy()
        window.geometry("1140x420")
        window.title("Assignments List")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        my_list = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        for item in self._assignment_service.assignments:
            my_list.insert(END, item.__str__())

        my_list.pack(side=TOP, fill=BOTH)
        scroll.config(command=my_list.yview)

    def assign_to_students_window(self):
        window = Toplevel(self.__window)
        window.geometry("400x400")
        window.title("Give assignments to students")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Assign to a student", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.assign_to_student(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Assign to a group of students", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.assign_to_group(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="List given assignments", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.list_given_assignments(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()

    def list_given_assignments(self, main):
        window = Toplevel(self.__window)
        main.destroy()
        window.geometry("1024x420")
        window.title("Given assignments list")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        my_list = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        for item in self._grade_service.grades:
            my_list.insert(END, item.__str__())

        my_list.pack(side=TOP, fill=BOTH)
        scroll.config(command=my_list.yview)

    def assign_to_student(self, main):
        student_id = IntVar()
        assignment_id = IntVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Assign to a student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Student Id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=student_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        Label(window, text="Assignment Id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        second_entry = Entry(window, textvariable=assignment_id, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)
        second_entry.grid(row=1, column=1)

        Button(window, text="Assign", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.assign_to_student_run(window, student_id, assignment_id)).grid(row=2)

    def assign_to_student_run(self, main, stud_id, assign_id):
        student_id = stud_id.get()
        assignment_id = assign_id.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Assign to a student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self._grade_service.assign_to_student(assignment_id, student_id)
        self._undo_redo_service.add_command_to_stack("give_student", Grade(assignment_id, student_id))

        Label(window, text="Assignment given successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def assign_to_group(self, main):
        group = IntVar()
        assignment_id = IntVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Assign to a group of students")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Group:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=group, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        Label(window, text="Assignment Id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=1)

        second_entry = Entry(window, textvariable=assignment_id, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)
        second_entry.grid(row=1, column=1)

        Button(window, text="Assign", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.assign_to_group_run(window, group, assignment_id)).grid(row=2)

    def assign_to_group_run(self, main, group, assign_id):
        student_group = group.get()
        assignment_id = assign_id.get()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Assign to a group of students")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        undo_list = self._grade_service.assign_to_group(assignment_id, student_group)
        self._undo_redo_service.add_command_to_stack("give_group", undo_list)

        Label(window, text="Assignment given successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def grade_students_window(self):
        window = Toplevel(self.__window)
        window.title("Grade students")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        stud_id = IntVar()
        Label(window, text="Student id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=stud_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)

        Button(window, text="Proceed", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.grade_student(window, stud_id)).grid(row=1)

    def grade_student(self, main, stud_id):
        assignment_id = IntVar()
        window = Toplevel(self.__window)
        main.destroy()
        window.title("Grade student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Student has the following ungraded assignments:", bd=self.__button_border,
              padx=self.__button_paddingX - 100, pady=self.__button_paddingY, relief=self.__button_relief,
              font=self.__font_family, bg=self.__button_background).grid(row=0)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        my_list = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        cnt = 0
        for item in self._grade_service.grades:
            if int(item.student_id) == int(stud_id) and float(item.grade_value) == -1:
                my_list.insert(END, item.__str__())
                cnt += 1

        my_list.pack(side=TOP, fill=BOTH)
        scroll.config(command=my_list.yview)

        if int(cnt) == 0:
            Label(window, text=f"Student with id {stud_id} does not have any ungraded assignments!",
                  bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY, relief=self.__button_relief,
                  font=self.__font_family, bg=self.__button_background).grid(row=3)

        Label(window, text="Assignment Id:", bd=self.__button_border, padx=self.__button_paddingX - 100, pady=self.__button_paddingY,
              relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).grid(row=4)

        second_entry = Entry(window, textvariable=assignment_id, bd=self.__button_border, relief=self.__button_relief,
                             font=self.__font_family, bg=self.__button_background)

        second_entry.grid(row=0, column=1)

        Button(window, text="Grade", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               command=lambda: self.grade_student_run(window, stud_id, assignment_id)).grid(row=5)

    def grade_student_run(self, main, stud_id, assign_id):
        student_id = stud_id.get()
        assignment_id = assign_id.get()
        grade = DoubleVar()

        window = Toplevel(self.__window)
        main.destroy()
        window.title("Grade student")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="Grade value:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
              bg=self.__button_background).grid(row=0)

        third_entry = Entry(window, textvariable=grade, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        third_entry.grid(row=0, column=1)

        grade_value = grade.get()
        self._grade_service.grade_student(student_id, assignment_id, grade_value)
        param = list()
        param.append(Grade(assignment_id, student_id))
        param.append(Grade(assignment_id, student_id, grade_value))
        self._undo_redo_service.add_command_to_stack("grade_student", param)

        Label(window, text="Student graded successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def statistics_window(self):
        window = Toplevel(self.__window)
        window.geometry("600x500")
        window.title("Statistics")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Students that received an assignment descending by grade", bd=self.__button_border,
               padx=self.__button_paddingX, pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
               bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.stat_assignment_window(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Students who are late with at least one assignment", bd=self.__button_border,
               padx=self.__button_paddingX, pady=self.__button_paddingY, relief=self.__button_relief,
               font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.stat_late_window(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Students with best school situation", bd=self.__button_border,
               padx=self.__button_paddingX, pady=self.__button_paddingY, relief=self.__button_relief,
               font=self.__font_family, bg=self.__button_background, activebackground=self.__button_active_background,
               command=lambda: self.stat_best_situation(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()

    def stat_assignment_window(self, main):
        window = Toplevel(self.__window)
        window.geometry("820x420")
        window.title("Statistics for assignment")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        assignment_id = IntVar()
        Label(window, text="Assignment Id:", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family,
              bg=self.__button_background).grid(row=0)

        first_entry = Entry(window, textvariable=assignment_id, bd=self.__button_border, relief=self.__button_relief,
                            font=self.__font_family, bg=self.__button_background)

        first_entry.grid(row=0, column=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        mylist = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        statistics = list(self._grade_service.create_list_of_given_assignment_ordered(assignment_id))

        for item in statistics:
            if float(item.grade_value) == -1:
                item.grade_value = "Not graded yet"
            student = self._student_service.repo.search_by_id(item.student_id)
            mylist.insert(END, f"Student id: {student.student_id}, Name: {student.name}, Grade value: {item.grade_value}")

        mylist.pack(side=TOP, fill=BOTH)
        scroll.config(command=mylist.yview)
        main.destroy()

    def stat_late_window(self, main):
        window = Toplevel(self.__window)
        window.geometry("820x420")
        window.title("Statistics late students")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        mylist = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        list_late = list(self._grade_service.create_list_of_late_students())

        for i in range(0, len(list_late)):
            stud_id = list_late[int(i)]['id']
            student = self._student_service.repo.search_by_id(stud_id)
            mylist.insert(END, f"Student id: {list_late[int(i)]['id']}, Name: {student.name}, Number of late assignments: {list_late[int(i)]['ungraded']}")

        mylist.pack(side=TOP, fill=BOTH)
        scroll.config(command=mylist.yview)

        main.destroy()

    def stat_best_situation(self, main):
        window = Toplevel(self.__window)
        window.geometry("820x420")
        window.title("Best school situation")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        scroll = Scrollbar(window, orient='vertical')
        scroll.pack(side=RIGHT, fill=Y)

        mylist = Listbox(window, yscrollcommand=scroll.set, height=420, font=self.__font_family, bg=self.__button_background)

        list_best_situation = list(self._grade_service.create_list_of_best_school_situation())

        for i in range(0, len(list_best_situation)):
            stud_id = list_best_situation[int(i)]['id']
            student = self._student_service.repo.search_by_id(stud_id)
            mylist.insert(END, f"  Student id: {list_best_situation[int(i)]['id']}, Name: {student.name}, Average grade: "
                               f"{list_best_situation[int(i)]['grade']}")

        mylist.pack(side=TOP, fill=BOTH)
        scroll.config(command=mylist.yview)

        main.destroy()

    def undo_redo_window(self):
        window = Toplevel(self.__window)
        window.geometry("400x400")
        window.title("Undo & Redo")

        bg_label = Label(window, image=self.__background)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Undo", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               activebackground=self.__button_active_background, command=lambda: self.undo(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()
        Button(window, text="Redo", bd=self.__button_border, padx=self.__button_paddingX, pady=self.__button_paddingY,
               relief=self.__button_relief, font=self.__font_family, bg=self.__button_background,
               activebackground=self.__button_active_background, command=lambda: self.redo(window)).pack()

        Label(window, text="").pack()
        Label(window, text="").pack()
        Label(window, text="").pack()

    def undo(self, main):
        self._undo_redo_service.call_undo()

        window = Toplevel(self.__window)
        main.destroy()

        Label(window, text="Last operation undone successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()

    def redo(self, main):
        self._undo_redo_service.call_redo()

        window = Toplevel(self.__window)
        main.destroy()

        Label(window, text="Last operation undone successfully!", bd=self.__button_border, padx=self.__button_paddingX - 100,
              pady=self.__button_paddingY, relief=self.__button_relief, font=self.__font_family, bg=self.__button_background).pack()
