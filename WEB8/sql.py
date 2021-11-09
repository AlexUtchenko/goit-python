import psycopg2
from psycopg2 import Error, DatabaseError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def creating_db():
    try:
        connection = psycopg2.connect(
            user= 'postgres',
            password= 'sS456PG',
            host= '127.0.0.1',
            port = '5432',
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
            user= 'postgres',
            password= 'sS456PG',
            host= '127.0.0.1',
            port = '5432',
            database = 'test_db'
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_table_students = """
                CREATE TABLE students (
                    student_id INT PRIMARY KEY NOT NULL,
                    student_name VARCHAR(100),
                    group INT,
                    FOREIGN KEY (group) REFERENCES groups (group_id)
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
                            grade TINYINT UNSIGNED,
                            student_id INT,
                            subject_id INT,
                            grade_gate DATE,
                            FOREIGN KEY (student_id) REFERENCES students (student_id)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE,
                            FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE
                );
                """
        # cursor.execute(create_table_groups)
        # cursor.execute(create_table_subjects)
        # cursor.execute(create_table_students)
        cursor.execute(create_table_grades)
        print('The tables have been created')

    except (Exception, Error, DatabaseError) as error:
        print('Error: ', error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print('connection is closed')

if __name__ == '__main__':
    # creating_db()
    creating_tables()