# BTD_RollSafe

# Description

M5stick, ESP32, processing the signal from accelerometer, counting the pushes of the wheelchair user as well as registering inactivity and reminding the user to move, and being connected to the caretaker's watch in order to ask for help through a click of a button, as well as enabling the caretaker to ask for the daily report of the user's physical activity.

## How to run the application

1. The server needs to start first, only then the connection can be established.
2. The server will not count the pushes until the first connection gets established with the client.
3. Once the connection is established the server counts the steps, and after 10 seconds of inactivity it will have 'Move' written on the screen as well as turn on the M5LED to remind the user to move.
4. Once the button on the server watch is pressed, the message 'Help requested' will be shown and on the client side the message 'Received help request' will be shown as well as the M5LED will be turned on.
5. Once the button on the client side is pressed the message 'Fetching report' is shown and once the message is received it shows the data, pushes and meters crossed.
