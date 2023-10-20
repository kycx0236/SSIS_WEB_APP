from flask import render_template, redirect, request, flash, url_for, jsonify
from . import college_bp
import app.models.college_models as college_models
from app.college.forms import CollegeForm

headings = ("College Code", "College Name")

@college_bp.route("/college")
def college_display():
    college_data = college_models.College.all()
    return render_template('college.html', headings=headings, data=college_data)

@college_bp.route('/college/edit', methods=["GET", "POST"])
def edit_college():
    college_code = request.args.get('college_code')
    form = CollegeForm()
    data_college = college_models.College.get_college_id(college_code)

    if data_college:
        college_data_dict = {
            "college_code": data_college['college_code'],
            "college_name": data_college['college_name'],
        }
    else:
        # Handle the case where no student data was found
        flash("College not found.", "error")
        return redirect(url_for("college.college_display"))

    if request.method == "POST" and form.validate():
        new_college_name = form.college_name

        if college_models.College.update(college_code, new_college_name):
            flash("College information updated successfully!", "success")
            return redirect(url_for("college.college_display"))
        else:
            flash("Failed to update student information.", "error")

    return render_template("edit_college.html", form=form, row=college_data_dict)


@college_bp.route("/edit/delete", methods=["POST"])
def delete_college():
    try:
        id_number = request.form.get('id_number')
        if college_models.College.delete(id_number):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed")
    except Exception as e:
        # Log the error for debugging purposes
        college_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500

@college_bp.route('/students/add', methods=['POST', 'GET'])
def add():
    form = CollegeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        check_college_code = form.college_code.data
        student_exists = college_models.College.unique_code(check_college_code)

        if student_exists:
            flash("Student already exists! Please enter a unique id_number", 'error')
        else:
            college = college_models.Students(
                college_code=check_college_code,
                college_name=form.college_name.data
            )
            college.add()
            flash("College added successfully!", 'success')
            return redirect(url_for('college.college_display'))
    
    return render_template('add_college.html', form=form)


@college_bp.route('/college/search', methods=['POST'])
def search_students():    
    query = request.form.get('search_query')
    college_data = college_models.College.search(query)
    return render_template('students.html', headings=headings, data=college_data)

