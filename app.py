
# from flask import Flask, render_template
# import requests
# import psycopg2
# from apscheduler.schedulers.background import BackgroundScheduler
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

# app = Flask(__name__)








# import requests
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# import psycopg2
# import logging
# from urllib.parse import urlparse

# def send_email(url, old_content, new_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
#     try:
#         msg = MIMEText(f"URL: {url}\n\nDefaced Time: {defaced_time}\n\nOld Content:\n{old_content}\n\nNew Content:\n{new_content}")
#         msg['Subject'] = Header(subject, 'utf-8')
#         msg['From'] = smtp_username
#         msg['To'] = ", ".join(recipients)

#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(smtp_username, recipients, msg.as_string())
#             logging.info(f"Email sent successfully to {recipients}")

#     except Exception as e:
#         logging.error(f"Error sending email to {recipients}: {e}")


# try:
#     conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost", port="5432")
#     cursor = conn.cursor()

#     # Fetch the URLs from the `urls` table that have content changes
#     cursor.execute("SELECT url, content FROM urls")
#     urls_data = cursor.fetchall()

#     for row in urls_data:
#         url, old_content = row
#         parsed_url = urlparse(url)
#         if not parsed_url.scheme:
#             url = "http://" + url  # Prepend "http://" if no scheme is provided

#         try:
#             response = requests.get(url, timeout=10)
#             if response.status_code == 200:
#                 new_content = response.content.decode('utf-8', errors='replace')  # Decode with error handling
#                 if old_content is not None and old_content != new_content:
#                     if defaced_time is None:
#                         cursor.execute("INSERT INTO defaced_websites (url, content_before, content_after) VALUES (%s, %s, %s)", (url, old_content, new_content))
#                     else:
#                         cursor.execute("UPDATE defaced_websites SET content_before = %s, content_after = %s WHERE url = %s", (old_content, new_content, url))
#             else:
#                 if defaced_time is None:
#                     cursor.execute("INSERT INTO defaced_websites (url, content_before, content_after) VALUES (%s, %s, %s)", (url, old_content, "Website not reachable"))
#                 else:
#                     cursor.execute("UPDATE defaced_websites SET content_before = %s, content_after = %s WHERE url = %s", (old_content, "Website not reachable", url))

#         except requests.exceptions.RequestException as e:
#             pass

#     cursor.execute("SELECT email FROM users")
#     recipients = [row[0] for row in cursor.fetchall()]

#     subject = "Website Monitoring Notification"  # Set the email subject

#     # Send email to recipients
#     for url_data in urls_data:
#         url, old_content = url_data
#         new_content = None  # Set new_content to None initially
#         defaced_time = None  # Set defaced_time to None initially
#         cursor.execute("SELECT content_after, defaced_time FROM defaced_websites WHERE url = %s", (url,))
#         result = cursor.fetchone()
#         if result is not None:
#             new_content, defaced_time = result
#         send_email(url, old_content, new_content, defaced_time, recipients, subject)

#     conn.commit()

# except Exception as e:
#     logging.error(f"Error fetching data from the database: {e}")









# def check_websites():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()

#     cur.execute("SELECT id, url, status, content, ping FROM urls")
#     rows = cur.fetchall()

#     messages = []

#     for row in rows:
#         url_id = row[0]
#         url = row[1]
#         status = row[2]
#         content = row[3]
#         ping = row[4]

#         response = None
#         try:
#             response = requests.get(url, timeout=10)
#             if response.status_code == 200:
#                 content_hash = hashlib.md5(response.content).hexdigest()
#                 cur.execute("UPDATE urls SET status = 200, content_hash = %s WHERE id = %s", (content_hash, url_id))
#                 conn.commit()
#                 message = f"Successfully checked {url} - Status code: {response.status_code}"
#                 print(message)
#                 messages.append(message)
#             else:
#                 cur.execute("UPDATE urls SET status = %s WHERE id = %s", (response.status_code, url_id))
#                 conn.commit()
#                 message = f"Failed to check {url} - Status code: {response.status_code}"
#                 print(message)
#                 messages.append(message)

#                 recipients = []
#                 cur.execute("SELECT email FROM users")
#                 rows = cur.fetchall()
#                 for row in rows:
#                     recipients.append(row[0])

#                 # Send email notification
#                 cur.execute("SELECT content FROM urls WHERE id = %s", (url_id,))
#                 old_content = cur.fetchone()[0]
#                 subject = "Website Monitoring Notification"
#                 send_email(url, old_content, response.content, recipients, subject)
#                 print(f"Email triggered for {url}")  # Add this line

#         except Exception as e:
#             cur.execute("UPDATE urls SET status = 0 WHERE id = %s", (url_id,))
#             conn.commit()
#             message = f"Failed to check {url} - Status code: 0"
#             print(message)
#             messages.append(message)

#         # Update the ping result in the database
#         cur.execute("UPDATE urls SET ping = %s WHERE id = %s", (ping, url_id))
#         conn.commit()

#     cur.close()
#     conn.close()

#     return messages


# # def send_email(url, old_content, new_content, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
# #     try:
# #         msg = MIMEText(f"URL: {url}\n\nOld Content:\n{old_content}\n\nNew Content:\n{new_content}")
# #         msg['Subject'] = Header(subject, 'utf-8')
# #         msg['From'] = smtp_username
# #         msg['To'] = ', '.join(recipients)

# #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# #             server.ehlo()
# #             server.starttls()
# #             server.ehlo()
# #             server.login(smtp_username, smtp_password)
# #             server.sendmail(smtp_username, recipients, msg.as_string())
# #             print(f"Email sent successfully to {recipients}")

# #     except Exception as e:
# #         print(f"Error sending email to {recipients}: {e}")


# # Set up scheduler to check websites every x seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=check_websites, trigger="interval", seconds=30)
# scheduler.start()


# @app.route('/')
# def home():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()

#     cur.execute("SELECT url, status, ping FROM urls")
#     rows = cur.fetchall()

#     urls = []
#     for row in rows:
#         url = row[0]
#         status = row[1]
#         ping = row[2]

#         urls.append((url, status, ping))

#     messages = check_websites()

#     cur.close()
#     conn.close()

#     return render_template('home.html', urls=urls, messages=messages)


# @app.route('/addweb')
# def addweb():
#     return render_template('addweb.html')

# if __name__ == "__main__":
#     app.run()




# from flask import Flask, render_template
# import requests
# import psycopg2
# from apscheduler.schedulers.background import BackgroundScheduler
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

# app = Flask(__name__)

# def send_email(url, old_content, new_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
#     try:
#         msg = MIMEText(f"URL: {url}\n\nDefaced Time: {defaced_time}\n\nOld Content:\n{old_content}\n\nNew Content:\n{new_content}")
#         msg['Subject'] = Header(subject, 'utf-8')
#         msg['From'] = smtp_username
#         msg['To'] = ", ".join(recipients)

#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(smtp_username, recipients, msg.as_string())
#             print(f"Email sent successfully to {recipients}")

#     except Exception as e:
#         print(f"Error sending email to {recipients}: {e}")


# def check_websites():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()

#     cur.execute("SELECT id, url, status, content, ping FROM urls")
#     rows = cur.fetchall()

#     messages = []

#     for row in rows:
#         url_id = row[0]
#         url = row[1]
#         status = row[2]
#         content = row[3]
#         ping = row[4]

#         response = None
#         try:
#             response = requests.get(url, timeout=10)
#             if response.status_code == 200:
#                 content_hash = hashlib.md5(response.content).hexdigest()
#                 cur.execute("UPDATE urls SET status = 200, content_hash = %s WHERE id = %s", (content_hash, url_id))
#                 conn.commit()
#                 message = f"Successfully checked {url} - Status code: {response.status_code}"
#                 print(message)
#                 messages.append(message)
#             else:
#                 cur.execute("UPDATE urls SET status = %s WHERE id = %s", (response.status_code, url_id))
#                 conn.commit()
#                 message = f"Failed to check {url} - Status code: {response.status_code}"
#                 print(message)
#                 messages.append(message)

#                 recipients = []
#                 cur.execute("SELECT email FROM users")
#                 rows = cur.fetchall()
#                 for row in rows:
#                     recipients.append(row[0])

#                 # Send email notification
#                 cur.execute("SELECT content FROM urls WHERE id = %s", (url_id,))
#                 old_content = cur.fetchone()[0]
#                 subject = "Website Monitoring Notification"
#                 send_email(url, old_content, response.content, recipients, subject)
#                 print(f"Email triggered for {url}")  # Add this line

#         except Exception as e:
#             cur.execute("UPDATE urls SET status = 0 WHERE id = %s", (url_id,))
#             conn.commit()
#             message = f"Failed to check {url} - Status code: 0"
#             print(message)
#             messages.append(message)

#         # Update the ping result in the database
#         cur.execute("UPDATE urls SET ping = %s WHERE id = %s", (ping, url_id))
#         conn.commit()

#     cur.close()
#     conn.close()

#     return messages


# # Set up scheduler to check websites every x seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=check_websites, trigger="interval", seconds=30)
# scheduler.start()


# @app.route('/')
# def home():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()

#     cur.execute("SELECT url, status, ping FROM urls")
#     rows = cur.fetchall()

#     urls = []
#     for row in rows:
#         url = row[0]
#         status = row[1]
#         ping = row[2]

#         urls.append((url, status, ping))

#     messages = check_websites()

#     cur.close()
#     conn.close()

#     return render_template('home.html', urls=urls, messages=messages)


# @app.route('/addweb')
# def addweb():
#     return render_template('addweb.html')


# if __name__ == "__main__":
#     app.run()

from flask import Flask, render_template
import requests
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from sendmail import *
app = Flask(__name__)


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
                # send_email()
            else:
                cur.execute("UPDATE urls SET status = %s WHERE id = %s", (response.status_code, url_id))
                conn.commit()
                message = f"Failed to check {url} - Status code: {response.status_code}"
                print(message)
                messages.append(message)

                recipients = []
                cur.execute("SELECT email FROM users")
                rows = cur.fetchall()
                for row in rows:
                    recipients.append(row[0])

                # Send email notification only if the status code is not 200 and the previous status was also not 200
                if status != 200 and status != 0:
                    cur.execute("SELECT content, defaced_time FROM urls WHERE id = %s", (url_id,))
                    row = cur.fetchone()
                    # new_conten`t = response.content.decode('utf-8', errors='ignore')

                    old_content = row[0]
                    defaced_time = row[1]
                    subject = "Website Monitoring Notification"
                    # send_email(url, old_content, response.content.decode('utf-8'), defaced_time, recipients, subject)
                    send_email()
                    print(f"Email triggered for {url}")

                
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


# Set up scheduler to check websites every x seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_websites, trigger="interval", seconds=30)
scheduler.start()


@app.route('/')
def home():
    conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT url, status, ping FROM urls")
    rows = cur.fetchall()

    urls = []
    for row in rows:
        url = row[0]
        status = row[1]
        ping = row[2]

        urls.append((url, status, ping))

    messages = check_websites()

    cur.close()
    conn.close()

    return render_template('home.html', urls=urls, messages=messages)








@app.route('/addweb')
def addweb():
    return render_template('addweb.html')





if __name__ == "__main__":
    app.run()
