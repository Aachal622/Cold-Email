# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 11:00:25 2025

@author: aachalkala
"""

import pandas as pd
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

# === Setup ===
your_email = "@gmail.com"
app_password = ""  # Use App Password

log_file = "email_log.txt"
log_path = os.path.join(os.getcwd(), log_file)

# === Prepare Logging Function ===
def log_result(email, status, message=""):
    with open(log_path, "a") as log:
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{time_stamp} | {email} | {status} | {message}\n")

# === Load HR Emails ===
try:
    hr_df = pd.read_csv(r"C:\Users\Lenovo\OneDrive\Self Document\Cold Email\hr_emails.csv")
except Exception as e:
    print("Error loading CSV:", e)
    exit()

# === Prepare Email Content ===
subject = "🚀 Data Scientist | GenAI + LLM Expert | Available by July 18"

html = """
<html>
  <body>
    <p>Dear <b>Hiring Manager</b>,</p>
    <p>
    I’m <b>Aachal Kala</b>, a passionate Data Scientist with <b>3+ years</b> of experience delivering
    real-world AI solutions across healthcare, education, and non-profit domains. My core expertise
    lies in <b>Generative AI, LLM-driven applications, and Retrieval-Augmented Generation (RAG)</b>
    using tools like LangChain, GPT-4, and Azure OpenAI.
    </p>
    <p>
    I’m currently <b>serving my notice period</b>, with my <b>last working day on 18 July 2025</b>,
    and actively seeking opportunities where I can bring immediate impact. I'm also confident working with Python, SQL, and cloud
    technologies like Azure and AWS.
    </p>
    <p>
    I’ve attached my resume for your consideration and would welcome a chance to connect.
    Thank you for your time—I look forward to contributing to your team’s success.
    </p>
    <p>
      Warm regards,<br>
      <b>Aachal Kala</b><br>
      📧 aachalkala2001@gmail.com | 📱 +91 Phone no<br>
      🔗 <a href="https://linkedin.com/in/aachal-kala-1050a31a6/">LinkedIn</a> |
      🖥️ <a href="https://github.com/Aachal622">GitHub</a>
    </p>
  </body>
</html>
"""

# === Load Resume ===
try:
    with open(r"C:\Users\Lenovo\OneDrive\Self Document\Cold Email\Aachal Kala DS V2.pdf", "rb") as f:
        resume_data = f.read()
except Exception as e:
    print("Error loading resume:", e)
    exit()

# === Send Email Loop ===
for index, row in hr_df.iterrows():
    email = row.get("email", "").strip()
    if not email or '@' not in email:
        print(f"Skipping invalid email at index {index}")
        log_result(email or "MISSING", "FAILED", "Invalid or missing email")
        continue

    msg = MIMEMultipart()
    msg['From'] = your_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, "html"))

    part = MIMEApplication(resume_data, Name="Aachal_Kala_Resume.pdf")
    part['Content-Disposition'] = 'attachment; filename="Aachal_Kala_Resume.pdf"'
    msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(your_email, app_password)
            server.sendmail(your_email, email, msg.as_string())
        print(f"✅ Email sent to {email}")
        log_result(email, "SUCCESS")
    except Exception as e:
        print(f"❌ Failed to send to {email}: {e}")
        log_result(email, "FAILED", str(e))
