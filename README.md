# Face Recognition Attendance System
Overview
This project is a Face Recognition-based Attendance System that automates the process of recording student attendance by detecting faces through a camera. The system uses Python, Flask, OpenCV, and React.js to create an efficient, user-friendly platform. Student faces are recognized in real-time using OpenCV, and their attendance is stored in a CSV file. The system provides a web interface for admins and students to interact with

Features:
Real-time Face Recognition: Uses OpenCV to detect and recognize students' faces via a live camera feed.
Attendance Recording: Automatically records attendance based on face recognition and stores it in a CSV file.
Admin Panel: Admins can manage student profiles, including uploading photos and viewing/editing attendance records.
Student Profile: Students can view their own profiles and attendance history.
Front-End: Developed using React.js for creating dynamic and responsive web pages.
Back-End: Powered by Flask with APIs for student data management and attendance processing.

Technologies Used:
Python: For the backend logic and integration of OpenCV and Flask.
Flask: To create a RESTful API for managing students, attendance records, and communication between the front-end and back-end.
OpenCV: For image processing and face recognition.
React.js: For building the front-end interface.
SQLAlchemy: To manage student data and attendance.
CSV: Used to store attendance records.
PostgreSQL (optional): For storing student information (if using a relational database).

Workflow:
Student Registration:

Admins upload student details and photos to the system.
Student photos are used to train the face recognition model.
Attendance Marking:

The student stands in front of the camera.
OpenCV processes the live camera feed to detect faces and match them with the registered student photos.
If a face is recognized, the student's attendance is marked and stored in a CSV file.
Data Storage:

Attendance is recorded with a timestamp and saved to a CSV file for easy retrieval.
CSV files can be exported or integrated with other systems if needed
