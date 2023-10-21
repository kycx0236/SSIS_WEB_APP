from flask import Flask
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect

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
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    # Initialize CSRF protection before registering blueprints
    CSRFProtect(app)

    from .students import student_bp as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/')
    
    from .college import college_bp
    app.register_blueprint(college_bp)
    """
    from .courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')
    """
    bootstrap.init_app(app)
    mysql.init_app(app)

    return app
