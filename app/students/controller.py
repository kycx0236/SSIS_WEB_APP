from flask import render_template, redirect, request, flash, url_for, jsonify, current_app
from . import student_bp
import app.models.students_models as student_models
from app.students.forms import StudentForm
from wtforms import ValidationError
from cloudinary import uploader
from cloudinary.uploader import upload
from cloudinary.uploader import destroy
import cloudinary.api
from cloudinary.utils import cloudinary_url
import cloudinary
import os

headings = ("Profile Picture", "ID_Number", "First Name", "Last Name", "Course Code", "College Code", "Year", "Gender", "Actions")

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
    print("Received id_number:", id_number)
    form = StudentForm()
    student_data = student_models.Students.get_student_by_id(id_number)
    all_courses = student_models.Students.get_all_courses()
    
    student_data_dict = {}  # Initialize with an empty dictionary

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


    if request.method == "POST" and form.validate():
        new_first_name = form.first_name.data
        new_last_name = form.last_name.data
        new_course_code = form.course_code.data
        new_year = form.year_.data
        new_gender = form.gender.data

        # Use the uploaded file if it exists, else use the existing URL
        new_profile_pic = request.files['profile_pic'] if 'profile_pic' in request.files and request.files['profile_pic'].filename != '' else student_data['profile_pic']
        print("Profile picture: ", new_profile_pic)

        if student_models.Students.update(id_number, new_first_name, new_last_name, new_course_code, new_year, new_gender, new_profile_pic):
            flash("Student information updated successfully!", "success")
            return redirect(url_for("students.students"))
        else:
            flash("Failed to update student information.", "error")

    return render_template("edit_student.html", form=form, row=student_data_dict, courses=all_courses, current_profile_pic=student_data['profile_pic'])




@student_bp.route("/students/delete", methods=["POST"])
def delete_students():
    try:
        id_number = request.form.get('id_number')

        # Use the get_student_by_id class method to retrieve the student data
        student = student_models.Students.get_student_by_id(id_number)

        if not student:
            return jsonify(success=False, message="Student not found"), 404

        # Delete the image from Cloudinary using public ID
        if student['profile_pic']:
            try:
                current_path = student['profile_pic']
                print("Current path: ",  current_path)

                # Split the URL by "/"
                path_parts = current_path.split("/")

                # Find the index of "SSIS" in the path_parts
                index_of_ssis = path_parts.index("SSIS")

                # Extract the desired part
                desired_part = "/".join(path_parts[index_of_ssis:index_of_ssis + 2])

                # Remove the file extension
                public_id, _ = os.path.splitext(desired_part)
                print("Public ID: " + public_id)
                # Create a list with a single element
                public_ids_to_delete = [public_id]

                # Use Cloudinary's delete_resources method to delete the image
                image_delete_result = cloudinary.api.delete_resources(public_ids_to_delete, resource_type="image", type="upload")
                print("Cloudinary API Response:", image_delete_result)

                if 'deleted' in image_delete_result and image_delete_result['deleted'][public_id] == 'deleted':
                    # Image deleted successfully
                    print("Successfully deleted from Cloudinary")
                else:
                    # Log the error for debugging purposes
                    current_app.logger.error("Failed to delete image from Cloudinary. Response: %s" % image_delete_result)
            except Exception as e:
                # Log the error for debugging purposes
                current_app.logger.error("Error deleting image from Cloudinary: %s" % str(e))

        # Delete the student record
        if student_models.Students.delete(id_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed to delete student")

    except Exception as e:
        # Log the error for debugging purposes
        current_app.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500



@student_bp.route('/students/add', methods=['POST', 'GET'])
def add():
    form = StudentForm()
    all_courses = student_models.Students.get_all_courses()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            profile_pic = request.files['profile_pic']
            check_id = form.id_number.data
            student_exists = student_models.Students.unique_code(check_id)

            if student_exists:
                flash("Student already exists! Please enter a unique id_number", 'error')
            else:
                if profile_pic:
                    # Call the add method from Students class
                    if student_models.Students.add(
                        check_id,
                        form.first_name.data,
                        form.last_name.data,
                        form.course_code.data,
                        form.year_.data,
                        form.gender.data,
                        profile_pic
                    ):
                        print("Student added successfully, and profile photo has been uploaded to Cloudinary")
                        flash("Student added successfully!", 'success')
                else:
                    student_models.Students.add(check_id,
                        form.first_name.data,
                        form.last_name.data,
                        form.course_code.data,
                        form.year_.data,
                        form.gender.data,
                        profile_pic=None)
                    flash("Student added successfully!", 'success')

                # Redirect to the students page or any other page
                return redirect(url_for('students.students'))

        except ValidationError as e:
            flash(str(e), 'error')

    return render_template('add_student.html', form=form, courses=all_courses)
    
@student_bp.route('/students/search', methods=['POST'])
def search_student():
    try:
        search_query = request.form.get('searchTerm')
        filter_by = request.form.get('filterBy')  # Get the filterBy parameter
        
        if filter_by == 'all':
            # If filterBy is 'all', perform a general search
            search_results = student_models.Students.search_student(search_query)
        else:
            # Otherwise, filter based on the selected column
            search_results = student_models.Students.filter_student(filter_by, search_query)
            
        return jsonify(search_results)
    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500


@student_bp.route('/students/info', methods=['POST', 'GET'])
def view_student_details():
    id_number = request.form.get('id_number')
    student_info = student_models.Students.view_student_info(id_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # This is an Ajax request
        return jsonify({'success': True, 'student_info': student_info})
    else:
        # This is a regular form submission, render the template
        return render_template('students.html', info=student_info)




