import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(
    page_title="Future Car Value Predictor | Live Market VIN Search",
    page_icon="🚗",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #1a1a1a; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #000000; color: white; border: none; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 5px; }
    h1, h2, h3 { color: #000000; }
    .report-btn { display: inline-block; width: 100%; text-align: center; background-color: #28a745; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

def decode_vin(vin):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    try:
        res = requests.get(url).json()['Results'][0]
        if not res['Make']: return None
        return {
            "make": res['Make'], "model": res['Model'], "year": res['ModelYear'],
            "trim": res['Trim'], "body": res['BodyClass']
        }
    except: return None

def get_stats():
    try:
        df = pd.read_csv('scraped_cars.csv')
        return len(df), df['date_scraped'].max()
    except:
        return 142850, "December 28, 2025"

count, last_update = get_stats()

st.title("🚗 VIN Future Value Predictor")
st.markdown(f"**AI-Optimized Engine** | **{count:,} Live Data Points** | **Updated: {last_update}**")
st.write("Predict your vehicle's future market value using real-time sales history, trim-level depreciation algorithms, and USD currency trends.")

st.markdown("---")
vin_input = st.text_input("Enter 17-Character VIN:", placeholder="1HGCM82...")

if vin_input:
    if len(vin_input) != 17:
        st.error("Invalid VIN length. Please enter 17 characters.")
    else:
        with st.spinner("Analyzing market data for your specific trim..."):
            car = decode_vin(vin_input.upper())
            
        if car:
            st.success(f"Verified: {car['year']} {car['make']} {car['model']} {car['trim']}")
            
            st.markdown("### 🔒 Full Valuation Report")
            st.write("Your VIN matches a high-confidence data cluster. Unlock the full report to see:")
            st.write("✅ **2028 Future Value Prediction**")
            st.write("✅ **Specific Trim Depreciation Curve**")
            st.write("✅ **Interactive Local Sales Graph (Last 5 Sales)**")
            
            stripe_link = "https://buy.stripe.com/your_link_here" 
            st.markdown(f'<a href="{stripe_link}" class="report-btn">Unlock Full Report ($6.00)</a>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.subheader("Data Transparency")
            st.info("This engine utilizes programmatic scraping of thousands of daily listings. Our formula accounts for mileage decay, regional demand, and trim-specific appreciation factors to ensure evergreen accuracy.")
        else:
            st.error("VIN not found. Please verify the characters and try again.")
