import psycopg2
from psycopg2 import Error, DatabaseError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import random
from faker import Faker
from datetime import date

def creating_db():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_db = 'CREATE DATABASE test_db'
        cursor.execute(create_db)
        print('DB has been created')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')


def creating_tables():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_table_students = """
                CREATE TABLE students (
                    student_id INT PRIMARY KEY NOT NULL,
                    student_name VARCHAR(100),
                    group_id INT,
                    FOREIGN KEY (group_id) REFERENCES groups (group_id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
        );
        """
        create_table_groups = """
                        CREATE TABLE groups (
                            group_id INT PRIMARY KEY NOT NULL
                );"""
        create_table_subjects = """
                        CREATE TABLE subjects (
                            subject_id INT PRIMARY KEY NOT NULL,
                            subject_name VARCHAR(100),
                            lecturer VARCHAR(100)
                );
                """
        create_table_grades = """
                        CREATE TABLE grades (
                            grade_id INT PRIMARY KEY,
                            grade INT,
                            student_id INT,
                            subject_id INT,
                            grade_date DATE,
                            FOREIGN KEY (student_id) REFERENCES students (student_id)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE,
                            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE
                );
                """
        cursor.execute(create_table_groups)
        cursor.execute(create_table_subjects)
        cursor.execute(create_table_students)
        cursor.execute(create_table_grades)
        print('The tables have been created')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')


def inserting_tables():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        insert_to_groups = """
        INSERT INTO groups (group_id)
                    VALUES 
                        (1),
						(2),
						(3)
        ;"""

        insert_to_students = """
                INSERT INTO students (student_id, student_name, group_id)
                    VALUES 
                        (1, 'Smith', 1),
                        (2, 'Li', 1),
                        (3, 'Petrov', 1),
                        (4, 'Holovko', 1),
                        (5, 'Shevchenko', 1),
                        (6, 'Rebrov', 1),
                        (7, 'Lobanovskiy', 1),
                        (8, 'Davitadze', 1),
                        (9, 'Kaladze', 1),
                        (10, 'Goncharov', 1),
                        (11, 'Doan', 2),
                        (12, 'Koval', 2),
                        (13, 'Petrenko', 2),
                        (14, 'Ischenko', 2),
                        (15, 'Cheh', 2),
                        (16, 'Virt', 2),
                        (17, 'Boiko', 2),
                        (18, 'Petrin', 2),
                        (19, 'Right', 2),
                        (20, 'Jim', 2),
                        (21, 'Makarenko', 3),
                        (22, 'Revenko', 3),
                        (23, 'Dmitrenko', 3),
                        (24, 'Zubov', 3),
                        (25, 'Khan', 3),
                        (26, 'Prasolov', 3),
                        (27, 'Climchuk', 3),
                        (28, 'Pedko', 3),
                        (29, 'Krutko', 3),
                        (30, 'Endko', 3)
        ;
        """

        insert_to_subjects = """
            INSERT INTO subjects (subject_id, subject_name, lecturer)
                        VALUES 
                            (1, 'Chemistry', 'Utchenko'),
                            (2, 'Python', 'GOIT'),
                            (3, 'Physics', 'Tesla'),
                            (4, 'Alchemy', 'Platon'),
                            (5, 'Football', 'Loban');
				"""
        cursor.execute(insert_to_groups)
        cursor.execute(insert_to_students)
        cursor.execute(insert_to_subjects)
        count = 0
        for student in range(1, 31):
            for subject in range(1, 6):
                for mark in range(20):
                    count += 1
                    faker = Faker()
                    f_date = faker.date_between_dates(date_start=date(2021, 8, 1), date_end=date(2021, 11, 10))
                    data = (count, random.randint(1, 5), student, subject, f_date)
                    mark_query = """INSERT INTO grades (grade_id, grade, student_id, subject_id, grade_date)
                    VALUES 
                        (%s, %s, %s, %s, %s);
                    """
                    cursor.execute(mark_query, data)
        print('The tables have been inserted')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q1_5_best_avg():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT AVG(grades.grade) AS AvGrade, students.student_name
                FROM grades
                INNER JOIN students ON grades.student_id = students.student_id
                GROUP BY students.student_name
                ORDER BY AvGrade DESC
                LIMIT 5
        """
        cursor.execute(query)
        result = cursor.fetchall()
        for rec in result:
            print(float(rec[0]), ': ', rec[1])


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q2_1_top_in_subj():
    n = input("Enter subject_id (1, 2, 3, 4 or 5)\n >>> ")
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT AVG(grades.grade) AS AvGrade, students.student_name, subjects.subject_name
                FROM grades
                INNER JOIN students ON grades.student_id = students.student_id
                INNER JOIN subjects ON grades.subject_id = subjects.subject_id
                WHERE grades.subject_id = %s
                GROUP BY students.student_name, subjects.subject_name
                ORDER BY AvGrade DESC
                LIMIT 1
        """
        cursor.execute(query,n)
        result = cursor.fetchone()
        print(f'{result[1]} got average score {float(result[0])} in {result[2]}')


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q3_avg_gr_subj():
    s = input("Enter subject_id (1, 2, 3, 4 or 5)\n >>> ")
    g = input("Enter group_id (1, 2 or 3)\n >>> ")
    variables = (g,s)
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT AVG(grades.grade) AS AvGrade, subjects.subject_name, students.group_id
	            FROM grades
	            INNER JOIN students ON grades.student_id = students.student_id
	            INNER JOIN subjects ON grades.subject_id = subjects.subject_id
	            WHERE students.group_id = %s and grades.subject_id = %s
	            GROUP BY subjects.subject_name, students.group_id
        """
        cursor.execute(query,variables)
        result = cursor.fetchone()
        print(f'Group number {result[2]} got average score {float(result[0])} in {result[1]}')


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q4_avg_all():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT AVG(grades.grade) AS AvGrade
	            FROM grades
        """
        cursor.execute(query)
        result = cursor.fetchone()
        print(f'The average score in all groups = {round(float(result[0]),2)}')


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q5_sub_by_lect():
    n = (input("Enter lecturer name (Tesla, GOIT, Utchenko, Platon, Loban)\n >>> "))
    n = (n,)
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT subject_name
                FROM subjects
                WHERE lecturer = %s
        """
        cursor.execute(query, n)
        result = cursor.fetchall()
        for subj in result:
            print(f'{n[0]} teaches {subj[0]}')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q6_stud_list_by_gr():
    n = (input("Enter group number (1, 2, or 3)\n >>> "))
    n = (n,)
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT student_name
                FROM students
                WHERE group_id = %s
        """
        cursor.execute(query, n)
        result = cursor.fetchall()
        print(f'Group number {n[0]}:')
        for stud in result:
            print(f'  {stud[0]}')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q7_grades_by_group_subj():
    g = int(input("Enter group number (1, 2, or 3)\n >>> "))
    s = (input('Enter subject ("Chemistry", "Python", "Physics", "Alchemy", "Football")\n >>> '))
    variables = (s,g)
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT students.student_name, grades.grade, subjects.subject_name, group_id
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE subjects.subject_name = %s and group_id = %s ;
        """
        cursor.execute(query, variables)
        result = cursor.fetchall()
        current_rec = [result[0][0], result[0][1], result[0][2], result[0][3]]
        grades_list = []
        for rec in result:
            if rec[0] == current_rec[0]:
                grades_list.append(rec[1])
            else:
                current_rec[1] = grades_list
                print(f'Student name: {current_rec[0]},\n  - subject: {current_rec[2]},\n  - group: {current_rec[3]},\n  - grades: {current_rec[1]} \n')
                grades_list = []
                current_rec = [rec[0], rec[1], rec[2], rec[3]]
        current_rec[1] = grades_list
        print(f'Student name: {current_rec[0]},\n  - subject: {current_rec[2]},\n  - group: {current_rec[3]},\n  - grades: {current_rec[1]} \n')


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q8_grades_by_group_subj_last_class():
    g = int(input("Enter group number (1, 2, or 3)\n >>> "))
    s = (input('Enter subject ("Chemistry", "Python", "Physics", "Alchemy", "Football")\n >>> '))
    variables = (s,g)
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT students.student_name, grades.grade, subjects.subject_name, group_id, grades.grade_date
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE subjects.subject_name = %s and group_id = %s
        """
        cursor.execute(query, variables)
        result = cursor.fetchall()
        current_rec = [result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]]
        grades_list = []
        for rec in result:
            if rec[4] != current_rec[4]:
                break
            if rec[0] == current_rec[0]:
                grades_list.append(rec[1])
            else:
                current_rec[1] = grades_list
                print(f'Student name: {current_rec[0]},\n  - subject: {current_rec[2]},\n  - group: {current_rec[3]},\n  - grades: {current_rec[1]},\n  - date: {current_rec[4]} \n')
                grades_list = []
                current_rec = [rec[0], rec[1], rec[2], rec[3]]
        current_rec[1] = grades_list
        print(f'Student name: {current_rec[0]},\n  - subject: {current_rec[2]},\n  - group: {current_rec[3]},\n  - grades: {current_rec[1]},\n  - date: {current_rec[4]} \n')


    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q9_subjs_student_attend():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT student_name
                FROM students
                WHERE student_id = %s
        """
        cursor.execute(query, (random.randint(1, 31),))
        rand_stud = cursor.fetchone()[0]
        stud_name = input(f"Enter student's name to get courses he attends (e.g. {rand_stud})\n>>> ")
        query = """
                SELECT subjects.subject_name
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE students.student_name = %s;
                """
        cursor.execute(query, (stud_name,))
        result = cursor.fetchall()
        final = set()
        for subj in result:
            final.add(subj)
        print(f'Student {stud_name} attends next classes: ')
        for subj in final:
            print(f' - {subj[0]}')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q10_subjs_student_and_lecturer():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT student_name
                FROM students
                WHERE student_id = %s
        """
        cursor.execute(query, (random.randint(1, 31),))
        rand_stud = cursor.fetchone()[0]
        stud_name = input(f"Enter student's name(e.g. {rand_stud})\n>>> ")
        lecturer_name = input(f"Enter lecturer's name (Tesla, GOIT, Utchenko, Platon, Loban)\n>>> ")
        query = """
                SELECT subjects.subject_name
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE students.student_name = %s and subjects.lecturer = %s
                """
        cursor.execute(query, (stud_name, lecturer_name))
        result = cursor.fetchall()
        final = set()
        for subj in result:
            final.add(subj)
        print(f'Lecturer {lecturer_name} reads next classes for student {stud_name}: ')
        for subj in final:
            print(f' - {subj[0]}')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q11_avg_grade_from_lect_to_stud():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = """
                SELECT student_name
                FROM students
                WHERE student_id = %s
        """
        cursor.execute(query, (random.randint(1, 31),))
        rand_stud = cursor.fetchone()[0]
        stud_name = input(f"Enter student's name(e.g. {rand_stud})\n>>> ")
        lecturer_name = input(f"Enter lecturer's name (Tesla, GOIT, Utchenko, Platon, Loban)\n>>> ")
        query = """
                SELECT AVG(grades.grade)
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE students.student_name = %s and subjects.lecturer = %s
                """
        cursor.execute(query, (stud_name, lecturer_name))
        result = float(cursor.fetchone()[0])
        print(f"Lecturer's {lecturer_name} average grade for the student {stud_name} is {result}")

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

def q12_avg_grade_from_lect():
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='sS456PG',
            host='127.0.0.1',
            port='5432',
            database='test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        lecturer_name = input(f"Enter lecturer's name (Tesla, GOIT, Utchenko, Platon, Loban)\n>>> ")
        query = """
                SELECT AVG(grades.grade)
                FROM grades
                INNER JOIN
                 students
                 ON grades.student_id = students.student_id
                INNER JOIN
                 subjects
                 ON grades.subject_id = subjects.subject_id
                WHERE subjects.lecturer = %s
                """
        cursor.execute(query, (lecturer_name,))
        result = round(float(cursor.fetchone()[0]),2)
        print(f"Lecturer's {lecturer_name} average grade is {result}")

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

if __name__ == '__main__':
    # creating_db()
    # creating_tables()
    # inserting_tables()
    q1_5_best_avg() # 1
    # q2_1_top_in_subj() # 2
    # q3_avg_gr_subj() # 3
    # q4_avg_all() # 4
    # q5_sub_by_lect() # 5
    # q6_stud_list_by_gr() # 6
    # q7_grades_by_group_subj() # 7
    # q8_grades_by_group_subj_last_class() # 8
    # q9_subjs_student_attend() # 9
    # q10_subjs_student_and_lecturer() # 10
    # q11_avg_grade_from_lect_to_stud() # 11
    # q12_avg_grade_from_lect()


