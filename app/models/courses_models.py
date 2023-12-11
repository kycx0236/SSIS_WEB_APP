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
            # You might want to log this error for debugging purposes
            print(f"Error adding courses info: {e}")
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
            # You might want to log this error for debugging purposes
            print(f"Error fetching all course info: {e}")
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
            print(f"Error updating courses: {e}")
            return False
        
    @classmethod
    def unique_code(cls, course_code):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT course_code FROM courses WHERE course_code = %s", (course_code,))
            code = cursor.fetchone()
            return code is not None  # Return True if the course code exists, otherwise False
        except Exception as e:
            print(f"Error checking unique course code: {e}")
            return False
        finally:
            cursor.close()

    
    @classmethod
    def get_course_code(cls, course_code):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM courses WHERE course_code = %s", (course_code,))
        course_data = cursor.fetchone()
        cursor.close()
        return course_data

    @classmethod
    def search_course(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = """
                    SELECT courses.course_code, courses.course_name, courses.college_code, college.college_name
                    FROM courses
                    LEFT JOIN college ON courses.college_code = college.college_code
                    WHERE courses.course_code LIKE %s 
                    OR courses.course_name LIKE %s 
                    OR courses.college_code LIKE %s 
                    OR college.college_name LIKE %s
                """
                cursor.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
        
    @classmethod
    def get_college_codes(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
            cursor.execute("SELECT college_code FROM college")
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_codes: {e}")
            return False
    
    @classmethod
    def filter_course(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                # Construct the SQL query based on the selected column
                columns = ["course_code", "course_name", "college_code", "college_name"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                sql = f"""
                    SELECT courses.course_code, courses.course_name, courses.college_code, college.college_name
                    FROM courses
                    LEFT JOIN college ON courses.college_code = college.college_code
                    WHERE {filter_by} = %s
                """
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def get_all_colleges(cls, course_code):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT college.college_name
                FROM college
                JOIN courses
                ON courses.college_code = college.college_code
                WHERE courses.college_code = %s
            """, (course_code,))
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False
        

    @classmethod
    def get_all_courses_with_colleges(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT courses.course_code, courses.course_name, courses.college_code, college.college_name
                FROM courses
                JOIN college ON courses.college_code = college.college_code
            """)
            all_courses = cursor.fetchall()
            cursor.close()
            return all_courses
        except Exception as e:
            print(f"Error obtaining courses with colleges: {e}")
            return []
