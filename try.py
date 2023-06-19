import requests
import psycopg2
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback

def send_email(url, old_content, new_content, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
    try:
        msg = MIMEText(f"URL: {url}\n\nOld Content:\n{old_content}\n\nNew Content:\n{new_content}")
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = smtp_username
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipients, msg.as_string())
            print(f"Email sent successfully to {recipients}")

    except Exception as e:
        print(f"Error sending email to {recipients}: {e}")
        traceback.print_exc()

def check_websites():
    conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT id, url, status, content, ping FROM urls")
    rows = cur.fetchall()

    messages = []

    for row in rows:
        url_id = row[0]
        url = row[1]
        status = row[2]
        content = row[3]
        ping = row[4]

        response = None
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content_hash = hashlib.md5(response.content).hexdigest()
                cur.execute("UPDATE urls SET status = 200, content_hash = %s WHERE id = %s", (content_hash, url_id))
                conn.commit()
                message = f"Successfully checked {url} - Status code: {response.status_code}"
                print(message)
                messages.append(message)
            else:
                cur.execute("UPDATE urls SET status = %s WHERE id = %s", (response.status_code, url_id))
                conn.commit()
                message = f"Failed to check {url} - Status code: {response.status_code}"
                print(message)
                messages.append(message)

                if response.status_code != 200:  # Only send email if status code is not 200
                    recipients = []
                    cur.execute("SELECT email FROM users")
                    rows = cur.fetchall()
                    for row in rows:
                        recipients.append(row[0])

                    # Send email notification
                    cur.execute("SELECT content FROM urls WHERE id = %s", (url_id,))
                    old_content = cur.fetchone()[0]

                    subject = "Website Monitoring Notification"
                    send_email(url, old_content, response.content, recipients, subject)
                    print(f"Email triggered for {url}")  # Add this line

        except Exception as e:
            cur.execute("UPDATE urls SET status = 0 WHERE id = %s", (url_id,))
            conn.commit()
            message = f"Failed to check {url} - Status code: 0"
            print(message)
            messages.append(message)

        # Update the ping result in the database
        cur.execute("UPDATE urls SET ping = %s WHERE id = %s", (ping, url_id))
        conn.commit()

    cur.close()
    conn.close()

    return messages


    # return messages


if __name__ == "__main__":
    check_websites()
    # send_email()
