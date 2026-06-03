from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "studentapp123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="daemon1234",
    database="StudentDB"
)

cursor = db.cursor(dictionary=True)

# HOME
@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)

# ADD STUDENT
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    cursor.execute(
        "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
        (name, email, course)
    )
    db.commit()

    flash("Student added successfully!", "success")
    return redirect('/')

# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()

    flash("Student deleted successfully!", "danger")
    return redirect('/')

# EDIT STUDENT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        cursor.execute("""
            UPDATE students
            SET name=%s, email=%s, course=%s
            WHERE id=%s
        """, (name, email, course, id))

        db.commit()
        flash("Student updated successfully!", "info")
        return redirect('/')

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template('edit.html', student=student)

if __name__ == '__main__':
    print("Server running...")
    app.run(debug=True)