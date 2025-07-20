import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="School Dashboard", layout="wide")
st.title("📊 School Student Dashboard")

# Upload the student data file
uploaded_file = st.file_uploader("Upload Monthly Student Data (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Basic metrics
    total_students = len(df)
    total_fees_collected = df['Fees Paid'].sum()
    total_fees_due = df['Total Fees'].sum() - total_fees_collected
    avg_attendance = df['Attendance (%)'].mean()

    st.subheader("📌 Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Fees Collected", f"₹{total_fees_collected}")
    col3.metric("Fees Due", f"₹{total_fees_due}")
    col4.metric("Avg. Attendance", f"{avg_attendance:.1f}%")

    # Class Filter
    selected_class = st.selectbox("Select Class", options=sorted(df['Class'].unique()))
    class_df = df[df['Class'] == selected_class]

    st.subheader(f"👩‍🏫 Students in {selected_class}")
    st.dataframe(class_df, use_container_width=True)

    # Charts
    st.subheader("📈 Fee Payment Overview")
    fig1, ax1 = plt.subplots()
    fee_paid_count = sum(class_df['Fees Paid'] >= class_df['Total Fees'])
    fee_due_count = len(class_df) - fee_paid_count
    ax1.pie([fee_paid_count, fee_due_count], labels=["Paid", "Unpaid"], autopct='%1.1f%%', colors=['green', 'red'])
    st.pyplot(fig1)

    st.subheader("📊 Attendance Chart")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(class_df['Name'], class_df['Attendance (%)'], color='skyblue')
    ax2.set_xticklabels(class_df['Name'], rotation=45)
    ax2.set_ylabel("Attendance %")
    st.pyplot(fig2)

    # Low attendance filter
    st.subheader("⚠️ Students with < 75% Attendance")
    low_attendance_df = class_df[class_df['Attendance (%)'] < 75]
    if not low_attendance_df.empty:
        st.dataframe(low_attendance_df)
    else:
        st.info("All students have good attendance this month!")

else:
    st.warning("📤 Please upload a student data file to view the dashboard.")
