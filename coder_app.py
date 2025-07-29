
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="S2M Coder Portal", layout="wide")

# Function to connect to Google Sheet
def connect_sheet(sheet_name):
    scope = ["https://docs.google.com/spreadsheets/d/1RreF554P5oITseYX4tGRWLgN_gnop3HmNupkkF2lIrY/edit?usp=sharing"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def submit_coder_data(data):
    sheet = connect_sheet("S2M_Production_Data")
    sheet.append_row(data)

st.title("Coder Portal - S2M")
with st.form("coder_form"):
    date = st.date_input("Date", datetime.today())
    emp_id = st.text_input("Employee ID")
    emp_name = st.text_input("Employee Name")
    charts = st.number_input("No of Charts", min_value=0)
    icd = st.number_input("ICD Count", min_value=0)
    dos = st.number_input("DOS Count", min_value=0)
    cph = st.number_input("CPH", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("Submit")
    if submitted:
        row = [str(date), emp_id, emp_name, charts, icd, dos, cph]
        submit_coder_data(row)
        st.success("Data submitted to Google Sheet successfully!")
