from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Configuration Class
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_LIFETIME = int(os.getenv("ACCESS_TOKEN_LIFETIME", 30))
    REFRESH_TOKEN_LIFETIME = int(os.getenv("REFRESH_TOKEN_LIFETIME", 7))
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Configuration Instance
config = Config
