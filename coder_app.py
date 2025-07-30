import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import json
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

st.set_page_config(page_title="S2M Coder Portal", layout="wide")

# ---------------------------
# 🔐 Load credentials from secrets
# ---------------------------
def load_credentials_from_base64():
    b64_creds = st.secrets["gcp"]["base64_key"]
    creds_dict = json.loads(base64.b64decode(b64_creds).decode("utf-8"))
    return creds_dict

# ✅ Optional: Test connection
def test_google_auth():
    try:
        creds_dict = load_credentials_from_base64()
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        creds.refresh(Request())
        st.success("✅ Google credentials and token are valid!")
    except Exception as e:
        st.error(f"❌ Token refresh failed: {e}")

test_google_auth()

# ---------------------------
# 📊 Google Sheet Connection
# ---------------------------
def connect_sheet(sheet_name):
    creds_info = load_credentials_from_base64()
    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

# ---------------------------
# 📤 Submit to Sheet
# ---------------------------
def submit_coder_data(data):
    sheet = connect_sheet("S2M_Production_Data")
    sheet.append_row(data)

# ---------------------------
# 🖥️ UI - Form Input
# ---------------------------
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
        st.success("✅ Data submitted to Google Sheet successfully!")
