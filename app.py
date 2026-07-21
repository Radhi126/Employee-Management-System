import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    send_file
)
from db import get_db_connection

app = Flask(__name__)
app.secret_key = "employee_secret_key"


@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "EMS@2026":
            session["admin"] = username
            return redirect("/dashboard")

        flash("Invalid Username or Password", "danger")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Employees
    cursor.execute("SELECT COUNT(*) AS total FROM employee")
    total_employees = cursor.fetchone()["total"]

    # Total Departments
    cursor.execute("SELECT COUNT(*) AS total FROM department")
    total_departments = cursor.fetchone()["total"]

    # Total Salary
    cursor.execute("SELECT SUM(salary) AS total_salary FROM employee")
    salary = cursor.fetchone()["total_salary"] or 0

    # Recent Employees (Latest 5 but shown in ascending order)
    cursor.execute("""
        SELECT *
        FROM (
            SELECT *
            FROM employee
            ORDER BY emp_id DESC
            LIMIT 5
        ) AS recent_employees
        ORDER BY emp_id ASC
    """)

    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        total_departments=total_departments,
        total_salary=salary,
        employees=employees
    )


@app.route("/employees")
def employees():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM department
        ORDER BY dept_name
    """)
    departments = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM employee
        ORDER BY emp_id ASC
    """)
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "employees.html",
        employees=employees,
        departments=departments
    )

@app.route("/save_employee", methods=["POST"])
def save_employee():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    emp_id = request.form.get("emp_id", "")

    emp_name = request.form["emp_name"].strip()
    age = request.form["age"]
    gender = request.form["gender"]
    department = request.form["department"]
    designation = request.form["designation"].strip()
    salary = request.form["salary"]
    phone = request.form["phone"].strip()
    email = request.form["email"].strip()
    address = request.form["address"].strip()

    # Duplicate Email Check
    cursor.execute(
        "SELECT * FROM employee WHERE email=%s",
        (email,)
    )

    existing = cursor.fetchone()

    if existing:

        # While Adding
        if emp_id == "":
            flash("Email already exists!", "warning")
            cursor.close()
            conn.close()
            return redirect("/employees")

        # While Updating
        elif str(existing["emp_id"]) != emp_id:
            flash("Email already exists!", "warning")
            cursor.close()
            conn.close()
            return redirect("/employees")

    # Add Employee
    if emp_id == "":

        cursor.execute("""
            INSERT INTO employee
            (
                emp_name,
                age,
                gender,
                department,
                designation,
                salary,
                phone,
                email,
                address
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            emp_name,
            age,
            gender,
            department,
            designation,
            salary,
            phone,
            email,
            address
        ))

        flash("Employee added successfully!", "success")

    # Update Employee
    else:

        cursor.execute("""
            UPDATE employee
            SET
                emp_name=%s,
                age=%s,
                gender=%s,
                department=%s,
                designation=%s,
                salary=%s,
                phone=%s,
                email=%s,
                address=%s
            WHERE emp_id=%s
        """, (
            emp_name,
            age,
            gender,
            department,
            designation,
            salary,
            phone,
            email,
            address,
            emp_id
        ))

        flash("Employee updated successfully!", "success")

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/employees")


@app.route("/delete_employee/<int:id>")
def delete_employee(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employee WHERE emp_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Employee deleted successfully!", "success")

    return redirect("/employees")

@app.route("/departments")
def departments():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM department
        ORDER BY dept_id ASC
    """)

    departments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "departments.html",
        departments=departments
    )

@app.route("/save_department", methods=["POST"])
def save_department():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    dept_id = request.form.get("dept_id", "")
    dept_name = request.form["dept_name"].strip()

    # Duplicate Check
    cursor.execute(
        "SELECT * FROM department WHERE dept_name=%s",
        (dept_name,)
    )

    existing = cursor.fetchone()

    if existing:

        # While Adding
        if dept_id == "":
            flash("Department already exists!", "warning")
            cursor.close()
            conn.close()
            return redirect("/departments")

        # While Updating
        elif str(existing["dept_id"]) != dept_id:
            flash("Department already exists!", "warning")
            cursor.close()
            conn.close()
            return redirect("/departments")

    # Add Department
    if dept_id == "":

        cursor.execute(
            """
            INSERT INTO department(dept_name)
            VALUES(%s)
            """,
            (dept_name,)
        )

        flash("Department added successfully!", "success")

    # Update Department
    else:

        cursor.execute(
            """
            UPDATE department
            SET dept_name=%s
            WHERE dept_id=%s
            """,
            (dept_name, dept_id)
        )

        flash("Department updated successfully!", "success")

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/departments")

@app.route("/delete_department/<int:id>")
def delete_department(id):

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM department WHERE dept_id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Department deleted successfully!", "success")

    return redirect("/departments")

@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Employees
    cursor.execute("SELECT COUNT(*) AS total FROM employee")
    total_employees = cursor.fetchone()["total"]

    # Total Departments
    cursor.execute("SELECT COUNT(*) AS total FROM department")
    total_departments = cursor.fetchone()["total"]

    # Salary Report
    cursor.execute("""
        SELECT
            SUM(salary) AS total_salary,
            AVG(salary) AS avg_salary,
            MAX(salary) AS max_salary,
            MIN(salary) AS min_salary
        FROM employee
    """)

    report = cursor.fetchone()

    total_salary = report["total_salary"] or 0
    avg_salary = report["avg_salary"] or 0
    max_salary = report["max_salary"] or 0
    min_salary = report["min_salary"] or 0

    cursor.close()
    conn.close()

    return render_template(
        "reports.html",
        total_employees=total_employees,
        total_departments=total_departments,
        total_salary=total_salary,
        avg_salary=avg_salary,
        max_salary=max_salary,
        min_salary=min_salary
    )
    
@app.route("/export")
def export():

    if "admin" not in session:
        return redirect("/login")

    conn = get_db_connection()

    query = """
        SELECT
            emp_id AS 'Employee ID',
            emp_name AS 'Employee Name',
            age AS 'Age',
            gender AS 'Gender',
            department AS 'Department',
            designation AS 'Designation',
            salary AS 'Salary',
            phone AS 'Phone',
            email AS 'Email',
            address AS 'Address'
        FROM employee
        ORDER BY emp_id ASC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    filename = "Employee_Report.xlsx"

    df.to_excel(filename, index=False)

    return send_file(
        filename,
        as_attachment=True
    )
    
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)