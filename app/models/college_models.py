import logging
from app import mysql

# Configure the logger
logging.basicConfig(filename='app_errors.log', level=logging.ERROR)

class College:
    def __init__(self, id_number=None, first_name=None, last_name=None, course_code=None, year_=None, gender=None):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.course_code = course_code
        self.year_ = year_
        self.gender = gender

    def add(self):
        """
        Add a new student to the database.

        Returns:
            bool: True if the addition was successful, False otherwise.
        """
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO students (id_number, first_name, last_name, course_code, year_, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.id_number, self.first_name, self.last_name, self.course_code, self.year_, self.gender))
            mysql.connection.commit()
            return True
        except Exception as e:
            # Log the error for debugging purposes
            logging.error(f"Error adding student: {e}")
            return False

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM college"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error fetching all colleges: {e}")
            return []

    @classmethod
    def search(cls, query):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM college WHERE college_code LIKE %s OR college_name LIKE %s"
            cursor.execute(sql, (f"%{query}%", f"%{query}%"))
            result = cursor.fetchall()
            return result
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error searching for colleges: {e}")
            return []

    @classmethod
    def delete(cls, college_code):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM college WHERE college_code = %s"
            cursor.execute(sql, (college_code,))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error deleting college: {e}")
            return False

    @classmethod
    def update(cls, college_code, new_college_name):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE college SET college_name = %s WHERE college_code = %s"
            cursor.execute(sql, (new_college_name, college_code))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error updating college: {e}")
            return False

    @classmethod
    def unique_code(cls, college_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT college_code FROM college WHERE college_code = %s", (college_code,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code
    
    @classmethod
    def unique_code(cls, college_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT college_code FROM college WHERE college_code = %s", (college_code,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code
    
    @classmethod
    def get_college_id(cls, college_code):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM college WHERE college_code = %s", (college_code,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data