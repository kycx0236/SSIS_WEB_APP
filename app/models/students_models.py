from app import mysql
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload, destroy

import re


class Students:
    def __init__(self, id_number=None, first_name=None, last_name=None, course_code=None, year_=None, gender=None, profile_pic=None):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.course_code = course_code
        self.year_ = year_
        self.gender = gender
        self.profile_pic = profile_pic

    @classmethod
    def add(cls, id_number, first_name, last_name, course_code, year_, gender, profile_pic):
        try:
            with mysql.connection.cursor() as cursor:
                if profile_pic:
                    upload_result = cloudinary.uploader.upload(profile_pic, folder="SSIS", resource_type='image')
                    profile_pic_url = upload_result['secure_url']

                    sql = "INSERT INTO students (id_number, first_name, last_name, course_code, year_, gender, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id_number, first_name, last_name, course_code, year_, gender, profile_pic_url))
                else:
                    sql = "INSERT INTO students (id_number, first_name, last_name, course_code, year_, gender) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id_number, first_name, last_name, course_code, year_, gender))

            mysql.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error adding student: {e}")
            return False


    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            sql = "SELECT students.*, courses.course_code, college.college_code FROM students INNER JOIN courses ON students.course_code = courses.course_code INNER JOIN college ON courses.college_code = college.college_code;"
            cursor.execute(sql)
            result = cursor.fetchall()

            for student in result:
                student['profile_pic'] = student['profile_pic']
                
            return result
        except Exception as e:
            print(f"Error fetching all students: {e}")
            return []
        
    @classmethod
    def view_student_info(cls, id_number):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT students.id_number, students.first_name, students.last_name, students.course_code, students.year_, students.gender, students.profile_pic, courses.course_name, college.college_code, college.college_name
                    FROM students
                    INNER JOIN courses ON students.course_code = courses.course_code
                    INNER JOIN college ON courses.college_code = college.college_code
                    WHERE students.id_number = %s
                """
                cursor.execute(sql, (id_number,))
                student_data = cursor.fetchone()
                print('Student data: ', student_data)

                return student_data
                
        except Exception as e:
            print(f"Error fetching students data: {e}")
     
            
    @classmethod
    def delete(cls, id_number):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM students WHERE id_number = %s"
            cursor.execute(sql, (id_number,))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error deleting student: {e}")
            return False

    @classmethod
    def update(cls, id_number, new_first_name, new_last_name, new_course_code, new_year_, new_gender, new_profile_pic):
        try:
            cursor = mysql.connection.cursor()

            if new_profile_pic is not None:
                # Upload the new profile picture to Cloudinary
                result = upload(new_profile_pic, folder="SSIS", resource_type='image')
                new_profile_pic_url = result['secure_url']
                print('Uploading profile picture link: ', new_profile_pic_url)

                # Delete the old profile picture from Cloudinary
                old_profile_pic_url = cls.get_student_by_id(id_number).get('profile_pic')
                if old_profile_pic_url:
                    public_id = old_profile_pic_url.split('/')[-1].split('.')[0]
                    destroy(public_id)

                # Update the student record with the new profile picture URL
                sql = "UPDATE students SET first_name = %s, last_name = %s, course_code = %s, year_ = %s, gender = %s, profile_pic = %s WHERE id_number = %s"
                cursor.execute(sql, (new_first_name, new_last_name, new_course_code, new_year_, new_gender, new_profile_pic_url, id_number))
            else:
                # Update the student record without changing the profile picture
                sql = "UPDATE students SET first_name = %s, last_name = %s, course_code = %s, year_ = %s, gender = %s WHERE id_number = %s"
                cursor.execute(sql, (new_first_name, new_last_name, new_course_code, new_year_, new_gender, id_number))

            mysql.connection.commit()
            return True
        except Exception as e:
            # Print the error message to the console
            print(f"Error updating student: {e}")
            return False


        
    @classmethod
    def unique_code(cls, id_number):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_number FROM students WHERE id_number = %s", (id_number,))
        code = cursor.fetchone()  # Use fetchone() to get a single result
        cursor.close()
        return code
    
    @classmethod
    def get_student_by_id(cls, id_number):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM students WHERE id_number = %s", (id_number,))
        student_data = cursor.fetchone()
        cursor.close()
        return student_data

    @classmethod
    def search_student(cls, query):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                sql = """
                    SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender, students.profile_pic
                    FROM students
                    JOIN courses ON students.course_code = courses.course_code
                    WHERE students.id_number = %s
                    OR students.first_name = %s
                    OR students.last_name = %s
                    OR students.course_code = %s
                    OR courses.college_code = %s
                    OR students.year_ = %s
                    OR students.gender = %s
                """
                cursor.execute(sql, (query, query, query, query, query, query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

    @classmethod
    def filter_student(cls, filter_by, query):
        try:
            with mysql.connection.cursor(dictionary=True) as cursor:
                # Construct the SQL query based on the selected column
                columns = ["id_number", "first_name", "last_name", "course_code", "college_code", "year_", "gender"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                if filter_by == "college_code":
                    sql = f"""
                        SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender, students.profile_pic
                        FROM students
                        JOIN courses ON students.course_code = courses.course_code
                        WHERE courses.college_code = %s
                    """
                else:
                    sql = f"""
                        SELECT students.id_number, students.first_name, students.last_name, students.course_code, courses.college_code, students.year_, students.gender, students.profile_pic
                        FROM students
                        JOIN courses ON students.course_code = courses.course_code
                        WHERE students.{filter_by} = %s
                    """
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []

        
    @classmethod
    def get_all_courses(cls):
        try:
            cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
            cursor.execute("SELECT course_code FROM courses")
            all_courses = cursor.fetchall()
            cursor.close()
            return all_courses
        except Exception as e:
            print(f"Error obtaining course_code: {e}")
            return False
        
    @classmethod
    def get_all_colleges(cls, id_number):
        try:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT courses.college_code 
                FROM courses
                JOIN students
                ON students.course_code = courses.course_code
                WHERE id_number = %s
            """, (id_number,))
            all_colleges = cursor.fetchall()
            cursor.close()
            return all_colleges
        except Exception as e:
            print(f"Error obtaining college_code: {e}")
            return False
