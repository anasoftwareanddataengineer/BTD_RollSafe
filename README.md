# BTD_RollSafe
 M5stick, ESP32, processing the signal from accelometer, counting the pushes of the wheelchair user, regisdstering inactivity and reminding the user to move, and being connected to the caretaker's watch in order to ask for help through a click of a button, as well as enabling the caretaker to ask for the daily report of the user's physical activity.
The server needs to start first, only then the connection can be established.
The server will not count the pushes until the first connection gets established with the client.
Once the connection is established the server counts the steps, and after 10 seconds of inactivity it will have 'Move' written on the screen, to remind the user to move.
Once the button on the server watch is pressed, the message 'Help requested' will be shown and on the client side the message 'Recieved help request' will be shown.
Once the button on the client side is pressed the message 'Fetching report' is shown and once the message is recieved it shows the data, pushes and meters crossed.
This exchange can go on, while the watches are turned on, indefinetly. 