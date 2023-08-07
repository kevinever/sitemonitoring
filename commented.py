

#                                      this works on kevin.github website


# from sendmail import *
# import time
# from datetime import datetime
# from urllib.parse import urlparse
# import requests
# from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
# from bs4 import BeautifulSoup
# from apscheduler.schedulers.background import BackgroundScheduler

# def check_website_status(url):
#     try:
#         response = requests.get(url, timeout=5)
#         return response.status_code == 200
#     except (RequestException, ConnectTimeout, ConnectionError) as e:
#         print(f"An error occurred while accessing {url}: {str(e)}")
#         return False

# def soup():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()
#     cur.execute("SELECT url, defaced_time FROM urls")
#     rows = cur.fetchall()

#     for row in rows:
#         url = row[0]
#         defaced_time = row[1]
#         parsed_url = urlparse(url)

#         # Check if the scheme is missing
#         if not parsed_url.scheme:
#             url = "http://" + url  # Prepend "http://" if no scheme is provided

#         if not check_website_status(url):
#             print(f"Website {url} is not reachable. Please check.")
#             send_email(url, None, None, None, recipients, "Website not reachable")
#             continue

#         try:
#             url = "https://kevinever.github.io/hiddentech/"
#             res = requests.get(url, timeout=5)
#             if res.status_code == 200:
#                 soup = BeautifulSoup(res.text, 'html.parser')
#                 element = soup.select('.bs')
#                 data = element[0].text
#                 old_content = "A Best Best Place To find It solutions"
#                 if element[0].text != old_content:
#                     print(f"Invalid: Changes detected on {url}")
#                     if defaced_time is None:
#                         defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     send_email(url, old_content, data, defaced_time, recipients, "Website Content Changed")
#                 else:
#                     print(f"No changes detected on {url}")
#                     defaced_time = None
#             else:
#                 print(f"Website {url} status code is not 200. Please check.")
#                 message = f"Website {url} status code is not 200. Please check."
#                 if defaced_time is None:
#                     defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 send_email(url, "Website {url} status code is not 200. Please check.", None, defaced_time, recipients, "Website status code is not 200. Please check")
#         except (RequestException, ConnectTimeout, ConnectionError) as e:
#             print(f"An error occurred while accessing {url}: {str(e)}")

#         # Update the defaced time in the database
#         cur.execute("UPDATE urls SET defaced_time = %s WHERE url = %s", (defaced_time, url))
#         conn.commit()

#     cur.close()
#     conn.close()

# # Set up scheduler to check the websites every 10 seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(soup, trigger="interval", seconds=10)
# scheduler.start()

# # Keep the script running
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     scheduler.shutdown()






# ###############                    this works perfect but all it does is it checks for a simple class 


# from sendmail import *
# import psycopg2
# import time
# from datetime import datetime
# from urllib.parse import urlparse
# import requests
# from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
# from bs4 import BeautifulSoup
# from apscheduler.schedulers.background import BackgroundScheduler
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

# # Function to send an email notification
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


# def check_website_status(url):
#     try:
#         response = requests.get(url, timeout=5)
#         return response.status_code == 200
#     except (RequestException, ConnectTimeout, ConnectionError) as e:
#         print(f"An error occurred while accessing {url}: {str(e)}")
#         return False

# def soup():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()
#     cur.execute("SELECT url, defaced_time, content_before, reference_content FROM urls")
#     rows = cur.fetchall()

#     for row in rows:
#         url = row[0]
#         defaced_time = row[1]
#         old_content = row[2]
#         reference_content = row[3]
#         parsed_url = urlparse(url)

#         # Check if the scheme is missing
#         if not parsed_url.scheme:
#             url = "http://" + url  # Prepend "http://" if no scheme is provided

#         if not check_website_status(url):
#             print(f"Website {url} is not reachable. Please check.")
#             send_email(url, None, None, None, recipients, "Website not reachable")
#             continue

#         new_content = None  # Initialize new_content as None

#         try:
#             res = requests.get(url, timeout=5)
#             if res.status_code == 200:
#                 soup = BeautifulSoup(res.text, 'html.parser')
#                 element = soup.select('#gradient')
#                 if element:
#                     new_content = element[0].text
#                     if reference_content is not None and reference_content != new_content:
#                         print(f"Invalid: Changes detected on {url}")
#                         if defaced_time is None:
#                             defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                         send_email(url, reference_content, new_content, defaced_time, recipients, "Website Content Changed")
#                     else:
#                         print(f"No changes detected on {url}")
#                         defaced_time = None
#                 else:
#                     print(f"No element found with selector '.bs' on {url}")
#                     send_email(url, old_content, None, defaced_time, recipients, "Selector not defined")
#             else:
#                 print(f"Website {url} status code is not 200. Please check.")
#                 message = f"Website {url} status code is not 200. Please check."
#                 if defaced_time is None:
#                     defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 send_email(url, "Website {url} status code is not 200. Please check.", None, defaced_time, recipients, "Website status code is not 200. Please check")
#         except (RequestException, ConnectTimeout, ConnectionError) as e:
#             print(f"An error occurred while accessing {url}: {str(e)}")

#         # Update the defaced time and content_before in the database
#         cur.execute("UPDATE urls SET defaced_time = COALESCE(%s, defaced_time), content_before = %s WHERE url = %s", (defaced_time, new_content, url))
#         conn.commit()

#     cur.close()
#     conn.close()

# # Set up scheduler to check the websites every 10 seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(soup, trigger="interval", seconds=10)
# scheduler.start()

# # Keep the script running
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     scheduler.shutdown()














from sendmail import *
import psycopg2
import time
from datetime import datetime
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import difflib

# Function to send an email notification with only the changed content highlighted in red
def send_email(url, changed_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
    try:
        html_content = f"""\
        <html>
        <body>
            <p><strong>URL:</strong> {url}</p>
            <p><strong>Defaced Time:</strong> {defaced_time}</p>
            <p><strong>Changed Content:</strong></p>
            <pre style="background-color: #f8f8f8; padding: 10px;">
                {changed_content}
            </pre>
        </body>
        </html>
        """
        msg = MIMEText(html_content, 'html')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = smtp_username
        msg['To'] = ", ".join(recipients)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipients, msg.as_string())
            print(f"Email sent successfully to {recipients}")

    except Exception as e:
        print(f"Error sending email to {recipients}: {e}")


def check_website_status(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except (RequestException, ConnectTimeout, ConnectionError) as e:
        print(f"An error occurred while accessing {url}: {str(e)}")
        return False

def soup():
    conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT url, defaced_time, content_before FROM urls")
    rows = cur.fetchall()

    for row in rows:
        url = row[0]
        defaced_time = row[1]
        old_content = row[2]
        parsed_url = urlparse(url)

        # Check if the scheme is missing
        if not parsed_url.scheme:
            url = "http://" + url  # Prepend "http://" if no scheme is provided

        if not check_website_status(url):
            print(f"Website {url} is not reachable. Please check.")
            send_email(url, None, None, recipients, "Website not reachable")
            continue

        new_content = None  # Initialize new_content as None

        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                new_content = soup.prettify()
                if old_content is not None and old_content != new_content:
                    print(f"Invalid: Changes detected on {url}")

                    # Calculate the differences between old and new content as plain text
                    diff = difflib.ndiff(old_content.splitlines(), new_content.splitlines())
                    content_diff = "\n".join(line[2:] for line in diff if line.startswith("+ "))

                    if defaced_time is None:
                        defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Highlight the changed content in red
                    changed_content_html = content_diff.replace('+ ', '<span style="color: red;">') + "</span>"

                    send_email(url, changed_content_html, defaced_time, recipients, "Website Content Changed")
                else:
                    print(f"No changes detected on {url}")
                    defaced_time = None
            else:
                print(f"Website {url} status code is not 200. Please check.")
                message = f"Website {url} status code is not 200. Please check."
                if defaced_time is None:
                    defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                send_email(url, message, defaced_time, recipients, "Website status code is not 200. Please check")
        except (RequestException, ConnectTimeout, ConnectionError) as e:
            print(f"An error occurred while accessing {url}: {str(e)}")

        # Update the defaced time and content_before in the database
        cur.execute("UPDATE urls SET defaced_time = COALESCE(%s, defaced_time), content_before = %s WHERE url = %s", (defaced_time, new_content, url))
        conn.commit()
        return changed_content_html

    cur.close()
    conn.close()

# Set up scheduler to check the websites every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(soup, trigger="interval", seconds=10)
scheduler.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()














# from sendmail import *
# import psycopg2
# import time
# from datetime import datetime
# from urllib.parse import urlparse
# import requests
# from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
# from bs4 import BeautifulSoup
# from apscheduler.schedulers.background import BackgroundScheduler
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
# import difflib

# # Function to send an email notification with only the changed content highlighted in red
# def send_email(url, changed_content, defaced_time, recipients, subject, smtp_server='smtp.gmail.com', smtp_port=587, smtp_username='kalisadoe@gmail.com', smtp_password='pibdptzdjqvltexu'):
#     try:
#         html_content = f"""\
#         <html>
#         <body>
#             <p><strong>URL:</strong> {url}</p>
#             <p><strong>Defaced Time:</strong> {defaced_time}</p>
#             <p><strong>Changed Content:</strong></p>
#             <pre style="background-color: #f8f8f8; padding: 10px;">
#                 {changed_content}
#             </pre>
#         </body>
#         </html>
#         """
#         msg = MIMEText(html_content, 'html')
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
    


# def check_website_status(url):
#     try:
#         response = requests.get(url, timeout=5)
#         return response.status_code == 200
#     except (RequestException, ConnectTimeout, ConnectionError) as e:
#         print(f"An error occurred while accessing {url}: {str(e)}")
#         return False

#     # this works but we're going to remove the null cvalue 

# def soup():
#     conn = psycopg2.connect(database="monitoring", user="postgres", password="post123", host="127.0.0.1", port="5432")
#     cur = conn.cursor()
#     cur.execute("SELECT url, defaced_time, content_before FROM urls")
#     rows = cur.fetchall()

#     for row in rows:
#         url = row[0]
#         defaced_time = row[1]
#         old_content = row[2]
#         parsed_url = urlparse(url)

#         # Check if the scheme is missing
#         if not parsed_url.scheme:
#             url = "http://" + url  # Prepend "http://" if no scheme is provided

#         if not check_website_status(url):
#             print(f"Website {url} is not reachable. Please check.")
#             defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             print(defaced_time)
#             update_defaced_time_in_database(url, defaced_time)
#             send_email(url, None, None, recipients, "Website not reachable")
#             continue

#         new_content = None  # Initialize new_content as None

#         try:
#             res = requests.get(url, timeout=5)
#             if res.status_code == 200:
#                 soup = BeautifulSoup(res.text, 'html.parser')
#                 new_content = soup.prettify()
#                 if old_content is not None and old_content != new_content:
#                     print(f"Invalid: Changes detected on {url}")
#                     defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     update_defaced_time_in_database(url, defaced_time)

#                     # Calculate the differences between old and new content as plain text
#                     diff = difflib.ndiff(old_content.splitlines(), new_content.splitlines())
#                     content_diff = "\n".join(line[2:] for line in diff if line.startswith("+ "))

#                     if defaced_time is None:
#                         # url = "www.apexconnect.rw"
#                         defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                         update_defaced_time_in_database(url, defaced_time)

#                     # Highlight the changed content in red
#                     changed_content_html = content_diff.replace('+ ', '<span style="color: red;">') + "</span>"

#                     send_email(url, changed_content_html, defaced_time, recipients, "Website Content Changed")
#                     update_defaced_time_in_database(url, defaced_time)
#                 else:
#                     print(f"No changes detected on {url}")
#                     # defaced_time = None
#                     defaced_time = f"no changes detected on {url}"
#             else:
#                 print(f"Website {url} status code is not 200. Please check.")
#                 message = f"Website {url} status code is not 200. Please check."
#                 if defaced_time is None:
#                     # url = 'www.higacreatives.com'
#                     defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 send_email(url, message, defaced_time, recipients, "Website status code is not 200. Please check")
#         except (RequestException, ConnectTimeout, ConnectionError) as e:
#             print(f"An error occurred while accessing {url}: {str(e)}")
#         cur.execute("UPDATE urls SET defaced_time = %s WHERE url = %s", (defaced_time, url))
#         conn.commit()
#         print(f"Defaced time updated in the database for {url}")

#         # Update the defaced time and content_before in the database
#         # cur.execute("UPDATE urls SET defaced_time = COALESCE(%s, defaced_time), content_before = %s WHERE url = %s", (defaced_time, new_content, url))
#         # conn.commit()

#     cur.close()
#     conn.close()
# def update_defaced_time_in_database(url, defaced_time):
#     if defaced_time is None:
#         return  # Skip updating defaced_time if it is None

#     conn = psycopg2.connect("dbname='monitoring' user='postgres' password='post123' port='5432'")
#     cur = conn.cursor()

#     try:
#         print(f"Executing query: UPDATE urls SET defaced_time = '{defaced_time}' WHERE url = '{url}'")
#         cur.execute(f"UPDATE urls SET defaced_time = %s WHERE url = %s", (defaced_time, url))
#         conn.commit()
#         print(f"Defaced time updated in the database for {url}")
#     except psycopg2.Error as e:
#         print(f"Error updating defaced time in the database for {url}: {str(e)}")


# # Set up scheduler to check the websites every 10 seconds
# scheduler = BackgroundScheduler()
# scheduler.add_job(soup, trigger="interval", seconds=10)
# scheduler.start()

# # Keep the script running
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     scheduler.shutdown()
