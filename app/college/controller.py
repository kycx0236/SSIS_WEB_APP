from flask import render_template, redirect, request, flash, url_for, jsonify
from . import college_bp
import app.models.college_models as college_models
from app.college.forms import CollegeForm

headings = ("College Code", "College Name", "Options")

@college_bp.route("/college/display")
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
        # Handle the case where no college data was found
        flash("College info cannot be edited.", "error")
        return redirect(url_for("college.college_display"))

    if request.method == "POST" and form.validate():
        new_college_name = form.college_name

        if college_models.College.update(college_code, new_college_name):
            flash("College information updated successfully!", "success")
            return redirect(url_for("college.college_display"))
        else:
            flash("Failed to update college information.", "error")

    return render_template("edit_college.html", form=form, row=college_data_dict)


@college_bp.route("/college/delete", methods=["POST"])
def delete_college():
    try:
        college_code = request.form.get('college_code')  # Correct the variable name
        if college_models.College.delete(college_code):
            return jsonify(success=True, message="Successfully deleted")
        else:
            return jsonify(success=False, message="Failed since there are enrolled students")
    except Exception as e:
        # Log the error for debugging purposes
        college_bp.logger.error("An error occurred: %s" % str(e))
        return jsonify(success=False, message="Internal Server Error"), 500


@college_bp.route('/college/add', methods=['POST', 'GET'])
def add():
    form = CollegeForm(request.form)
    
    if request.method == 'POST' and form.validate():
        check_code = form.college_code.data
        student_exists = college_models.College.unique_code(check_code)

        if student_exists:
            flash("College already exists! Please enter a unique code", 'error')
        else:
            college = college_models.College(
                college_code=check_code,
                college_name=form.college_name.data,
            )
            college.add()
            flash("College added successfully!", 'success')
            return redirect(url_for('college.college_display'))
    
    return render_template('add_college.html', form=form)


@college_bp.route('/college/search', methods=['POST'])
def search_college():
    try:
        search_query = request.form.get('searchTerm')  # Updated to 'searchTerm'
        search_results = college_models.College.search_college(search_query)
        
        if search_results:
            flash("We found it!", 'success')
        else:
            flash("We could not find it!", 'error')

        return jsonify(search_results)

    except Exception as e:
        # Handle errors and return an error response
        return jsonify(error=str(e)), 500

