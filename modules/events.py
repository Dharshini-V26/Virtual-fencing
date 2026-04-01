import time
import smtplib
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class EventManager:
    def __init__(self):
        self.last_alert_time = 0

        # -----------------------------
        # EMAIL CONFIGURATION
        # -----------------------------
        self.sender_email = "revadharshini25@gmail.com"
        self.receiver_email = "revadharshini25@gmail.com"
        self.app_password = "pluo inhh gdvt chbt"  # 🔴 replace this

        self.cooldown = 10  # seconds

    def send_email_alert(self, frame):
        try:
            # -----------------------------
            # SAVE IMAGE SNAPSHOT
            # -----------------------------
            image_path = "alert.jpg"
            cv2.imwrite(image_path, frame)

            # -----------------------------
            # CREATE EMAIL
            # -----------------------------
            msg = MIMEMultipart()
            msg["Subject"] = "🚨 ALERT: Intrusion Detected"
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email

            # Email body
            body = "A person has entered the restricted virtual fencing area.\n\nSee attached image."
            msg.attach(MIMEText(body, "plain"))

            # -----------------------------
            # ATTACH IMAGE
            # -----------------------------
            with open(image_path, "rb") as f:
                img_data = f.read()
                image = MIMEImage(img_data, name="intrusion.jpg")
                msg.attach(image)

            # -----------------------------
            # SEND EMAIL
            # -----------------------------
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
            server.quit()

            print("📧 Email with image sent!")

        except Exception as e:
            print("Email Error:", e)

    def create_event(self, status, frame):
        return {
            "status": status,
            "timestamp": time.time(),
            "frame": frame
        }

    def handle_event(self, event):
        if event["status"] == "UNSAFE":
            current_time = time.time()

            # -----------------------------
            # SPAM CONTROL (COOLDOWN)
            # -----------------------------
            if current_time - self.last_alert_time > self.cooldown:
                print("🚨 ALERT: Intrusion detected!")

                # SEND EMAIL WITH IMAGE
                self.send_email_alert(event["frame"])

                self.last_alert_time = current_time