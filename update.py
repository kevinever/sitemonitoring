# from commented import *

# def update_defaced_time_in_database(url, defaced_time):
#     if defaced_time is None:
#         return  # Skip updating defaced_time if it is None

#     conn = psycopg2.connect("dbname='monitoring' user='postgres' password='post123' port='5432'")
#     cur = conn.cursor()

#     try:
#         url = 'https://kevinever.github.io/hiddentech/'
#         defaced_time =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         cur.execute("UPDATE urls SET defaced_time = %s WHERE url = %s", (defaced_time,url))
#         conn.commit()
#         print(f"Defaced time updated in the database for {url}")
#     except psycopg2.Error as e:
#         print(f"Error updating defaced time in the database for {url}: {str(e)}")
