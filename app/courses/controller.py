from flask import render_template, redirect, request, flash, url_for, jsonify
from . import courses_bp
import app.models.courses_models as courses_models
from app.courses.forms import CourseForm

headings = ("Course Code", "Course Name", "College Code", "Options")

@courses_bp.route("/course/display")
def course_display():
    course_data = courses_models.Courses.all()
    return render_template('courses.html', headings=headings, data=course_data)

@courses_bp.route('/course/edit', methods=["GET", "POST"])
def edit_courses():
    course_code = request.args.get('course_code')
    form = CourseForm()
    course_data = courses_models.Courses.get_course_code(course_code)
    college_code = courses_models.Courses.get_college_codes()

    if course_data:
        course_data_dict = {
            "course_code": course_data['course_code'],
            "course_name": course_data['course_name'],
            "college_code": course_data['college_code']
        }
    else:
        # Handle the case where no course data was found
        flash("Course data cannot be edited.", "error")
        return redirect(url_for("courses.course_display"))

    if request.method == "POST" and form.validate():
        new_course_name = request.form.get('course_name')
        new_college_code = request.form.get('college_code')

        if courses_models.Courses.update(course_code, new_course_name, new_college_code):
            flash("Course information updated successfully!", "success")
            return redirect(url_for("courses.course_display"))
        else:
            flash("Failed to update course information.", "error")
            
    return render_template("edit_course.html", form=form, row=course_data_dict, colleges=college_code)


@courses_bp.route("/course/delete", methods=["POST"])
def delete_course():
    try:
        course_code = request.form.get('course_code')  # Correct the variable name
        if courses_models.Courses.delete(course_code):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed since there are enrolled students in the course")
    except Exception as e:
        # Log the error for debugging purposes
        courses_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500


@courses_bp.route('/course/add', methods=['POST', 'GET'])
def add_course():
    form = CourseForm(request.form)
    college_code = courses_models.Courses.get_college_codes()
    
    if request.method == 'POST' and form.validate():
        check_code = form.course_code.data
        course_exists = courses_models.Courses.unique_code(check_code)

        if course_exists:
            flash("Course already exists! Please enter a unique code", 'error')
        else:
            course = courses_models.Courses(
                course_code=check_code,
                course_name=form.course_name.data,
                college_code=form.college_code.data
            )
            if course.add():
                flash("Course added successfully!", 'success')
                return redirect(url_for('courses.course_display'))
            else:
                flash("Failed to add the course. Please check your inputs.", 'error')
    
    return render_template('add_courses.html', form=form, colleges=college_code)


@courses_bp.route('/course/search', methods=['POST'])
def search_course():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        search_results = courses_models.Courses.search(search_query)
        return jsonify(search_results)

    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500
