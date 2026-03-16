# streamlit_app.py
import streamlit as st
from fpdf import FPDF  # pip install fpdf2
import datetime
from io import BytesIO

# ---- PDF function (same as before) ----
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
    # aici pui restul conținutului PDF, exact ca în varianta ta Flask
    # ...
    return pdf.output(dest="S").encode("latin1")


def main():
    st.title("Procese verbale terminale service")

    with st.form("pv_form"):
        person_name = st.text_input("Nume persoană", "")
        device_type = st.selectbox("Tip echipament", ["Zebra", "Honeywell"])
        serial_number = st.text_input("Număr serial", "")
        location = st.text_input("Locație", "București")
        priority = st.selectbox("Prioritate", ["High", "Medium", "Low"])
        issue = st.text_area("Descriere problemă", "")

        submitted = st.form_submit_button("Generează PV (PDF)")

    if submitted:
        if not person_name or not serial_number:
            st.error("Te rog completează numele persoanei și numărul de serie.")
            return

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

        st.success("PDF generat cu succes!")
        st.download_button(
            label="Descarcă PDF",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
