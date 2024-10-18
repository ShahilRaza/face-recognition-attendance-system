import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:shariq%40123@localhost:5432/Face_Recognition_System'
    SQLALCHEMY_TRACK_MODIFICATIONS = False,

    CLOUDINARY_URL = "cloudinary://789895926322396:qakNaRkfdu1xINkz0nRXXamYhAA6@dfvjn2ec0"
    UPLOAD_FOLDER = r'D:\Face-recoginations-app\Face-Recogination-Back-End\Image'