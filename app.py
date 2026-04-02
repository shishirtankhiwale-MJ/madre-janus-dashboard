import streamlit as st
import pandas as pd

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="Madre Janus", layout="wide")

# ----------- LOAD DATA -----------
df = pd.read_csv("activity_data.csv")

# ----------- HEADER -----------
st.markdown("""
    <h1 style='color:#4A90E2;'>🛡️ Madre Janus</h1>
    <p style='color:gray;'>Workforce Intelligence Platform</p>
""", unsafe_allow_html=True)

st.divider()

# ----------- SIDEBAR -----------
st.sidebar.title("🔍 Filters")
employee = st.sidebar.selectbox("Select Employee", df["employee"].unique())

filtered_df = df[df["employee"] == employee]

# ----------- KPI SECTION -----------
total_hours = filtered_df["hours"].sum()
productive_hours = filtered_df[filtered_df["category"] == "Productive"]["hours"].sum()
non_productive_hours = filtered_df[filtered_df["category"] == "Non-Productive"]["hours"].sum()

productivity_score = (productive_hours / total_hours) * 100

st.subheader(f"📊 {employee} Performance Overview")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div style='background-color:#E3F2FD;padding:20px;border-radius:10px'>
<h3>Total Hours</h3>
<h2>{total_hours} hrs</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='background-color:#E8F5E9;padding:20px;border-radius:10px'>
<h3>Productive Hours</h3>
<h2>{productive_hours} hrs</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style='background-color:#FFF3E0;padding:20px;border-radius:10px'>
<h3>Productivity Score</h3>
<h2>{productivity_score:.1f}%</h2>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----------- CHARTS -----------
col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Application Usage")
    app_usage = filtered_df.groupby("application")["hours"].sum()
    st.bar_chart(app_usage)

with col5:
    st.subheader("👥 Client Work")
    client_data = filtered_df.groupby("client")["hours"].sum()
    st.bar_chart(client_data)

# ----------- PRODUCTIVITY SPLIT -----------
st.subheader("⚖️ Productivity Split")
category_data = filtered_df.groupby("category")["hours"].sum()
st.bar_chart(category_data)

# ----------- INSIGHTS -----------
st.subheader("📌 Key Insights")

if productivity_score > 80:
    st.success("High productivity observed")
elif productivity_score > 60:
    st.info("Moderate productivity - scope for improvement")
else:
    st.error("Low productivity - attention required")

if non_productive_hours > 1:
    st.warning("High non-productive usage detected")

# ----------- TEAM SUMMARY -----------
st.divider()
st.title("👥 Team Overview")

team_data = df.groupby("employee").apply(
    lambda x: pd.Series({
        "total_hours": x["hours"].sum(),
        "productive_hours": x[x["category"] == "Productive"]["hours"].sum()
    })
).reset_index()

team_data["productivity_score"] = (
    team_data["productive_hours"] / team_data["total_hours"]
) * 100

# ----------- RANKING -----------
team_data = team_data.sort_values(by="productivity_score", ascending=False)
team_data["rank"] = range(1, len(team_data) + 1)

# ----------- BADGE SYSTEM -----------
def get_badge(score):
    if score >= 80:
        return "🔥 High Performer"
    elif score >= 60:
        return "👍 Consistent Performer"
    elif score >= 40:
        return "⚠️ Needs Improvement"
    else:
        return "🚨 At Risk"

team_data["badge"] = team_data["productivity_score"].apply(get_badge)

# ----------- LEADERBOARD UI -----------
st.subheader("🏅 Team Leaderboard")

# Top Performer
top = team_data.iloc[0]

st.markdown(f"""
<div style='background: linear-gradient(90deg, #4CAF50, #81C784);
            padding:20px;
            border-radius:15px;
            margin-bottom:20px;
            color:white;'>
    <h2>🥇 {top['employee']}</h2>
    <h3>Productivity: {top['productivity_score']:.1f}%</h3>
    <p>{top['badge']}</p>
</div>
""", unsafe_allow_html=True)

# Other Employees
for i in range(1, len(team_data)):
    row = team_data.iloc[i]

    color = "#E3F2FD"
    if row["rank"] == 2:
        color = "#BBDEFB"
    elif row["rank"] == 3:
        color = "#E1F5FE"

    st.markdown(f"""
    <div style='background-color:{color};
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;'>
        <strong>Rank {int(row['rank'])} - {row['employee']}</strong><br>
        Productivity: {row['productivity_score']:.1f}%<br>
        {row['badge']}
    </div>
    """, unsafe_allow_html=True)

# ----------- PERFORMANCE ALERTS -----------
low_employee = team_data.iloc[-1]

st.divider()

col6, col7 = st.columns(2)

col6.success(
    f"🏆 Top Performer: {top['employee']} ({top['productivity_score']:.1f}%)"
)

col7.error(
    f"⚠️ Needs Attention: {low_employee['employee']} ({low_employee['productivity_score']:.1f}%)"
)

# ----------- DAILY PRODUCTIVITY SCORECARD -----------

st.divider()
st.title("📊 Daily Productivity Scorecard")

scorecard = df.groupby("employee").apply(
    lambda x: pd.Series({
        "total_hours": x["hours"].sum(),
        "productive_hours": x[x["category"] == "Productive"]["hours"].sum()
    })
).reset_index()

scorecard["score"] = (
    scorecard["productive_hours"] / scorecard["total_hours"]
) * 100

def get_status(score):
    if score >= 80:
        return "🔥 High Performer"
    elif score >= 60:
        return "👍 Average"
    elif score >= 40:
        return "⚠️ Low"
    else:
        return "🚨 Critical"

scorecard["status"] = scorecard["score"].apply(get_status)
scorecard["score"] = scorecard["score"].round(1)

# Display Scorecard
st.dataframe(scorecard)

# Highlights
top_emp = scorecard.sort_values(by="score", ascending=False).iloc[0]
low_emp = scorecard.sort_values(by="score", ascending=True).iloc[0]

col8, col9 = st.columns(2)

col8.success(
    f"🏆 Best Performer Today: {top_emp['employee']} ({top_emp['score']}%)"
)

col9.error(
    f"⚠️ Needs Attention: {low_emp['employee']} ({low_emp['score']}%)"
)
# ----------- ADD TASK FORM -----------

st.divider()
st.subheader("➕ Add Compliance Task")

with st.form("task_form"):
    employee_input = st.selectbox("Select Employee", df["employee"].unique())
    task_input = st.text_input("Task (e.g. GST Filing)")
    client_input = st.text_input("Client Name")
    deadline_input = st.date_input("Deadline")
    status_input = st.selectbox("Status", ["Pending", "Completed"])

    submit = st.form_submit_button("Add Task")

    if submit:
        new_data = pd.DataFrame([{
            "employee": employee_input,
            "task": task_input,
            "client": client_input,
            "deadline": deadline_input,
            "status": status_input
        }])

        new_data.to_csv("compliance_data.csv", mode='a', header=False, index=False)

        st.success("✅ Task Added Successfully!")
# ----------- COMPLIANCE TRACKER -----------

import datetime

st.divider()
st.title("📅 Compliance Tracker")

comp_df = pd.read_csv("compliance_data.csv")

# Convert date
comp_df["deadline"] = pd.to_datetime(comp_df["deadline"])
today = pd.to_datetime(datetime.date.today())

# Status classification
pending = comp_df[comp_df["status"] == "Pending"]
completed = comp_df[comp_df["status"] == "Completed"]
overdue = pending[pending["deadline"] < today]

# ----------- SUMMARY CARDS -----------

col1, col2, col3 = st.columns(3)

col1.metric("📌 Pending Tasks", len(pending))
col2.metric("✅ Completed Tasks", len(completed))
col3.metric("🚨 Overdue Tasks", len(overdue))
# ----------- COMPLIANCE ALERT SYSTEM -----------

st.subheader("🚨 Compliance Alerts")

# Due in next 2 days
due_soon = pending[
    (pending["deadline"] >= today) &
    (pending["deadline"] <= today + pd.Timedelta(days=2))
]

# ----------- ALERT DISPLAY -----------

if len(overdue) > 0:
    st.error(f"🚨 {len(overdue)} Overdue Tasks! Immediate action required")

if len(due_soon) > 0:
    st.warning(f"⏳ {len(due_soon)} Tasks due in next 2 days")

if len(overdue) == 0 and len(due_soon) == 0:
    st.success("✅ All compliance tasks are under control")

# ----------- OVERDUE -----------

st.subheader("🚨 Overdue Tasks")

if len(overdue) > 0:
    st.dataframe(overdue)
else:
    st.success("No overdue tasks")

# ----------- UPCOMING -----------

st.subheader("⏳ Upcoming Tasks")

upcoming = pending[pending["deadline"] >= today]

st.dataframe(upcoming)

# ----------- ALL TASKS -----------

st.subheader("📋 All Compliance Tasks")

st.dataframe(comp_df)
