import nmap
from flask import Flask

app = Flask(__name__)

@app.route("/")
def scan_website():
    target = "www.igihe.com"  # Replace with the website you want to scan
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments="-sS -p-")
    open_ports = []
    for host in nm.all_hosts():
        for port in nm[host]['tcp']:
            if nm[host]['tcp'][port]['state'] == "open":
                service = nm[host]['tcp'][port]['name']
                open_ports.append(f"Port {port}: {service}")
    html_message = "<h1>Open ports and services</h1>"
    if open_ports:
        html_message += "<ul>"
        for port in open_ports:
            html_message += f"<li>{port}</li>"
        html_message += "</ul>"
    else:
        html_message += "<p>No open ports found.</p>"
    return html_message

if __name__ == "__main__":
    app.run(debug=True)
