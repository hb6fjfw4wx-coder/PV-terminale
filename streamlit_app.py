# app_flask.py
from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF  # pip install fpdf2
import datetime
from io import BytesIO

app = Flask(__name__)

# ---- PDF function (same as above; keep only one copy in real code) ----
def create_proces_verbal_pdf(
    pv_number: str,
    person_name: str,
    device_type: str,
    serial_number: str,
    issue_description: str,
    priority: str,
    date_submitted: str,
    location: str = "București",
) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PROCES VERBAL", ln=1, align="C")
    pdf.cell(0, 8, "Predare echipament pentru service", ln=1, align="C")
    pdf.ln(8)
    # (same body as in Streamlit example...)
    # ...
    return pdf.output(dest="S").encode("latin1")


# ---- Simple HTML form template ----
FORM_HTML = """
<!doctype html>
<html lang="ro">
  <head>
    <meta charset="utf-8">
    <title>Procese verbale terminale service</title>
  </head>
  <body>
    <h1>Procese verbale terminale service</h1>
    <form action="/generate" method="post">
      <label>Nume persoană:</label><br>
      <input type="text" name="person_name" required><br><br>

      <label>Tip echipament:</label><br>
      <select name="device_type">
        <option value="Zebra">Zebra</option>
        <option value="Honeywell">Honeywell</option>
      </select><br><br>

      <label>Număr serial:</label><br>
      <input type="text" name="serial_number" required><br><br>

      <label>Locație:</label><br>
      <input type="text" name="location" value="București"><br><br>

      <label>Prioritate:</label><br>
      <select name="priority">
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select><br><br>

      <label>Descriere problemă:</label><br>
      <textarea name="issue" rows="4" cols="50"></textarea><br><br>

      <button type="submit">Generează PV (PDF)</button>
    </form>
  </body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(FORM_HTML)


@app.route("/generate", methods=["POST"])
def generate():
    person_name = request.form.get("person_name")
    device_type = request.form.get("device_type")
    serial_number = request.form.get("serial_number")
    location = request.form.get("location", "București")
    priority = request.form.get("priority", "Medium")
    issue = request.form.get("issue", "")

    today = datetime.datetime.now().strftime("%d-%m-%Y")
    pv_number = "PV-1"  # sau generezi din DB

    pdf_bytes = create_proces_verbal_pdf(
        pv_number=pv_number,
        person_name=person_name,
        device_type=device_type,
        serial_number=serial_number,
        issue_description=issue,
        priority=priority,
        date_submitted=today,
        location=location,
    )

    file_name = f"{pv_number}_{device_type}_{serial_number}_{today}.pdf"

    return send_file(
        BytesIO(pdf_bytes),
        as_attachment=True,
        download_name=file_name,
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True)
import streamlit as st

# All your logic that was inside Flask routes can be turned into
# normal Python functions and called directly from Streamlit.

def main():
    st.title("My App")

    # Example: instead of a Flask route that returns text,
    # just write it in Streamlit:
    st.write("Hello from Streamlit")

    # Put the rest of your UI here:
    # st.text_input(...), st.button(...), etc.

if __name__ == "__main__":
    main()
