import socket
from m5stack import *
from m5ui import *
from uiflow import *
import network
import socket
import time

HOST = "192.168.4.1"  # The server's hostname or IP address
PORT = 50  # The port used by the server

lcd.clear(0x000000)  # black
status_lbl = M5TextBox(10, 30, "Status", lcd.FONT_DejaVu18,
                       0xffffff, rotate=0)  # white

report_lbl_pushes = M5TextBox(10, 120, "P: ", lcd.FONT_DejaVu24,
                       0xffffff, rotate=0)  # white
report_lbl_distance = M5TextBox(10, 140, "D: ", lcd.FONT_DejaVu24,
                       0xffffff, rotate=0)  # white

# Set up wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("M5", "")
status_lbl.setText("Connected to Wifi")


def fetch_report(s):
    '''Fetch report from server watch'''
    lcd.clear(0x000000)  # black

    status_lbl.setText("Fetching report")
    # Send a request to the server
    s.sendall(str("fetch_report").encode('utf-8'))

    # Receive the report from the server
    report = s.recv(1024).decode('utf-8')

    # Display the report on the LCD
    lcd.clear(0x000000)  # black
    
    return report

def request_report(s):
    '''Request report from server watch'''
    lcd.clear(0x000000)  # black

    status_lbl.setText("Fetching report")
    # Send a request to the server
    s.sendall(str("fetch_report").encode('utf-8'))
    
    return report

def display_report(report):
    '''Display report on LCD'''
    report = report.split(";")
    
    # Display the report on the LCD
    report_lbl_pushes.setText("Pushes: " + report[0])
    report_lbl_distance.setText("Distance: " + report[1])

def display_help_message():
    '''Display help request'''
    status_lbl.setText("Received help request")
    M5Led.on()  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    time.sleep(1) # just a delay to see the wifi connected label, uncomment if needed
    s.connect((HOST, PORT))
    s.settimeout(0.5)
    status_lbl.setText("Connected to Server")

    report = ""

    while True:

        # Fetch report from server watch
        if btnA.wasPressed():
            report = request_report(s)
        
        try:
            # Receive from server
            received = s.recv(1024).decode('utf-8').strip()
            
            if received != '':
                lcd.clear(0x000000)  # black    
                
                if received == 'request_help':
                    display_help_message()
                else:
                    display_report(received)
        except:
            received = None

finally:
    s.close()
    