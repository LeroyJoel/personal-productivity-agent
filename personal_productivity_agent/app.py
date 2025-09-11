# app.py
import sys, os
from dotenv import load_dotenv
# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)  # Go up one level to src
project_root = os.path.dirname(src_dir)  # Go up another level to project root

sys.path.insert(0, src_dir)
sys.path.insert(0, os.path.join(src_dir, 'personal_productivity_agent'))

# Load environment variables from .env file
load_dotenv()

import streamlit as st
import pandas as pd
from main import run_with_inputs
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Personal Productivity Agent Crew", layout="wide")
st.title("🧑‍💻 Personal Productivity Agent Crew")

# --- Input Sections ---
st.header("📋 Task Manager")
tasks = st.text_area("Enter your tasks (one per line):", 
                     placeholder="e.g., Finish data report\nPrepare slides for meeting\nBuy groceries")
priority = st.radio("Set priority for new tasks:", ["High", "Medium", "Low"])

st.header("📧 Email Assistant")
emails = st.text_area("Paste your unread emails or email threads:", 
                      placeholder="e.g., Dear Joel, we would like to schedule a meeting...")

st.header("📅 Calendar Scheduler")
events = st.text_area("Enter upcoming events (one per line):", 
                      placeholder="e.g., Team meeting - Monday 3 PM\nDoctor appointment - Tuesday 9 AM")

report_type = st.selectbox("Generate a report for:", ["Daily", "Weekly"])

# --- Run Crew ---
if st.button("🚀 Generate Productivity Report"):
    with st.spinner("Running Productivity Crew..."):

        # Prepare inputs for Crew
        inputs = {
            "tasks": tasks.split("\n") if tasks else [],
            "priority": priority,
            "emails": emails,
            "events": events.split("\n") if events else [],
            "report_type": report_type
        }

        # Run the Crew
        insights = run_with_inputs(inputs)
        st.markdown(insights)

    st.success("✅ Productivity Report Ready")

    # --- Display Report ---
    if isinstance(insights, str):
        st.markdown(insights, unsafe_allow_html=True)
        insights_text = insights
    else:
        st.write(insights)
        insights_text = str(insights)

    # --- Download as Markdown ---
    st.download_button(
        label="⬇️ Download Report (Markdown)",
        data=insights_text,
        file_name="productivity_report.md",
        mime="text/markdown"
    )

    # --- Download as PDF ---
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    for line in insights_text.split("\n"):
        if line.strip():
            if line.startswith("## "):  # headings
                story.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))
            elif line.startswith("- "):  # bullet points
                story.append(Paragraph(line, styles["Normal"]))
            else:
                story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download Report (PDF)",
        data=buffer,
        file_name="productivity_report.pdf",
        mime="application/pdf"
    )
