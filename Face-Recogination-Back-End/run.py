from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    UPLOAD_FOLDER = 'Image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    from Models.student import Student
    from Models.attendence import Attendance

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(file, filename):
        if allowed_file(filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(f"File saved at {file_path}")
            return file_path
        return None

    @app.route("/save_student", methods=['POST'])
    def save_user():
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        photo = request.files.get('photo')

        if not name or not student_id or not photo:
            return jsonify({"message": "Please fill in all fields"}), 400

        file_path = upload_file(photo, photo.filename)
        new_student = Student(name=name, student_id=student_id, photo=file_path)

        try:
            db.session.add(new_student)
            db.session.commit()
            return jsonify({"message": "Student saved successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error saving student", "error": str(e)}), 500

  

    def generate_image():
        IMAGE_FILES = []
        filename = []
        image_dir = app.config['UPLOAD_FOLDER']
        for image_name in os.listdir(image_dir):
            img_path = os.path.join(image_dir, image_name)
            if os.path.isfile(img_path):
                image = face_recognition.load_image_file(img_path)
                IMAGE_FILES.append(image)
                filename.append(image_name.split(".", 1)[0])
        return IMAGE_FILES, filename
    
        

    def encoding_img(image_files):
        encode_list = []
        for img in image_files:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(img_rgb)
            if encodings:
                encode_list.append(encodings[0])
        return encode_list
    
    
    def add_attendance(name):
        with open('attendence.csv', 'r+') as f:
            my_people_list = f.readlines()
            date_list = []
            now = datetime.now()
            date_string = now.strftime('%m/%d/%Y')

            for line in my_people_list:
                entry = line.split(',')
                date_list.append(entry)
                if(len(entry) >= 2 and entry[0] == name and entry[1] == date_string):
                    return 
                else:
                    print(f"Skipping invalid line: {line.strip()}") 
            time_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{date_string},{time_string}')



    @app.route("/video_feed")
    def video_feed():
        def generate_video_stream():
            IMAGE_FILES, filename = generate_image()
            encode_list_known = encoding_img(IMAGE_FILES)

            cap = cv2.VideoCapture(0)
            while True:
                success, img = cap.read()
                if not success:
                    break
                # Resize for faster processing
                img_resized = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(img_rgb)
                face_encodings_current = face_recognition.face_encodings(img_rgb, face_locations)

                for encode_face, face_loc in zip(face_encodings_current, face_locations):
                    matches_face = face_recognition.compare_faces(encode_list_known, encode_face)
                    face_distance = face_recognition.face_distance(encode_list_known, encode_face)
                    match_index = np.argmin(face_distance)

                    if matches_face[match_index]:
                        name = filename[match_index].upper()
                        put_text = 'Captured'

                        y1, x2, y2, x1 = face_loc
                        # Draw rectangle around face
                        cv2.rectangle(img, (x1 * 4, y1 * 4), (x2 * 4, y2 * 4), (255, 0, 0), 2)
                        cv2.putText(img, put_text, (x1 * 4 + 6, y2 * 4 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        add_attendance(name)

                # Encode frame to display
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            cap.release()
            cv2.destroyAllWindows()

        return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    



    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)



        


 


                

