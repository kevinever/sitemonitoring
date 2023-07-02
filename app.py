
# from flask import Flask, render_template
# import requests
# import psycopg2
# from apscheduler.schedulers.background import BackgroundScheduler
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# from sendmail import *
# app = Flask(__name__)
# from defaced import *


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
#             res = requests.get(url,timeout=5)
#             if res.status_code != 200:
#                 send_email()
#             if response.status_code == 200:
#                 content_hash = hashlib.md5(response.content).hexdigest()
#                 cur.execute("UPDATE urls SET status = 200, content_hash = %s WHERE id = %s", (content_hash, url_id))
#                 conn.commit()
#                 message = f"Successfully checked {url} - Status code: {response.status_code}"
#                 print(message)
#                 messages.append(message)
#                 # send_email()
            
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

#                 # Send email notification only if the status code is not 200 and the previous status was also not 200
#                 if status != 200 and status != 0:
#                     cur.execute("SELECT content, defaced_time FROM urls WHERE id = %s", (url_id,))
#                     row = cur.fetchone()
#                     # new_conten`t = response.content.decode('utf-8', errors='ignore')

#                     old_content = row[0]
#                     defaced_time = row[1]
#                     subject = "Website Monitoring Notification"
#                     # send_email(url, old_content, response.content.decode('utf-8'), defaced_time, recipients, subject)
#                     send_email()
#                     print(f"Email triggered for {url}")

                
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
# scheduler.add_job(check_websites, trigger="interval", seconds=10)
# scheduler.start()

# # Keep the script running
# # try:
# #     while True:
# #         pass
# # except KeyboardInterrupt:
# #     scheduler.shutdown()

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


# @app.route('/addmail')
# def addmail():
#     return render_template('addmail.html')


# if __name__ == "__main__":
#     app.run()


from flask import Flask, render_template
import requests
import psycopg2
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from urllib.parse import urlparse
import bs4
import threading

app = Flask(__name__)

def check_websites():
    # Add your database connection details here
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
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                send_email()
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
                    # new_content = response.content.decode('utf-8', errors='ignore')

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


def send_email(url, old_content, new_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
    try:
        # conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost", port="5432")
        # cursor = conn.cursor()
        msg = MIMEText(f"URL: {url}\n\nDefaced Time: {defaced_time}\n\nOld Content:\n{old_content}\n\nNew Content:\n{new_content}")
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = smtp_username
        msg['To'] = ", ".join(recipients)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipients, msg.as_string())
            logging.info(f"Email sent successfully to {recipients}")

    except Exception as e:
        logging.error(f"Error sending email to {recipients}: {e}")


@app.route('/')
def home():
    # Add your database connection details here
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


@app.route('/addmail')
def addmail():
    return render_template('addmail.html')


def run_flask():
    app.run()


def run_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_websites, trigger="interval", seconds=10)
    scheduler.start()



if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    scheduler_thread = threading.Thread(target=run_scheduler)

    flask_thread.start()
    scheduler_thread.start()

    flask_thread.join()
    scheduler_thread.join()
