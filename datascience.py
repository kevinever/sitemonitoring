from flask import Flask, render_template
from urllib import request
import matplotlib.pyplot as plt
import numpy as np

from flask import send_file
app = Flask(__name__)

def checkwebsite(urls):
    """
    Returns a list of tuples, each containing a URL and its status code
    """
    statuses = []
    for url in urls:
        try:
            response = request.urlopen(url)
            status = response.getcode()
        except:
            status = None
        statuses.append((url, status))
    return statuses
import os

@app.route('/plot')
def plot():
    urls = ['https://www.google.com', 'https://www.facebook.com', 'https://www.github.com', 'https://www.example.com']
    websites = checkwebsite(urls)
    statuses = [x[1] for x in websites]

    fig, ax = plt.subplots()
    ax.bar(urls, statuses)
    ax.set_xlabel('Website URL')
    ax.set_ylabel('Status Code')
    ax.set_title('Website Status Codes')

    # Save the plot to a file
    fig.savefig('plot.png')

    # Return the saved image
    return send_file('plot.png', mimetype='image/png')
