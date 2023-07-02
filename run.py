# from flask import Flask
# from threading import Thread
# from app import app
from defaced import soup

# def run_flask():
#     # Run the Flask server
#     app.run(debug=True)  # Adjust the parameters as needed

# def run_scheduler():
#     # Call the function to start the scheduler script
#     soup()  # Adjust the function name and parameters as needed

# if __name__ == '__main__':
#     # Create threads for Flask server and scheduler
#     flask_thread = Thread(target=run_flask)
#     scheduler_thread = Thread(target=run_scheduler)

#     # Start both threads
#     flask_thread.start()
#     scheduler_thread.start()

#     # Optionally, wait for both threads to complete
#     flask_thread.join()
#     scheduler_thread.join()


# from flask import Flask
# from threading import Thread
# import subprocess

# def run_flask():
#     # Run the Flask server using subprocess
#     subprocess.run(["flask", "run"])  # Adjust the parameters as needed

# def run_scheduler():
#     # Call the function to start the scheduler script
#     soup()  # Adjust the function name and parameters as needed

# if __name__ == '__main__':
#     # Create threads for Flask server and scheduler
#     flask_thread = Thread(target=run_flask)
#     scheduler_thread = Thread(target=run_scheduler)

#     # Start both threads
#     flask_thread.start()
#     scheduler_thread.start()

#     # Optionally, wait for both threads to complete
#     flask_thread.join()
#     scheduler_thread.join()



from flask import Flask
from threading import Thread
import subprocess
import webbrowser
from defaced import * 

def run_flask():
    # Run the Flask server using subprocess
    subprocess.run(["flask", "run"])  # Adjust the parameters as needed

def open_browser():
    # Open the Flask app in a web browser
    webbrowser.open("http://127.0.0.1:5000/")  # Adjust the URL as needed

def run_scheduler():
    # Call the function to start the scheduler script
    soup()  # Adjust the function name and parameters as needed

if __name__ == '__main__':
    # Create threads for Flask server, browser, and scheduler
    flask_thread = Thread(target=run_flask)
    browser_thread = Thread(target=open_browser)
    scheduler_thread = Thread(target=run_scheduler)

    # Start all threads
    flask_thread.start()
    browser_thread.start()
    scheduler_thread.start()

    # Optionally, wait for all threads to complete
    flask_thread.join()
    browser_thread.join()
    scheduler_thread.join()
