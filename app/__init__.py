from flask import Flask
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import (
    SECRET_KEY,
    DB_USERNAME,
    DB_PASSWORD,
    DB_NAME,
    DB_HOST,
    BOOTSTRAP_SERVE_LOCAL,
    CLOUD_NAME, API_KEY, API_SECRET,
    CLOUDINARY_URL,
)
from flask_wtf.csrf import CSRFProtect
import cloudinary
from cloudinary.api import create_folder

mysql = MySQL()
bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        CLOUDINARY_URL=CLOUDINARY_URL,
        # BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )
    cloudinary.config( 
        cloud_name = CLOUD_NAME, 
        api_key = API_KEY, 
        api_secret = API_SECRET,
        secure=True,
    )
    
    # Specify the name of the new folder you want to create
    folder_name = "SSIS"

    # Create the folder using the Cloudinary API
    create_folder(folder_name)
    print(f"Folder '{folder_name}' created successfully.")

    # Initialize CSRF protection before registering blueprints
    CSRFProtect(app)

    from .students import student_bp as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/')
    
    from .college import college_bp as college_bluprint
    app.register_blueprint(college_bluprint)

    from .courses import courses_bp as courses_bluprint
    app.register_blueprint(courses_bluprint)

    bootstrap.init_app(app)
    mysql.init_app(app)

    return app
