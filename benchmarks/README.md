# Benchmarkign docker for large multi-node systems


## Requirements

- docker
- docker-compose
- python3
- bash or zsh
- node.js

## Plan

How efficient is Docker? I've always wondered just how much overhead there is in containerizing a server. 

To invistigate this, I settled for a simple setup to measure throughput. I have a generic server with a `/ping` endpoint that echos back the sent data in a post request, and a generic client that pings all of the servers using round robin. 

I also wrote a python script to generate a `docker-compose` file with a constant number of clients, and a parameter number of servers deployable. In this way, the overall load on the system should scale linearly with the number of servers provisioned. 

To be clear, I am not pushing these nodes to their limit, and instead am putting a constant load on each of the servers, and seeing how overall system performance is maintained when the scale of an application increases linearly.

I ran the same experiment with a variable number of servers all running in their own process on my machine, and then compared how they performed.

## Running

Inside `./docker_deployment` and `./local_deployment, running `python3 run-sim.py` generates the logs for benchmarking docker and local deployments respectively.

**Format:**

```
Report for <n> servers:
Total Requests: <a>
Total Responses: <b>
Throughput: <c>
```














