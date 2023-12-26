const axios = require('axios');

const SERVER_PORT_START = parseInt(process.env.SERVER_PORT_START);
const SERVER_PORT_END = parseInt(process.env.SERVER_PORT_END);
const CLIENT_NUM = parseInt(process.env.CLIENT_NUM);

if (isNaN(SERVER_PORT_START) || isNaN(SERVER_PORT_END) || isNaN(CLIENT_NUM)) {
    console.error('SERVER_PORT_START, SERVER_PORT_END, and CLIENT_NUM must be set');
    process.exit(1);
}

console.log(`Starting client ${CLIENT_NUM} with ports ${SERVER_PORT_START} to ${SERVER_PORT_END}`);

const serverPorts = Array.from({ length: SERVER_PORT_END - SERVER_PORT_START + 1 }, (_, i) => SERVER_PORT_START + i);

const URL = port => `http://server${port - SERVER_PORT_START + 1}:3000/ping`;
const INTERVAL = 1000; // interval in milliseconds

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
        console.error(`Error waiting for response from ${response}:`, error.message);
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

// send request every INTERVAL milliseconds
setInterval(sendRequest, INTERVAL);
