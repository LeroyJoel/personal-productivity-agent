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
import json
import re

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
        try:
            result = run_with_inputs(inputs)
            
            # Handle different types of CrewAI results
            if hasattr(result, 'raw'):
                # CrewAI TaskOutput object
                insights = result.raw
            elif hasattr(result, 'result'):
                # CrewAI Result object
                insights = result.result
            elif isinstance(result, dict):
                # Dictionary result
                insights = result.get('result', str(result))
            else:
                # Direct string or other result
                insights = str(result)
            
            st.success("✅ Productivity Report Ready")
            
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            insights = None

    # --- Display Report ---
    if insights:
        # Clean up the insights text
        if isinstance(insights, str):
            # Remove JSON formatting artifacts if present
            cleaned_insights = insights.strip()
            
            # If it looks like JSON, try to extract the actual content
            if cleaned_insights.startswith('{') or cleaned_insights.startswith('['):
                try:
                    parsed_json = json.loads(cleaned_insights)
                    if isinstance(parsed_json, dict) and 'content' in parsed_json:
                        cleaned_insights = parsed_json['content']
                    elif isinstance(parsed_json, dict) and 'result' in parsed_json:
                        cleaned_insights = parsed_json['result']
                    else:
                        cleaned_insights = str(parsed_json)
                except json.JSONDecodeError:
                    pass  # Keep original if not valid JSON
            
            # Remove excessive newlines and clean up markdown
            cleaned_insights = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_insights)
            cleaned_insights = cleaned_insights.strip()
            
            # Display the cleaned report
            st.markdown("## 📊 Your Productivity Report")
            st.markdown(cleaned_insights, unsafe_allow_html=False)
            
            insights_text = cleaned_insights
        else:
            st.markdown("## 📊 Your Productivity Report")
            st.write(insights)
            insights_text = str(insights)

        # --- Download Buttons ---
        col1, col2 = st.columns(2)
        
        with col1:
            # --- Download as Markdown ---
            st.download_button(
                label="⬇️ Download Report (Markdown)",
                data=insights_text,
                file_name=f"productivity_report_{report_type.lower()}.md",
                mime="text/markdown"
            )

        with col2:
            # --- Download as PDF ---
            try:
                buffer = BytesIO()
                doc = SimpleDocDocument(buffer)
                styles = getSampleStyleSheet()
                story = []

                # Split text into lines and format for PDF
                lines = insights_text.split("\n")
                for line in lines:
                    line = line.strip()
                    if line:
                        if line.startswith("# "):  # Main headings
                            story.append(Paragraph(f"<b>{line[2:]}</b>", styles["Title"]))
                        elif line.startswith("## "):  # Sub headings
                            story.append(Paragraph(f"<b>{line[3:]}</b>", styles["Heading2"]))
                        elif line.startswith("### "):  # Sub-sub headings
                            story.append(Paragraph(f"<b>{line[4:]}</b>", styles["Heading3"]))
                        elif line.startswith("* ") or line.startswith("- "):  # Bullet points
                            story.append(Paragraph(f"• {line[2:]}", styles["Normal"]))
                        elif line.startswith("**") and line.endswith("**"):  # Bold text
                            story.append(Paragraph(f"<b>{line[2:-2]}</b>", styles["Normal"]))
                        else:
                            story.append(Paragraph(line, styles["Normal"]))
                        story.append(Spacer(1, 6))

                doc.build(story)
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Download Report (PDF)",
                    data=buffer,
                    file_name=f"productivity_report_{report_type.lower()}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF generation failed: {str(e)}")