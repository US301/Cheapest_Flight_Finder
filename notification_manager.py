import os
import smtplib
import requests

api_key = os.environ['URL_EMAIL']
authorization = os.environ["AUTH"]
headers = {"Authorization": authorization}

my_email = "saidusam098@gmail.com"
password = "301856Us12!"

class NotificationManager:
    def send_emails(self, message):
        data = requests.get(url=api_key, headers=headers)
        users_data = data.json()
        print(users_data)
        for email in users_data:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email, to_addrs=f"{email['email']}",
                                    msg=f"Subject: New Low Price Flight!\n\n{message}")
                connection.close()
