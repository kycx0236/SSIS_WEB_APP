from app import mysql

class Courses:
    def __init__(self, course_code=None, course_name=None, college_code=None):
        self.course_code = course_code
        self.course_name = course_name
        self.college_code = college_code

    def add(self):
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO courses (course_code, course_name, college_code) VALUES (%s, %s, %s)"
            cursor.execute(sql, (self.course_code, self.course_name, self.college_code))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding course: {e}")
            return False

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM courses"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error fetching all courses: {e}")
            return []

    @classmethod
    def delete(cls, course_code):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM courses WHERE course_code = %s"
            cursor.execute(sql, (course_code,))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting course: {e}")
            return False

    @classmethod
    def update(cls, course_code, new_course_name, new_college_code):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE courses SET course_name = %s, college_code = %s WHERE course_code = %s"
            cursor.execute(sql, (new_course_name, new_college_code, course_code))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating course: {e}")
            return False

    @classmethod
    def search(cls, query):
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM courses WHERE course_code LIKE %s OR course_name LIKE %s OR college_code LIKE %s"
            cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error searching for courses: {e}")
            return []

    @classmethod
    def unique_code(cls, course_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", (course_code,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code