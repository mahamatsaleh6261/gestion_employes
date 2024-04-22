from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from app.extensions import db
from app.models import Employee, User

main_bp = Blueprint("main_bp", __name__)
employee_bp = Blueprint("employee_bp", __name__, url_prefix="/employees")


@main_bp.route("/", methods=["POST", "GET"])
def dashboard():
    employees = Employee.query.all()
    return render_template("dashboard.html", employees=employees)


@employee_bp.route("/create/", methods=["POST", "GET"])
def employee_create():
    if request.method == "POST":
        employee = Employee()
        employee.firstname = request.form["firstname"]
        employee.lastname = request.form["lastname"]
        employee.gender = request.form["gender"]
        employee.date_of_birth = request.form["date_of_birth"]
        employee.phone_number = request.form["phone_number"]
        employee.email = request.form["email"]
        employee.address = request.form["address"]
        employee.position = request.form["position"]
        employee.department = request.form["department"]
        employee.salary = request.form["salary"]
        employee.is_active = True if "is_active" in request.form else False
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for("employee_bp.employee_list"))
    return render_template("employee_create.html")


@employee_bp.route("/update/<int:id>", methods=["POST", "GET"])
def employee_update(id: int):
    employee = Employee.query.get(id)
    if not employee:
        return redirect(url_for("employee_bp.employee_list"))

    if request.method == "POST":
        employee.firstname = request.form["firstname"]
        employee.lastname = request.form["lastname"]
        employee.gender = request.form["gender"]
        employee.date_of_birth = request.form["date_of_birth"]
        employee.phone_number = request.form["phone_number"]
        employee.email = request.form["email"]
        employee.address = request.form["address"]
        employee.position = request.form["position"]
        employee.department = request.form["department"]
        employee.salary = request.form["salary"]
        employee.is_active = True if "is_active" in request.form else False
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for("employee_bp.employee_list"))
    return render_template("employee_create.html", employee=employee)


@employee_bp.route("/", methods=["POST", "GET"])
def employee_list():
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    query = request.args.get("search")
    order_by = request.args.get("order_by")

    if query:
        employees = Employee.query.filter(
            (Employee.firstname.contains(query))
            | (Employee.lastname.contains(query))
            | (Employee.position.contains(query))
            | (Employee.department.contains(query))
            | (Employee.salary.contains(query))
        ).all()

    if order_by == "firstname_asc":
        employees = Employee.query.order_by(Employee.firstname).all()
    elif order_by == "firstname_desc":
        employees = Employee.query.order_by(Employee.firstname.desc()).all()
    elif order_by == "lastname_asc":
        employees = Employee.query.order_by(Employee.lastname).all()
    elif order_by == "lastname_desc":
        employees = Employee.query.order_by(Employee.lastname.desc()).all()
    elif order_by == "position_asc":
        employees = Employee.query.order_by(Employee.position).all()
    elif order_by == "position_desc":
        employees = Employee.query.order_by(Employee.position.desc()).all()
    elif order_by == "department_asc":
        employees = Employee.query.order_by(Employee.department).all()
    elif order_by == "department_desc":
        employees = Employee.query.order_by(Employee.department.desc()).all()
    elif order_by == "salary_asc":
        employees = Employee.query.order_by(Employee.salary).all()
    elif order_by == "salary_desc":
        employees = Employee.query.order_by(Employee.salary.desc()).all()
    elif order_by == "status_asc":
        employees = Employee.query.order_by(Employee.is_active).all()
    elif order_by == "status_desc":
        employees = Employee.query.order_by(Employee.is_active.desc()).all()
    elif order_by == "address_asc":
        employees = Employee.query.order_by(Employee.address).all()
    elif order_by == "address_desc":
        employees = Employee.query.order_by(Employee.address.desc()).all()

    employee_list = []
    for employee in employees:
        employee.created_at = datetime.strptime(
            employee.created_at, "%Y-%m-%d %H:%M:%S.%f"
        ).strftime("%Y-%m-%d")
        employee_list.append(employee)
    return render_template("employee_list.html", employees=employee_list)


@employee_bp.route("/delete/<int:id>", methods=["POST", "GET"])
def employee_delete(id: int):
    if employee := Employee.query.get(id):
        db.session.delete(employee)
        db.session.commit()
    return redirect(url_for("employee_bp.employee_list"))
