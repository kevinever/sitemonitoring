# from sendmail import *
# import time
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
#     cur.execute("SELECT url FROM urls")
#     rows = cur.fetchall()

#     for row in rows:
#         url = row[0]
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
#                     send_email(url, old_content, data, None, recipients, "Website Content Changed")
#                 else:
#                     print(f"No changes detected on {url}")
#             else:
#                 print(f"Website {url} status code is not 200. Please check.")
#                 message = f"Website {url} status code is not 200. Please check."
#                 send_email(url, "Website {url} status code is not 200. Please check.", None, None, recipients, "Website status code is not 200. Please check")
#         except (RequestException, ConnectTimeout, ConnectionError) as e:
#             print(f"An error occurred while accessing {url}: {str(e)}")

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



















# from sendmail import *
# import time
# from urllib.parse import urlparse
# import requests
# from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
# from bs4 import BeautifulSoup
# from apscheduler.schedulers.background import BackgroundScheduler
# import psycopg2

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
#     cur.execute("SELECT url, defaced_time, content_before FROM defaced_websites")
#     rows = cur.fetchall()

#     for row in rows:
#         url, defaced_time, content_before = row
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
#                 if data != content_before:
#                     print(f"Invalid: Changes detected on {url}")
#                     if defaced_time is None:
#                         cur.execute("INSERT INTO defaced_websites (url, content_before, content_after) VALUES (%s, %s, %s)", (url, content_before, data))
#                     else:
#                         cur.execute("UPDATE defaced_websites SET defaced_time = NOW(), content_before = %s, content_after = %s WHERE url = %s", (content_before, data, url))
#                     conn.commit()
#                     send_email(url, content_before, data, defaced_time, recipients, "Website Content Changed")
#                 else:
#                     print(f"No changes detected on {url}")
#             else:
#                 print(f"Website {url} status code is not 200. Please check.")
#                 message = f"Website {url} status code is not 200. Please check."
#                 send_email(url, f"Website {url} status code is not 200. Please check.", None, defaced_time, recipients, "Website status code is not 200. Please check")
#         except (RequestException, ConnectTimeout, ConnectionError) as e:
#             print(f"An error occurred while accessing {url}: {str(e)}")

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
import time
from datetime import datetime
from urllib.parse import urlparse
import requests
from requests.exceptions import RequestException, ConnectTimeout, ConnectionError
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

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
    cur.execute("SELECT url, defaced_time FROM urls")
    rows = cur.fetchall()

    for row in rows:
        url = row[0]
        defaced_time = row[1]
        parsed_url = urlparse(url)

        # Check if the scheme is missing
        if not parsed_url.scheme:
            url = "http://" + url  # Prepend "http://" if no scheme is provided

        if not check_website_status(url):
            print(f"Website {url} is not reachable. Please check.")
            send_email(url, None, None, None, recipients, "Website not reachable")
            continue

        try:
            url = "https://kevinever.github.io/hiddentech/"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                element = soup.select('.bs')
                data = element[0].text
                old_content = "A Best Best Place To find It solutions"
                if element[0].text != old_content:
                    print(f"Invalid: Changes detected on {url}")
                    if defaced_time is None:
                        defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    send_email(url, old_content, data, defaced_time, recipients, "Website Content Changed")
                else:
                    print(f"No changes detected on {url}")
                    defaced_time = None
            else:
                print(f"Website {url} status code is not 200. Please check.")
                message = f"Website {url} status code is not 200. Please check."
                if defaced_time is None:
                    defaced_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                send_email(url, "Website {url} status code is not 200. Please check.", None, defaced_time, recipients, "Website status code is not 200. Please check")
        except (RequestException, ConnectTimeout, ConnectionError) as e:
            print(f"An error occurred while accessing {url}: {str(e)}")

        # Update the defaced time in the database
        cur.execute("UPDATE urls SET defaced_time = %s WHERE url = %s", (defaced_time, url))
        conn.commit()

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
