# import requests 
import bs4
# from sendmail import *
from app import *



from app import *
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


from apscheduler.schedulers.background import BackgroundScheduler

product="https://kevinever.github.io/hiddentech/"

res = requests.get(product,timeout=5)
if res.status_code != 200:
    pass
def soup():
    url = "https://kevinever.github.io/hiddentech/"  # Replace with your desired URL
    res = requests.get(url, timeout=5)

    if res.status_code == 200:
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        element = soup.select('.bs')
        data = element[0].text

        if element[0].text != "A Best Best Place To find It solutions":
            print("Invalid: Changes detected")
            send_email(url, None, data, None, recipients, "Website Content Changed")
        else:
            print("No changes detected")
    else:
        print("Website not reachable")

# Set up scheduler to check the website every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(soup, trigger="interval", seconds=10)
scheduler.start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()