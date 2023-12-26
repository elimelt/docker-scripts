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

    # convert services dictionary to yaml format
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Docker Compose file with specified number of servers and port range for clients.")
    parser.add_argument("-n", "--num-servers", type=int, required=True, help="Number of server containers.")
    args = parser.parse_args()

    docker_compose_content = generate_docker_compose(args.num_servers)
    with open("docker-compose.yml", "w") as file:
        file.write(docker_compose_content)

