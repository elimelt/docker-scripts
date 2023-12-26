const express = require('express');

const app = express();

app.use(express.json())

app.get('/ping', (req, res) => {
    const timestamp = new Date().toISOString();
    console.log(`Incoming request ${req.method}, ${req.url} received at ${timestamp}`);
    res.send('Hello World!');
});

app.post('/ping', (req, res) => {
    const body = req.body;
    const timestamp = new Date().toISOString();
    console.log(`Incoming request ${req.method}, ${req.url} received at ${timestamp}`);
    res.json(body);
});


app.listen(3000, () => {
    console.log('server listening on port 3000!');
});