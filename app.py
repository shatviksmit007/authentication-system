from flask import Flask, request, render_template, redirect, url_for, send_file, session, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField  # Added SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import uuid
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'djfldksajglkdgl'

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin):
    def __init__(self, admission_number):
        self.admission_number = admission_number
        self.id = admission_number

@login_manager.user_loader
def load_user(admission_number):
    return User(admission_number=admission_number)


class LoginForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[InputRequired(), Length(min=4, max=20)])
    passcode = PasswordField('Passcode', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    user = None


    form = LoginForm()

    if form.validate_on_submit(): 
        admission_number = form.admission_number.data
        passcode = form.passcode.data

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT admission_number, name, father_name, mother_name, is_used FROM students WHERE admission_number = ? AND passcode = ?",
                   (admission_number, passcode))

        student_data = cursor.fetchone()

        if student_data and student_data[4] == 0:
            student_dict = {
                "admission_number": student_data[0],
                "name": student_data[1],
                "father_name": student_data[2],
                "mother_name": student_data[3]
            }

            user = User(student_dict['admission_number'])
            login_user(user)
            cursor.execute("UPDATE students SET is_used=1 WHERE admission_number = ?", (admission_number,))
            conn.commit()
            return redirect(url_for('welcome'))
        elif student_data[4] == 1:
            error = "You have already entered once. Multiple entries are not allowed. If you believe this is an error, please contact our support team."
        else: 
            error = "The admission number or passcode is incorrect. Please try again later."

    return render_template('login.html', form=form, error=error)

@app.route('/welcome')
@login_required
def welcome():
        admission_number = current_user.admission_number
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT admission_number, name, father_name, mother_name, class FROM students WHERE admission_number = ?",
                   (admission_number,))

        student_data = cursor.fetchone()
        student_dict = {
                "admission_number": student_data[0],
                "name": student_data[1],
                "father_name": student_data[2],
                "mother_name": student_data[3],
                "class": student_data[4]
            }

            
        return render_template('welcome.html', student_dict=student_dict)   
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
