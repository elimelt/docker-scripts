const axios = require('axios');

const SERVER_PORT_START = parseInt(process.env.SERVER_PORT_START);
const SERVER_PORT_END = parseInt(process.env.SERVER_PORT_END);
const CLIENT_NUMBER = parseInt(process.env.CLIENT_NUMBER);

if (isNaN(SERVER_PORT_START) || isNaN(SERVER_PORT_END) || isNaN(CLIENT_NUMBER)) {
    console.error(`client${CLIENT_NUMBER}  | SERVER_PORT_START, SERVER_PORT_END, and CLIENT_NUMBER must be set`);
    process.exit(1);
}

console.log(`client${CLIENT_NUMBER}  | Starting client ${CLIENT_NUMBER} with ports ${SERVER_PORT_START} to ${SERVER_PORT_END}`);

const serverPorts = Array.from({ length: SERVER_PORT_END - SERVER_PORT_START + 1 }, (_, i) => SERVER_PORT_START + i);

const URL = port => `http://localhost:${port}/ping`;
const INTERVAL = 1000; // interval in milliseconds

function now() {
    return new Date().toISOString();
}

async function waitAndLog(response) {
    try {
        const start = now();
        const res = await response;
        const end = now();
        console.log(`client${CLIENT_NUMBER}  | Received response at ${end} from ${res.config.url}`);
    } catch (error) {
        console.error(`client${CLIENT_NUMBER}  | Error waiting for response from ${response}:`, error.message);
    }
}

async function sendRequest() {
    const numPorts = SERVER_PORT_END - SERVER_PORT_START + 1;

    try {
        const responses = serverPorts
            .map(port => axios.post(URL(port), { message: 'Hello World!' }));

        responses.forEach(waitAndLog);
    } catch (error) {
        console.error(`client${CLIENT_NUMBER}  | Error sending request:`, error.message);
    }
}

// send request every INTERVAL milliseconds
setInterval(sendRequest, INTERVAL);
