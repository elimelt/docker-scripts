const axios = require('axios');

const SERVER_PORT_START = parseInt(process.env.SERVER_PORT_START);
const SERVER_PORT_END = parseInt(process.env.SERVER_PORT_END);
const CLIENT_NUM = parseInt(process.env.CLIENT_NUM);

console.log(`Starting client ${CLIENT_NUM} with ports ${SERVER_PORT_START} to ${SERVER_PORT_END}`);

const serverPorts = Array.from({ length: SERVER_PORT_END - SERVER_PORT_START + 1 }, (_, i) => SERVER_PORT_START + i);

console.log(`Server ports: ${serverPorts}`);

const URL = port => `http://server${port - SERVER_PORT_START + 1}:3000/ping`; // Adjust this URL as needed based on your setup
const INTERVAL = 1000; // Time interval in milliseconds (e.g., every second)

function now() {
    return new Date().toISOString();
}

async function waitAndLog(response) {
    try {
        const start = now();
        const res = await response;
        const end = now();
        console.log(`Received response at ${end} from ${res.config.url}`);
    } catch (error) {
        console.error('Error waiting for response:', error.message);
    }
}

async function sendRequest() {
    const numPorts = SERVER_PORT_END - SERVER_PORT_START + 1;

    try {
        const responses = serverPorts
            .map(port => axios.post(URL(port), { message: 'Hello World!' }));

        responses.forEach(waitAndLog);
    } catch (error) {
        console.error('Error sending request:', error.message);
    }
}

// Set up interval to send requests
setInterval(sendRequest, INTERVAL);
