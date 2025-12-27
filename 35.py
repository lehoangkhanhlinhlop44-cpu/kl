import smtplib
import mysql.connector
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os
import json

# -------------------------------------------------------
# 1. Load environment variables
# -------------------------------------------------------
load_dotenv()

SENDER_EMAIL = os.getenv("FROM_EMAIL")
SENDER_PASSWORD = os.getenv("APP_PASSWORD")
SUBJECT = os.getenv("SUBJECT", "THƯ THÔNG BÁO HOÀN TIỀN")

# -------------------------------------------------------
# 2. Connect MySQL
# -------------------------------------------------------
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USERNAME"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="test",
        charset="utf8mb4",
        use_unicode=True
    )
    cursor = mydb.cursor()
    print("🔗 Kết nối MySQL thành công.")

except Exception as e:
    print("❌ Lỗi kết nối MySQL:", e)
    exit()

# -------------------------------------------------------
# 3. Load HTML template from MySQL
# -------------------------------------------------------
try:
    cursor.execute("SELECT html_content FROM email_templates WHERE id = 3")
    result = cursor.fetchone()

    if not result:
        print("❌ Không tìm thấy template với id = 3")
        exit()

    template_str = result[0]
    template = Template(template_str)
    print("📄 Template đã tải từ MySQL.")

except Exception as e:
    print("❌ Lỗi tải template:", e)
    exit()


# -------------------------------------------------------
# 4. Load recipients JSON file
# -------------------------------------------------------
def load_recipients_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Lỗi đọc file JSON:", e)
        return []

recipients_data = load_recipients_data("SS5/mail_get.json")

if not recipients_data:
    print("❌ Không có dữ liệu người nhận trong file JSON.")
    exit()


# -------------------------------------------------------
# 5. Loop & Send Emails
# -------------------------------------------------------
for user in recipients_data:

    # Render HTML with each user data
    email_html = template.render(**user)

    # Get email
    recipient_email = user.get("email")
    if not recipient_email:
        print("⚠️ Bỏ qua một user vì thiếu email.")
        continue

    # Create MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    msg.attach(MIMEText(email_html, "html", "utf-8"))

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)