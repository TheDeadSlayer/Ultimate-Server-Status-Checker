// Dependencies
const fs = require('fs');
const http = require('http');
const https = require('https');
const express = require('express');

const app = express();

// Certificate
const privateKey = fs.readFileSync('/etc/letsencrypt/live/ultimate-checker.ddns.net/privkey.pem', 'utf8');
const certificate = fs.readFileSync('/etc/letsencrypt/live/ultimate-checker.ddns.net/cert.pem', 'utf8');
const ca = fs.readFileSync('/etc/letsencrypt/live/ultimate-checker.ddns.net/chain.pem', 'utf8');

var admin = require("firebase-admin");

var serviceAccount = require("/home/deadslayer/Desktop/NetworkProject/server-status-checker-b5e8e-firebase-adminsdk-20kzh-366b85fa7a.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://server-status-checker-b5e8e-default-rtdb.europe-west1.firebasedatabase.app"
});

const { getDatabase } = require('firebase-admin/database');
const db = getDatabase();
const ref = db.ref('/Server').child("-N-ti1d2Yx-PX2JTPcX-");


const credentials = {
	key: privateKey,
	cert: certificate,
	ca: ca
};
const html = fs.readFileSync("hello.html");
app.use((req, res) => {
	res.writeHead(200, { 'Content-Type': 'text/html' });
	res.end(html);
});

// Starting both http & https servers
const httpServer = http.createServer(app);
const httpsServer = https.createServer(credentials, app);

httpServer.listen(80,"192.168.1.100", () => {
	console.log('HTTP Server running on port 80');
});

httpsServer.listen(443,"192.168.1.100", () => {
	console.log('HTTPS Server running on port 443');
	
});

setInterval(() => {
  process.stdout.cursorTo(0); // Stay on the same line
  let uptime = Math.floor(process.uptime());
  ref.update({
  'uptime': uptime
});
  process.stdout.write('Uptime: ' + uptime + 'S');
}, 1000)

