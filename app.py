from flask import Flask, render_template, request, make_response
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

# ---------- Home / Form Page ----------
@app.route("/")
def form():
    return render_template("form.html")

# ---------- Report Page ----------
@app.route("/report", methods=["POST"])
def report():
    name = request.form["name"]
    age = request.form["age"]
    bmi = request.form["bmi"]
    glucose = request.form["glucose"]
    bp = request.form["bp"]

    result = "Positive" if int(glucose) > 140 else "Negative"

    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M %p")

    return render_template(
        "report.html",
        name=name,
        age=age,
        bmi=bmi,
        glucose=glucose,
        bp=bp,
        result=result,
        date=date,
        time=time
    )

# ---------- PDF Download ----------
def create_pdf(html):
    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    return pdf

@app.route("/download", methods=["POST"])
def download():
    html = render_template(
        "report.html",
        name=request.form["name"],
        age=request.form["age"],
        bmi=request.form["bmi"],
        glucose=request.form["glucose"],
        bp=request.form["bp"],
        result=request.form["result"],
        date=request.form["date"],
        time=request.form["time"]
    )

    pdf = create_pdf(html)
    response = make_response(pdf.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=medical_report.pdf"
    return response

if __name__ == "__main__":
    app.run(debug=True)