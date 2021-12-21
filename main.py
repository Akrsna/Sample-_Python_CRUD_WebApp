from flask import Flask, render_template, request, redirect
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://achythu:achu123@db/students'
app.config['SECRET_KEY'] = "abcdefg"
db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

subscribers = []

@app.route('/students', methods=['POST','GET'])
def students():
    if request.method == "POST":
        student_fname = request.form['first_name']
        student_lname = request.form['last_name']
        student_email = request.form['email']
        new_student = Students(first_name=student_fname,last_name=student_lname, email=student_email)
        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect('/students')
        except:
            return "There was an error adding student"

    else:
        students = Students.query.order_by(Students.date_created)
        return render_template("students.html", students=students)

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    student_to_update = Students.query.get_or_404(id)
    if request.method == "POST":
        student_to_update.first_name = request.form['first_name']
        student_to_update.last_name = request.form['last_name']
        student_to_update.email = request.form['email']

        try:
            db.session.commit()
            return redirect('/students')
        except:
            return "There was an error updating student"

    else:
        return render_template("update.html", student_to_update=student_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    student_to_delete = Students.query.get_or_404(id)
    try:
            db.session.delete(student_to_delete)
            db.session.commit()
            return redirect('/students')

    except:
            return "There was an error deleting student"



@app.route('/subscribe')
def subscribe():
    return render_template("subscribe.html")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    if not first_name or not last_name or not email:
        error_stat = "All fields required..."
        return render_template("subscribe.html", error_stat=error_stat,first_name=first_name, last_name=last_name,
                               email=email)
    subscribers.append(f"{first_name} {last_name} || {email}")
    return render_template('form.html', len=len(subscribers), subscribers=subscribers)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8080", debug=True)
