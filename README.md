# Ultimate-Server-Status-Checker
The ultimate server status checker is tool made for monitoring connection and the performance of the server, it consists of 3 main parts:
- A HTTPS secure server
- The Status Chcker 
- An android application

The server checker works by running shell commands and forwarding their outputs to a Firebase Realtime Database, The android application then fetches this data and acts as the main UI for the user.

# The Server
The server was writin in Node.js , and it displays a simple HTML page: hello.html, it was secured using the certbot tool which obtains certificates from letsencrypt provider. The server constantly sends its uptime to the Realtime DB. The server is a test server for checking the app.

Code : fserver.js

The server can be accesed at ultimate-checker.ddns.net



# Status Checker
The server status checker code constantly runs some commands in the linux shell, gather their outputs, then redirects them to the realtime DB.

The first code: Checker.py
- Can be run from any device on the same or outside of the network
- Constantly pings the server to check for it status
- Forwards the number of packets sent, received and the percentage packet loss to the realtime DB
- If the 100% packets are lost or an error occurs, lets the user knoew via email that the server is down , then sends timestamp to the realtime DB
- If the code runs on the same network , it has feature to simulate packet loss to the user by randomly subtracting a number from the packets received.

The second code: performance.py
Before running the code , sysstats has to be installed on the server -> sudo apt install sysstats
- The code runs on the server side
- If the server is up , it runs linux commands to check the system's performance
- It checks CPU Utilization, Memory Usage, CPU Temprature and the number of clients connected to the DB
- The code sends the output of these commands to the Database


# Android Application
The android application the main interface for the user to check the status of the server.

App repo:  https://github.com/InterVam/Server-Observer

The application consists of 2 main pages.

Page 1 (Server Status):
- Average packet RTT (speedometer)
- Server Status (Up or Down)
- Last Down Time (Timestamp)
- Down Time Elapsed
- Up time
- Packet Loss
- Packets sent
- Packets Revived
- Button to simulate Packet loss
- Performance Page Button

Page 2 (Performance):
- CPU Utilization (speedometer)
- Memory Usage (speedometer)
- CPU Temperature (speedometer)
