from app import *
# from flask import Flask, render_template,send_file
# import requests

# import psycopg2
# from apscheduler.schedulers.background import BackgroundScheduler
# from bs4 import BeautifulSoup
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import subprocess
# import chardet

# from datascience import *


# from email.utils import COMMASPACE
# from urllib.parse import urlparse
# import logging

# import os
# from app import *
# # def send_email(url, old_content, new_content, user_id, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):

# #     try:
# #         conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost",port="5432")
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT email FROM users WHERE id IN %s", (tuple(user_id),))
# #         to_addr = cursor.fetchone()[0]
# #         from_addr = "kalisadoe@gmail.com"
# #         msg = MIMEText(new_content)
# #     except Exception as e:
# #         logging.error(f"Error fetching email address for user id {user_id}: {e}")
# #         return

# #     # ...

# #     try:
# #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# #             server.ehlo()
# #             server.starttls()
# #             server.ehlo()
# #             server.login(smtp_username, smtp_password)
# #             server.sendmail(from_addr, to_addr, msg.as_string())
# #             logging.info(f"Email sent successfully to {to_addr}")
# #     except Exception as e:
# #         logging.error(f"Error sending email to {to_addr}: {e}")




# # conn = psycopg2.connect("dbname='monitoring' user='postgres' password='post123' host='localhost' port='5432' ")
# # cur = conn.cursor()
# # cur.execute("select url from urls")
# # url = cur.fetchone()[0]
# # cur.execute("select content_before  from defaced_websites")
# # old_content = cur.fetchall()
# # cur.execute("select content_after from defaced_websites")
# # new_content = cur.fetchall()
# # cur.execute("select id from users")
# # user_id = cur.fetchall()
# # conn.commit()

# def send_email(url, old_content, new_content, user_ids, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):

#     try:
#         conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost",port="5432")
#         cursor = conn.cursor()
#         cursor.execute("SELECT email FROM users WHERE id = ANY(%s)", (user_ids,))
#         to_addresses = [row[0] for row in cursor.fetchall()]
#         from_addr = "kalisadoe@gmail.com"
#         msg = MIMEText(new_content)
#     except Exception as e:
#         logging.error(f"Error fetching email addresses for user IDs {user_ids}: {e}")
#         return

#     # ...

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(from_addr, to_addresses, msg.as_string())
#             logging.info(f"Email sent successfully to {to_addresses}")
#     except Exception as e:
#         logging.error(f"Error sending email to {to_addresses}: {e}")


# conn = psycopg2.connect("dbname='monitoring' user='postgres' password='post123' host='localhost' port='5432' ")
# cur = conn.cursor()
# cur.execute("select url from urls")
# url = cur.fetchone()[0]
# cur.execute("select content_before  from defaced_websites")
# old_content = cur.fetchall()
# cur.execute("select content_after from defaced_websites")
# new_content = cur.fetchall()
# cur.execute("select id from users")
# user_id = cur.fetchall()
# conn.commit()

# send_email(url, old_content, new_content, user_id)





# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# import psycopg2
# import logging

# def send_email(url, old_content, new_content, user_ids, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):

#     try:
#         conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost", port="5432")
#         cursor = conn.cursor()
#         cursor.execute("SELECT email FROM users WHERE id = ANY(%s)", (user_ids,))
#         to_addresses = [row[0] for row in cursor.fetchall()]
#         from_addr = "kalisadoe@gmail.com"
#         msg = MIMEText(new_content)
#         msg['Subject'] = Header(subject, 'utf-8')  # Set the subject
#     except Exception as e:
#         logging.error(f"Error fetching email addresses for user IDs {user_ids}: {e}")
#         return

#     # ...

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login(smtp_username, smtp_password)
#             server.sendmail(from_addr, to_addresses, msg.as_string())
#             logging.info(f"Email sent successfully to {to_addresses}")
#     except Exception as e:
#         logging.error(f"Error sending email to {to_addresses}: {e}")


# conn = psycopg2.connect("dbname='monitoring' user='postgres' password='post123' host='localhost' port='5432'")
# cur = conn.cursor()
# cur.execute("SELECT url FROM urls")
# url = cur.fetchone()[0]
# cur.execute("SELECT content_before FROM defaced_websites")
# old_content = cur.fetchall()
# cur.execute("SELECT content_after FROM defaced_websites")
# new_content = cur.fetchall()
# cur.execute("SELECT id FROM users")
# user_id = cur.fetchall()
# conn.commit()

# user_ids = [row[0] for row in user_id]
# old_content = old_content[0][0]
# new_content = new_content[0][0]

# subject = "Website Monitoring Notification"  # Set the email subject

# send_email(url, old_content, new_content, user_ids, subject)
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import psycopg2
import logging
from urllib.parse import urlparse

def send_email(url, old_content, new_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
    try:
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


try:
    conn = psycopg2.connect(dbname="monitoring", user="postgres", password="post123", host="localhost", port="5432")
    cursor = conn.cursor()

    # Fetch the URLs from the `urls` table that have content changes
    cursor.execute("SELECT url, content FROM urls")
    urls_data = cursor.fetchall()

    for row in urls_data:
        url, old_content = row
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "http://" + url  # Prepend "http://" if no scheme is provided

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                new_content = response.content.decode('utf-8', errors='replace')  # Decode with error handling
                if old_content is not None and old_content != new_content:
                    if defaced_time is None:
                        cursor.execute("INSERT INTO defaced_websites (url, content_before, content_after) VALUES (%s, %s, %s)", (url, old_content, new_content))
                    else:
                        cursor.execute("UPDATE defaced_websites SET content_before = %s, content_after = %s WHERE url = %s", (old_content, new_content, url))
            else:
                if defaced_time is None:
                    cursor.execute("INSERT INTO defaced_websites (url, content_before, content_after) VALUES (%s, %s, %s)", (url, old_content, "Website not reachable"))
                else:
                    cursor.execute("UPDATE defaced_websites SET content_before = %s, content_after = %s WHERE url = %s", (old_content, "Website not reachable", url))

        except requests.exceptions.RequestException as e:
            pass

    cursor.execute("SELECT email FROM users")
    recipients = [row[0] for row in cursor.fetchall()]

    subject = "Website Monitoring Notification"  # Set the email subject

    # Send email to recipients
    for url_data in urls_data:
        url, old_content = url_data
        new_content = None  # Set new_content to None initially
        defaced_time = None  # Set defaced_time to None initially
        cursor.execute("SELECT content_after, defaced_time FROM defaced_websites WHERE url = %s", (url,))
        result = cursor.fetchone()
        if result is not None:
            new_content, defaced_time = result
        send_email(url, old_content, new_content, defaced_time, recipients, subject)

    conn.commit()

except Exception as e:
    logging.error(f"Error fetching data from the database: {e}")

# return new_content

