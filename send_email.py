# send_email.py
import os
from datetime import date
from pathlib import Path
import win32com.client


SENT_MARKER_DIR = Path(__file__).resolve().parent
SENT_MARKER_FILE = SENT_MARKER_DIR / ".email_sent_today"


def send_email(subject: str, recipient: str, body_text: str, cc: str | None = None, attachments: list[str] | None = None):
    """
    Send an email using Outlook via COM (win32com).
    - subject: Email subject
    - recipient: Semicolon-separated recipients (e.g., "a@x.com;b@y.com")
    - body_text: Plain text body
    - cc: Optional semicolon-separated CC list
    - attachments: Optional list of file paths
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)  # 0 = olMailItem

    mail.Subject = subject
    mail.To = recipient
    if cc:
        mail.CC = cc

    # Plain text body (you can switch to HTMLBody if you want formatting)
    mail.Body = body_text

    # Attach files if provided
    if attachments:
        for path in attachments:
            if os.path.exists(path):
                mail.Attachments.Add(Source=path)

    # Send immediately via default Outlook profile
    mail.Send()


# def already_sent_today() -> bool:
#     """
#     Return True if we've already sent today (based on a small marker file).
#     """
#     if not SENT_MARKER_FILE.exists():
#         return False
#     try:
#         content = SENT_MARKER_FILE.read_text(encoding="utf-8").strip()
#         return content == str(date.today())
#     except Exception:
#         return False


# def update_sent_marker() -> None:
#     """
#     Update the marker file to today's date.
#     """
#     SENT_MARKER_FILE.write_text(str(date.today()), encoding="utf-8")


# if __name__ == "__main__":
#     # Example usage
#     subject = "Cash BOP QC Refresh Completed Successfully"
#     recipient = "faris.zaimir.@bnm.gov.my"  # change if needed
#     cc_list = None  # e.g., "dr.ho@bnm.gov.my;dr.tng@bnm.gov.my"
#     body = (
#         "Dear Nabil,\n\n"
#         "Cash BOP QC Refresh completed successfully.\n\n"
#         "Regards,\nFaris"
#     )

#     if not already_sent_today():
#         send_email(subject=subject, recipient=recipient, body_text=body, cc=cc_list)
#         update_sent_marker()
#         print("Email sent successfully.")
#     else:
#         print("Email already sent today. Skipping.")
