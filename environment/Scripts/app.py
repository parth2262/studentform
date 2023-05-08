from flask import Flask , redirect , render_template , url_for , request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///STUDENT1.db'
db = SQLAlchemy(app)



class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    roll_no = db.Column(db.Integer, nullable=False )
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


   


@app.route('/')    
def home():
    return render_template('home.html')


# <<<<<------------------ragister page--------------------->>>>>>

@app.route('/ragister', methods=['POST', 'Get'])
def ragister():
    if request.method == 'GET':
        subjects = Subject.query.all()
        teachers = Teacher.query.all()
        return render_template('ragister.html', subjects=subjects, teachers=teachers)
    
    
    else:
        name = request.form['name']
        roll_no = request.form['rollno']
        subject_id = request.form['subject']
        teacher_id = request.form['teacher']
        marks = request.form['marks']

        student = Student(name=name, roll_no=roll_no, subject_id=subject_id,
                          teacher_id=teacher_id, marks=marks)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('show'))
    return render_template('ragister.html')

# <<<<<------------------Data show page--------------------->>>>>>    
    
@app.route('/show')
def show():
    all_std = Student.query.all()
    for std in all_std:
        std.subject_id = Subject.query.get(std.subject_id).name
        std.teacher_id = Teacher.query.get(std.teacher_id).name
    return render_template('show.html', students= all_std)

# <<<<<------------------Delete page--------------------->>>>>>

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    dc = Student.query.get(id)
    db.session.delete(dc)
    db.session.commit()
    return redirect(url_for('show'))


# <<<<<------------------Update page--------------------->>>>>>

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get(id)
    if request.method == 'GET':
        subjects = Subject.query.all()
        teachers = Teacher.query.all()
        return render_template('edit.html', student=student, subjects=subjects, teachers=teachers)
    else:
      
        student.name = request.form['name']
        student.roll_no = request.form['rollno']
        student.subject_id = request.form['subject']
        student.teacher_id = request.form['teacher']
        student.marks = request.form['marks']
        db.session.commit()

        return redirect(url_for('show'))
    
# <<<<<------------------Result page--------------------->>>>>>

@app.route('/calculate', methods=['GET', 'POST'])
def calculate_percentage():
    total_marks = 0
    if request.method == 'POST':
        roll_no = request.form['roll_no']   
        student = Student.query.filter_by(roll_no=roll_no)
        all_std = Student.query.all()
        if student: 
            for roll_no in student:
                total_marks = total_marks + roll_no.marks
                percentage = (total_marks / 300) * 100
            return render_template('result.html',student=student, total_marks=total_marks, percentage=percentage)
        
    return render_template('calculate.html')


with app.app_context():
    db.create_all()  
    



