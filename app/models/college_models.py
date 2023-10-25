from app import mysql

class College:
    def __init__(self, college_code=None, college_name=None):
        self.college_code = college_code
        self.college_name = college_name 

    def add(self):
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO college (college_code, college_name) VALUES (%s, %s)"
            cursor.execute(sql, (self.college_code, self.college_name))
            mysql.connection.commit()
            return True
        except Exception as e:
            # You might want to log this error for debugging purposes
            print(f"Error adding college info: {e}")
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
            print(f"Error fetching all college info: {e}")
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
            print(f"Error deleting course: {e}")
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
            print(f"Error updating college: {e}")
            return False
        
    @classmethod
    def unique_code(cls, college_code):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT college_code FROM college WHERE college_code = %s", (college_code,))
        code = cursor.fetchone()
        cursor.close()
        return code
    
    @classmethod
    def get_college_code(cls, college_code):
        cursor = mysql.connection.cursor(dictionary=True)  # Set dictionary=True to return results as dictionaries
        cursor.execute("SELECT * FROM college WHERE college_code = %s", (college_code,))
        college_data = cursor.fetchone()
        cursor.close()
        return college_data

    @classmethod
    def search(cls, query):
        try:
            with mysql.connection.cursor() as cursor:
                sql = "SELECT * FROM college WHERE college_code = %s OR college_name = %s"
                cursor.execute(sql, (query, query))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    @classmethod
    def filter_college(cls, filter_by, query):
        try:
            with mysql.connection.cursor() as cursor:
                # Construct the SQL query based on the selected column
                columns = ["college_code", "college_name"]
                if filter_by not in columns:
                    raise ValueError("Invalid filter column")
                sql = f"SELECT * FROM college WHERE {filter_by} = %s"
                cursor.execute(sql, (query,))
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Error: {e}")
            return []


    