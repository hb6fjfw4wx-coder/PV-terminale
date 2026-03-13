import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Procese verbale terminale service", page_icon="🎫")
st.title("🎫 Procese verbale terminale service")
st.write(
    """
    Procese verbale pentru scannerele zebra si honeywell, pentru a tine evidenta defectelor si a service-ului.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "terminalul Honeywell nu se conectează la Wi-Fi",
        "terminalul Zebra nu se sincronizează cu serverul",
        "softul terminalului Honeywell nu pornește",
        "scannerul Zebra nu citește codurile de bare 2D",
        "bateria terminalului Honeywell se descarcă prea rapid",
        "scannerul Zebra rămâne blocat după scanare continuă",
        "probleme de conectare Bluetooth între terminalul Honeywell și imprimantă",
        "actualizarea firmware-ului Zebra eșuează",
        "scannerul Honeywell nu mai transmite datele către aplicație",
        "terminalul Zebra nu recunoaște docking station-ul",
        "erori de aplicație la pornirea software-ului Honeywell Mobility",
        "terminalul Zebra nu se autentifică în rețea",
        "scannerul Honeywell nu citește codul de bare complet",
        "probleme la încărcarea terminalului Zebra în cradle",
        "latență mare la transmiterea datelor între terminal Honeywell și server",
        "terminalul Zebra afișează ecran negru după restart",
        "scannerul Honeywell scanează intermitent",
        "probleme cu aplicația de inventar pe terminalul Zebra",
        "terminalul Honeywell pierde conexiunea VPN",
        "sistemul Zebra generează erori de sincronizare fișiere",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Show a section to add a new ticket.
st.header("Deschide PV")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    issue = st.text_area("Describe the issue")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"PV-{recent_ticket_number+1}",
                "Descriere": issue,
                "Status": "Open",
                "Prioritate": priority,
                "Data trimitere service": today,
            }
        ]
    )

    # Show a little success message.
    st.write("Procesul verbal a fost generat, acestea sunt detaliile:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Show section to view and edit existing tickets in a table.
st.header("Procese verbale existente")
st.write(f"Total PV: `{len(st.session_state.df)}`")

st.info(
    "Se pot edita PV-urile prin dublu click pe linie"
    "Se pot sorta coloanele si exporta fisierul ca csv",
    icon="✍️",
)

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Prioritate": st.column_config.SelectboxColumn(
            "Prioritate",
            help="Prioritate",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Disable editing the ID and Date Submitted columns.
    disabled=["ID", "Data trimitere service"],
)

# Show some metrics and charts about the ticket.
st.header("Statistics")

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
