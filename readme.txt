## How to run the application

1. The server needs to start first, only then the connection can be established.
2. The server will not count the pushes until the first connection gets established with the client.
3. Once the connection is established the server counts the steps, and after 10 seconds of inactivity it will have 'Move' written on the screen as well as turn on the M5LED to remind the user to move.
4. Once the button on the server watch is pressed, the message 'Help requested' will be shown and on the client side the message 'Received help request' will be shown.
5. Once the button on the client side is pressed the message 'Fetching report' is shown and once the message is received it shows the data, pushes and meters crossed.

This exchange can go on, while the watches are turned on, indefinitely.