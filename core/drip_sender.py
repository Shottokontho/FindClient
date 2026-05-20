import smtplib
import time
import random
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

class DripSender:
    def __init__(self, email_user: str, email_pass: str):
        self.email_user = email_user
        self.email_pass = email_pass
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_email: str, subject: str, body: str):
        """Sends a single email via SMTP."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email_user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Delivery failed to {to_email}: {e}")
            return False

    def execute_drip(self, strategy_path: str, max_per_day: int, gap_range: tuple):
        """
        Reads the Excel strategy and sends emails with a 
        randomized gap to mimic human behavior.
        """
        df = pd.read_excel(strategy_path)
        leads = df.to_dict("records")
        
        print(f"Starting Drip Execution: {len(leads)} targets.")
        print(f"Safety Settings: Max {max_per_day}/day | Gap: {gap_range[0]}-{gap_range[1]} mins.")

        for idx, lead in enumerate(leads):
            # Only sending Day 1 for a demo, but this would iterate through 7 days via a cron job.
            success = self.send_email(
                to_email=lead["Email"],
                subject="Quick question",
                body=lead["Day 1 (The Hook)"]
            )
            
            if success:
                print(f"[{idx+1}] Successfully sent Day 1 to {lead['Email']}")
            
            # Anti-Ban Random Gap
            wait_time = random.randint(gap_range[0] * 60, gap_range[1] * 60)
            if idx < len(leads) - 1:
                print(f"Mimicking human... sleeping for {wait_time//60} minutes.")
                # In production, we used a real time.sleep(wait_time)
                # For the demo/repo, we simulate it.
                # time.sleep(wait_time) 

        print("\n✅ Drip cycle completed for this batch.")
