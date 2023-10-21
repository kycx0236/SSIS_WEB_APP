from flask import render_template, redirect, request, flash, url_for, jsonify
from . import student_bp
import app.models.students_models as student_models
from app.students.forms import StudentForm

headings = ("ID_Number", "First Name", "Last Name", "Course Code", "Year", "Gender", "Actions")

@student_bp.route('/')
def home_page():
    return render_template('home.html')

@student_bp.route("/students")
def students():
    student_data = student_models.Students.all()
    return render_template('students.html', headings=headings, data=student_data)

@student_bp.route('/students/edit', methods=["GET", "POST"])
def edit_student():
    id_number = request.args.get('id_number')
    form = StudentForm()
    student_data = student_models.Students.get_student_by_id(id_number)

    if student_data:
        # Ensure that student_data is not empty before accessing elements
        student_data_dict = {
            "id_number": student_data['id_number'],
            "first_name": student_data['first_name'],
            "last_name": student_data['last_name'],
            "course_code": student_data['course_code'],
            "year_": student_data['year_'],
            "gender": student_data['gender']
        }
    else:
        # Handle the case where no student data was found
        flash("Student not found.", "error")
        return redirect(url_for("students.students"))

    if request.method == "POST" and form.validate():
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data
        new_course_code = form.course_code.data
        new_year = form.year_.data
        new_gender = form.gender.data

        if student_models.Students.update(id_number, new_first_name, new_last_name, new_course_code, new_year, new_gender):
            flash("Student information updated successfully!", "success")
            return redirect(url_for("students.students"))
        else:
            flash("Failed to update student information.", "error")

    return render_template("edit_student.html", form=form, row=student_data_dict)




@student_bp.route("/students/delete", methods=["POST"])
def delete_students():
    try:
        id_number = request.form.get('id_number')
        if student_models.Students.delete(id_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed")
    except Exception as e:
        # Log the error for debugging purposes
        student_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@student_bp.route('/students/add', methods=['POST', 'GET'])
def add():
    form = StudentForm(request.form)
    
    if request.method == 'POST' and form.validate():
        check_id = form.id_number.data
        student_exists = student_models.Students.unique_code(check_id)

        if student_exists:
            flash("Student already exists! Please enter a unique id_number", 'error')
        else:
            student = student_models.Students(
                id_number=check_id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                course_code=form.course_code.data,
                year_=form.year_.data,
                gender=form.gender.data
            )
            student.add()
            flash("Student added successfully!", 'success')
            return redirect(url_for('students.students'))
    
    return render_template('add_student.html', form=form)

@student_bp.route('/students/search', methods=['POST'])
def search_student():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        # Perform a database query based on the search_query
        search_results = student_models.Students.search_student(search_query)
        return jsonify(search_results)
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500
