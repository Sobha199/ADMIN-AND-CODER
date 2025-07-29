
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="S2M Admin Dashboard", layout="wide")

# Function to connect to Google Sheet
def connect_sheet(sheet_name):
    scope = ["S2M_Production_Data"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def fetch_admin_data():
    sheet = connect_sheet("S2M_Production_Data")
    data = sheet.get_all_records()
    return pd.DataFrame(data)

st.title("Admin Dashboard - S2M")

df = fetch_admin_data()

if not df.empty:
    st.metric("Total Charts", df["No of Charts"].sum())
    st.metric("Total ICD", df["ICD Count"].sum())
    st.metric("Total DOS", df["DOS Count"].sum())
    st.metric("Average CPH", round(df["CPH"].astype(float).mean(), 2))
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "production_data.csv", "text/csv")
else:
    st.info("No data found.")
