from run import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    attendance_status = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', backref='attendances')

    def __repr__(self):
        return f'<Attendance {self.date} - {self.student_id}>'
    
