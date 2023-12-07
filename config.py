from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")

CLOUD_NAME = getenv("CLOUD_NAME")
API_KEY = getenv("API_KEY")
API_SECRET = getenv("API_SECRET")

CLOUDINARY_URL = getenv("CLOUDINARY_URL")  # Retrieve Cloudinary URL from environment

# If you need to use the Cloudinary URL directly in your application, you can use it like this:
# CLOUDINARY_URL = "cloudinary://716415177617336:O1CpH3Q5Jzmt3zhIJ1q6mpSx7ho@df5spbme7"
