import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ---------------------------------
# Email Credentials
# ---------------------------------
from_addr = "bhaktihaval@gmail.com"
password = "mxshtygdrxtwzawq"

# ---------------------------------
# Read CSV File
# ---------------------------------
data = pd.read_csv("H:/Devops/Daily Report Generator & Auto Sender.csv")

names = data["names"].to_list()
task_completed = data["task_completed"].to_list()

# ---------------------------------
# Calculation
# ---------------------------------
total_entries = len(names)

average_tasks = sum(task_completed) / len(task_completed)

max_tasks = max(task_completed)
top_index = task_completed.index(max_tasks)
top_performer = names[top_index]

# ---------------------------------
# Create Report File
# ---------------------------------
report_text = f"""
Daily Report

Total Entries: {total_entries}
Average Tasks Completed: {average_tasks:.2f}
Top Performer: {top_performer} ({max_tasks} tasks)
"""

report_path = "H:/Devops/daily_report.txt"

with open(report_path, "w") as file:
    file.write(report_text)

# ---------------------------------
# Connect to Gmail
# ---------------------------------
mail = smtplib.SMTP("smtp.gmail.com", 587)
mail.ehlo()
mail.starttls()
mail.login(from_addr, password)

# ---------------------------------
# Create Email
# ---------------------------------
to_email = "shreyaskaradkar003@gmail.com"

msg = MIMEMultipart()
msg["From"] = from_addr
msg["To"] = to_email
msg["Subject"] = "Daily Task Report"

body = "Hi,\n\nPlease find attached the daily report.\n\nRegards,\nBhakti"
msg.attach(MIMEText(body, "plain"))

# ---------------------------------
# Attach Report File
# ---------------------------------
with open(report_path, "rb") as file:
    part = MIMEApplication(file.read(), Name="daily_report.txt")
    part['Content-Disposition'] = 'attachment; filename="daily_report.txt"'
    msg.attach(part)

# ---------------------------------
# Send Email
# ---------------------------------
mail.sendmail(from_addr, to_email, msg.as_string())
mail.quit()

print("Report generated and email sent successfully!")
