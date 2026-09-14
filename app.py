import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Ola Analytics", layout="wide")
st.title("🚖 Ola Ride Analytics Dashboard")

conn = sqlite3.connect('ola_rides.db')
df = pd.read_sql_query("SELECT * FROM rides", conn)
conn.close()

col1, col2, col3, col4 = st.columns(4)
total_rides = len(df)
cancelled = len(df[df['Booking_Status'].str.contains('Canceled', case=False, na=False)])
cancel_rate = (cancelled / total_rides) * 100

with col1:
    st.metric("Total Bookings", f"{total_rides:,}")
with col2:
    st.metric("Cancellations", f"{cancelled:,}")
with col3:
    st.metric("Cancel Rate", f"{cancel_rate:.1f}%")
with col4:
    st.metric("Avg V_TAT (sec)", f"{df['V_TAT'].mean():.0f}")

st.subheader("📍 Top Pickup Locations")
pickup_df = df['Pickup_Location'].value_counts().head(10).reset_index()
pickup_df.columns = ['Location', 'Count']
fig1 = px.bar(pickup_df, x='Count', y='Location', orientation='h', color='Count')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🚗 Bookings by Vehicle Type")
vehicle_df = df['Vehicle_Type'].value_counts().reset_index()
vehicle_df.columns = ['Vehicle', 'Count']
fig2 = px.pie(vehicle_df, values='Count', names='Vehicle', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("❌ Cancellation Reasons (Top 5)")
cancel_reasons = df['Canceled_Rides_by_Customer'].value_counts().head(5).reset_index()
cancel_reasons.columns = ['Reason', 'Count']
fig3 = px.bar(cancel_reasons, x='Reason', y='Count', color='Count')
st.plotly_chart(fig3, use_container_width=True)