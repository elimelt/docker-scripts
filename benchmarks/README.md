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

To be clear, I am not pushing these nodes to their limit, and instead am putting a constant load on each of the servers, and seeing how overall system performance is maintained when the scale of an application increases linearly. I will run the same experiment with a variable number of servers all running in their own process.


## Running
./generate-logs.sh contains the script to generate the logs for the benchmarking. It will generate files with the following format:

```
results_<num-server-nodes>_servers.txt
```

You can analyze an individual log file with:

TO BE CONT.
