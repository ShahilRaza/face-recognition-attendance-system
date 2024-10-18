from run import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200), nullable=False)  
    student_id = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

