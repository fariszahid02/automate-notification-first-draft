# automation_email.py
import os
from pathlib import Path
import win32com.client


def send_email(subject: str, recipient: str, body_text: str, cc: str | None = None, attachments: list[str] | None = None):

    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)  # 0 = olMailItem

    mail.Subject = subject
    mail.To = recipient
    if cc:
        mail.CC = cc

    # Plain text body (switch to HTMLBody if you want HTML formatting)
    mail.Body = body_text

    # Attach files if provided
    if attachments:
        for path in attachments:
            if os.path.exists(path):
                mail.Attachments.Add(Source=path)

    # Send immediately via default Outlook profile
    mail.Send()


def main():
    # Adjust recipients as needed
    recipient = "faris.zaimir@bnm.gov.my"
    cc = "faris@bnm.gov.my"  # e.g., "rifqah@bnm.gov.my"

    subject = "Automation Status"
    body = (
        "Hi Team,\n\n"
        "All processes executed successfully ✅\n\n"
        "Regards,\nAutomation Bot"
    )

    try:
        send_email(subject=subject, recipient=recipient, body_text=body, cc=cc)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    main()