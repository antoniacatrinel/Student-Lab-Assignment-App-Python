import mysql.connector

my_database = mysql.connector.connect(host='localhost', user='root', password='1234', port='3306', database='student_lab_assignment_database')

my_cursor = my_database.cursor()
my_cursor.execute('SELECT * FROM students')

students = my_cursor.fetchall()
for student in students:
    print(student)

my_cursor.execute('SELECT * FROM assignments')

assignments = my_cursor.fetchall()
for assignment in assignments:
    print(assignment)

my_cursor.execute('SELECT * FROM grades')

grades = my_cursor.fetchall()
for grade in grades:
    print(grade)
