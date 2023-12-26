const express = require('express');

/*
client port range: [3001, 3005]
server port range: [3006, n + 3005]
*/


const SERVER_NUMBER = parseInt(process.env.SERVER_NUMBER);
const NUM_CLIENTS = 5;

if (isNaN(SERVER_NUMBER)) {
    console.error(`server${SERVER_NUMBER}  | SERVER_NUMBER must be set`);
    process.exit(1);
}

const app = express();

app.use(express.json())

app.get('/ping', (req, res) => {
    const timestamp = new Date().toISOString();
    console.log(`server${SERVER_NUMBER}  | Incoming request ${req.method}, ${req.url} received at ${timestamp}`);
    res.send('Hello World!');
});

app.post('/ping', (req, res) => {
    const body = req.body;
    const timestamp = new Date().toISOString();
    console.log(`server${SERVER_NUMBER}  | Incoming request ${req.method}, ${req.url} received at ${timestamp}`);
    res.json(body);
});


app.listen(3000 + NUM_CLIENTS + SERVER_NUMBER, () => {
    console.log(`server${SERVER_NUMBER}  | server listening on port ${3000 + NUM_CLIENTS + SERVER_NUMBER}`);
});