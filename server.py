import select
import socket

from m5stack import lcd
import machine
import time
import imu
from m5stack import *
from m5ui import *
from uiflow import *
import network
import socket

lcd.clear()
label0 = M5TextBox(50, 50, "waiting", lcd.FONT_Default, 0xcf0d00, rotate=0) #red text
label1 = M5TextBox(70, 70, "Push Count", lcd.FONT_Default, 0xcf0d00, rotate=0) #red text
label2 = M5TextBox(90, 90, "Move Count", lcd.FONT_Default, 0xcf0d00, rotate=0) # Move Text
label3 = M5TextBox(50, 100, "", lcd.FONT_Default, 0xcf0d00, rotate=0) #red text
network_label = M5TextBox(0, 130, "Network", lcd.FONT_Default, 0xcf0d00, rotate=0) 

imu0 = imu.IMU()

#make the watch an access point without password to enter. Client will connect to M5 and send/recieve messages
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="M5")

#listen to client
hostAddr = socket.getaddrinfo('0.0.0.0', 50)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(hostAddr)
s.listen(1)

Fs = 10 # sampling frequency
a_lpf = [0.0296128]
b_lpf = [0.4851936, 0.4851936]
a_hpf = [-0.77411293]
b_hpf = [0.11294354, -0.11294354]

array_accel_mag = []

def applyFilter(x, inputCoeff = [1,0], outputCoeff = [0]):
# Filter the signal using the difference equation
    y = [0 for element in range(len(x))]
    for i in range(2, len(x)):
        y[i] = outputCoeff[0]*y[i-1] + inputCoeff[0]*x[i] + inputCoeff[1]*x[i-1]
    return y

def process_pushes(array_accel_mag):
    tlims = [0,int(len(array_accel_mag)/Fs)]        # to have 1 second of simulated signal

    # generate the signal based on the above frequencies and amplitudes
    x = array_accel_mag[0:tlims[1]*Fs]
    # let y now be the high-pass filtered signal
    y = applyFilter(x,b_hpf,a_hpf)
    
    threshold_for_pushes = 0.1

    threshold_signal = []

    for i in y:
        if i >= threshold_for_pushes:
            threshold_signal.append(i)
        else:
            threshold_signal.append(0)

    pushes = 0
    currently_pushing = False

    for i in threshold_signal:
        if i > 0 and not currently_pushing:
            pushes += 1
            currently_pushing = True
        elif i == 0:
            currently_pushing = False
    
    return pushes


def process_activity(array_accel_mag):
    tlims = [0,int(len(array_accel_mag)/Fs)]        # to have 1 second of simulated signal

    # generate the signal based on the above frequencies and amplitudes
    x = array_accel_mag[0:tlims[1]*Fs]

    # let y be the low-pass filtered signal
    y = applyFilter(x,b_lpf,a_lpf)

    threshold_for_activity = 1.20

    for i in y:
        if i >= threshold_for_activity:
            return True
        
    return False

def isSocketClosed(sock: socket.socket) -> bool:
    return False

def readSocketIfAvailable() -> str:
    if readable == None:
        return ''

    r = select.select(readable,[],[],0)
    for rs in r: # iterate through readable sockets
        if rs is conn: # is it the server# read from a client
            data = rs.recv(1024)
            if not data:
                network_label.setText('disconnected')
                readable.remove(rs)
                rs.close()
            else:
                decoded = data.decode('UTF-8') # decode what is recieved from the client
                network_label.setText(str(decoded))
                return decoded
    return ''


push_count = 0
last_activity_seconds_ago = 0

conn, addr = s.accept()
readable = [conn]

while True:

    conn, addr = s.accept()
    readable = [conn]

    counter = 0
    while counter < 10:
        x_accel, y_accel, z_accel = imu0.acceleration
        accel_mag = (float(x_accel) ** 2 + float(y_accel) ** 2 + float(z_accel) ** 2) ** 0.5
        array_accel_mag.append(accel_mag)
        
        counter += 1
        time.sleep(0.1)
    
    pushed = process_pushes(array_accel_mag=array_accel_mag)
    array_accel_mag.clear()
    push_count += pushed

    if pushed == 0:
        last_activity_seconds_ago += 1
    else:
        last_activity_seconds_ago = 0

    if last_activity_seconds_ago >= 10:
        label2.setText('Move')
    else:
        label2.setText('')

    label1.setText(str(push_count))

    if readSocketIfAvailable() == 'fetch_report':
        conn.sendall('{};{}'.format(push_count, push_count*2).encode('utf-8'))
        network_label.setText("Report sent")
        
    if btnA.wasPressed():
        conn.sendall('request_help'.encode('utf-8'))
        network_label.setText("Help requested")

