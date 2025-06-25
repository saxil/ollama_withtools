import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_smtp(smtp_host, smtp_port, smtp_user, smtp_pass, sender, recipients, subject, body, html=None):
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = 'sahilchanna14@gmail.com'
    msg['Subject'] = subject

    part1 = MIMEText(body, 'plain', 'utf-8')
    msg.attach(part1)
    if html:
        part2 = MIMEText(html, 'html', 'utf-8')
        msg.attach(part2)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            if smtp_port == 587:
                server.starttls(context=context)
                server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender, recipients, msg.as_string())
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Failed to send email: {e}"
