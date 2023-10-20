{% extends 'base.html' %}
{% block title %}
   Add Student Page
{% endblock %}

{% block content %}

    {%for message in get_flashed_messages() %}
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>{{ message }}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    {% endfor %}

    <div class="shadow p-3 mb-5 bg-body-tertiary rounded">
        <h1>ADD STUDENT INFO</h1>
        <br/><br/>
        <form class="row g-3 needs-validation" method="POST" action="/students/add" novalidate>
            <!-- ID Number -->
            <div class="col-md-4">
                <label for="validationCustom01" class="form-label">ID Number</label>
                <input type="text" placeholder="YYYY-NNNN" class="form-control" id="validationCustom01" name="id_number" required>
                <div class="valid-feedback">
                    Looks good!
                </div>
                <div class="invalid-feedback">
                    Please enter your ID Number.
                </div>
            </div>
            <!-- First Name -->
            <div class="col-md-4">
                <label for="validationCustom02" class="form-label">First Name</label>
                <input type="text" class="form-control" id="validationCustom02" name="first_name" required>
                <div class="valid-feedback">
                    Looks good!
                </div>
                <div class="invalid-feedback">
                    Please enter your First Name.
                </div>
            </div>
            <!-- Last Name -->
            <div class="col-md-4">
                <label for="validationCustomUsername" class="form-label">Last Name</label>
                <div class="input-group has-validation">
                    <input type="text" class="form-control" id="validationCustomUsername" name="last_name" required>
                    <div class="invalid-feedback">
                        Please enter your Last Name.
                    </div>
                </div>
            </div>
            <!-- Course Code -->
            <div class="col-md-4">
                <label for="validationCustom03" class="form-label">Course Code</label>
                <input type="text" placeholder="e.g., BSCS" class="form-control" id="validationCustom03" name="course_code" required>
                <div class="invalid-feedback">
                    Please provide your Course Code.
                </div>
            </div>
            <!-- Year -->
            <div class="col-md-4">
                <label for="validationCustom04" class="form-label">Year</label>
                <select class="form-select" id="validationCustom04" name="year_" required>
                    <option selected disabled value="">Choose...</option>
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                    <option>4</option>
                </select>
                <div class="invalid-feedback">
                    Please select your year.
                </div>
            </div>
            <!-- Gender -->
            <div class="col-md-4">
                <label for="validationCustom05" class="form-label">Gender</label>
                <select class="form-select" id="validationCustom05" name="gender" required>
                    <option selected disabled value="">Choose...</option>
                    <option>M</option>
                    <option>F</option>
                    <option>Others</option>
                </select>
                <div class="invalid-feedback">
                    Please select your Gender.
                </div>
            </div>
            <br/><br/>
            <!-- Checkbox for input validation -->
            <div class="col-12">
                <div class="form-check">
                    <br/>
                    <input class="form-check-input" type="checkbox" value="" id="invalidCheck" name="input_correct" required>
                    <label class="form-check-label" for="invalidCheck">
                        Please check if your input is correct.
                    </label>
                    <div class="invalid-feedback">
                        You must agree before submitting.
                    </div>
                </div>
            </div>
            <div class="col-12">
                <!-- Add the CSRF token input here -->
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                <button class="btn btn-outline-dark" type="submit">Submit</button>
            </div>
        </form>
    </div>

    <!-- Include these script tags -->
    <script src="{{ url_for('static', filename='javascript/JQ.js') }}"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        // Example starter JavaScript for disabling form submissions if there are invalid fields
        (() => {
            'use strict'
        
            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            const forms = document.querySelectorAll('.needs-validation')
        
            // Loop over them and prevent submission
            Array.from(forms).forEach(form => {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
        
                    form.classList.add('was-validated')
                }, false)
            })
        })();
        
        // Add this JavaScript block after the form
        (() => {
            'use strict';
        
            // Function to add the CSRF token to form data
            const addCSRFTokenToFormData = (form) => {
                const csrfToken = document.querySelector('input[name=csrf_token]');
                if (csrfToken) {
                    const csrfField = document.createElement('input');
                    csrfField.type = 'hidden';
                    csrfField.name = 'csrf_token';
                    csrfField.value = csrfToken.value;
                    form.appendChild(csrfField);
                }
            };
        
            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            const forms = document.querySelectorAll('.needs-validation');
        
            // Loop over them and prevent submission
            Array.from(forms).forEach(form => {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    } else {
                        // Add the CSRF token to the form data
                        addCSRFTokenToFormData(form);
                    }
        
                    form.classList.add('was-validated');
                }, false);
            });
        })();  
    </script>
{% endblock %}
