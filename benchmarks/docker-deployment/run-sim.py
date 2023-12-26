import subprocess
import argparse


def generate_docker_compose(num_servers, server_port_start = 3002):
    services = {}
    client_ports = []

    # generate server services
    for port in range(server_port_start, num_servers + server_port_start):
        service_name = f'server{port - server_port_start + 1}'
        port_mapping = f"\"{port}:{3000}\""
        services[service_name] = {
            "build": "./server",
            "ports": [port_mapping],
            "environment": ["PORT=3000"],
            "volumes": ["./server:/app"]
        }

    # generate client services
    for port in range(4001, 4001 + 5):
        service_name = f'client{port - 4000}'
        port_mapping = f"\"{port}:{3000}\""
        services[service_name] = {
            "build": "./client",
            "ports": [port_mapping],
            "environment": [f"SERVER_PORT_START={server_port_start}", f"SERVER_PORT_END={num_servers + server_port_start - 1}", f"CLIENT_NUM={port - 4000}"],
            "volumes": ["./client:/app"]
        }

    # convert to yaml
    docker_compose_content = "version: '3'\n\nservices:\n"
    for service, config in services.items():
        docker_compose_content += f"  {service}:\n"
        for key, value in config.items():

            if key == "build":
                docker_compose_content += f"    {key}: {value}\n"
                continue

            if isinstance(value, list):
                value = "\n".join([f"      - {item}" for item in value])
            docker_compose_content += f"    {key}:\n{value}\n"
        docker_compose_content += "\n"

    return docker_compose_content


def run_simulation(num_servers):
    # generate docker-compose content
    docker_compose_content = generate_docker_compose(num_servers)
    
    # write to temp file
    with open("docker-compose-temp.yml", "w") as file:
        file.write(docker_compose_content)

    # run docker compose up
    subprocess.run(["docker-compose", "-f", "docker-compose-temp.yml", "up", "-d"])

    # wait for startup
    subprocess.run(["sleep", "20"])

    # capture logs
    result_file = f"results_{num_servers}_servers.txt"
    with open(result_file, "w") as file:
        subprocess.run(["docker-compose", "-f", "docker-compose-temp.yml", "logs"], stdout=file)

    # stop and remove containers
    subprocess.run(["docker-compose", "-f", "docker-compose-temp.yml", "down"])

    print(f"Simulation for {num_servers} servers completed. Results saved in {result_file}")

if __name__ == "__main__":
    # interactive mode

    # parser = argparse.ArgumentParser(description="Run simulation with Docker Compose for a specified number of servers.")
    # parser.add_argument("-n", "--num-servers", type=int, required=True, help="Number of server containers.")
    # args = parser.parse_args()

    # run_simulation(args.num_servers)


    # batch mode
    for i in [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64]:
        run_simulation(i)



