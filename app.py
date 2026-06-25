from models.patient import Patient
from flask import Flask, render_template, request, redirect
from database.db import get_connection

app = Flask(__name__)

#HOME 

@app.route("/")
def home():
    return render_template("home.html")


#ADD PATIENT

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]

        patient = Patient(
            name,
            age,
            gender,
            phone
        )

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Patient
                (
                    PatientName,
                    Age,
                    Gender,
                    Phone
                )
                VALUES(%s,%s,%s,%s)
                """,
                patient.get_details()
            )

            con.commit()

            cur.close()
            con.close()

            return redirect("/patients")

        except Exception as e:
            return f"Error : {e}"

    return render_template("add_patient.html")

#UPDATE PATIENTS
@app.route("/update_patient/<int:id>", methods=["GET", "POST"])
def update_patient(id):

    con = get_connection()
    cur = con.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]

        cur.execute(
            """
            UPDATE Patient
            SET PatientName=%s,
                Age=%s,
                Gender=%s,
                Phone=%s
            WHERE PatientID=%s
            """,
            (name, age, gender, phone, id)
        )

        con.commit()

        cur.close()
        con.close()

        return redirect("/patients")

    cur.execute(
        "SELECT * FROM Patient WHERE PatientID=%s",
        (id,)
    )

    patient = cur.fetchone()

    return render_template(
        "update_patient.html",
        patient=patient
    )

#VIEW PATIENTS

@app.route("/patients")
def patients():

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM Patient")

        data = cur.fetchall()

        cur.close()
        con.close()

        return render_template(
            "view_patients.html",
            patients=data
        )

    except Exception as e:
        return f"Error: {e}"

#DELETE PATIENTS
@app.route("/delete_patient/<int:id>")
def delete_patient(id):

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM Patient WHERE PatientID=%s",
        (id,)
    )

    con.commit()

    cur.close()
    con.close()

    return redirect("/patients")

#ADD DOCTOR

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():

    if request.method == "POST":

        name = request.form["name"]
        specialization = request.form["specialization"]

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Doctor
                (DoctorName, Specialization)
                VALUES (%s,%s)
                """,
                (name, specialization)
            )

            con.commit()

            cur.close()
            con.close()

            return redirect("/")

        except Exception as e:
            return f"Error: {e}"

    return render_template("add_doctor.html")


#VIEW DOCTORS

@app.route("/doctors")
def doctors():

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM Doctor")

        data = cur.fetchall()

        cur.close()
        con.close()

        return str(data)

    except Exception as e:
        return f"Error: {e}"


#BOOK APPOINTMENT

@app.route("/book_appointment", methods=["GET", "POST"])
def book_appointment():

    if request.method == "POST":

        patientid = request.form["patientid"]
        doctorid = request.form["doctorid"]
        appointmentdate = request.form["appointmentdate"]

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO Appointment
                (
                    PatientID,
                    DoctorID,
                    AppointmentDate
                )
                VALUES
                (%s,%s,%s)
                """,
                (patientid, doctorid, appointmentdate)
            )

            con.commit()

            cur.close()
            con.close()

            return redirect("/appointments")

        except Exception as e:
            return f"Error: {e}"

    return render_template("book_appointment.html")


#VIEW APPOINTMENTS

@app.route("/appointments")
def appointments():

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            SELECT

            a.AppointmentID,
            p.PatientName,
            d.DoctorName,
            d.Specialization,
            a.AppointmentDate

            FROM Appointment a

            JOIN Patient p
            ON a.PatientID = p.PatientID

            JOIN Doctor d
            ON a.DoctorID = d.DoctorID
            """
        )

        data = cur.fetchall()

        cur.close()
        con.close()

        return str(data)

    except Exception as e:
        return f"Error: {e}"

#LIST
@app.route("/patient_names")
def patient_names():

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT PatientName FROM Patient"
    )

    rows = cur.fetchall()

    patient_list = []

    for row in rows:
        patient_list.append(row[0])

    cur.close()
    con.close()

    return str(patient_list)

#TUPLE
@app.route("/tuple_demo")
def tuple_demo():

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM Patient LIMIT 1"
    )

    patient = cur.fetchone()

    cur.close()
    con.close()

    return str(patient)

#DICTIONARY
@app.route("/patient_dictionary")
def patient_dictionary():

    patient = {

        "name": "Harini",

        "age": 21,

        "gender": "Female",

        "phone": "9344682374"
    }

    return str(patient)

#report
@app.route("/generate_report")
def generate_report():

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM Patient"
    )

    data = cur.fetchall()

    with open(
        "reports/patient_report.txt",
        "w"
    ) as file:

        file.write(
            "PATIENT REPORT\n\n"
        )

        for row in data:

            file.write(
                f"{row}\n"
            )

    cur.close()
    con.close()

    return "Patient Report Generated Successfully"

#SEARCH PATIENTS
@app.route("/search_patient",
methods=["GET","POST"])
def search_patient():

    patient = None

    if request.method == "POST":

        name = request.form["name"]

        con = get_connection()

        cur = con.cursor()

        cur.execute(
            """
            SELECT *
            FROM Patient
            WHERE PatientName=%s
            """,
            (name,)
        )

        patient = cur.fetchone()

        cur.close()
        con.close()

    return render_template(
        "search_patient.html",
        patient=patient
    )


if __name__ == "__main__":
    app.run(debug=True)