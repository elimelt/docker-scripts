import re
import matplotlib.pyplot as plt

def parse_log_file(filename):
    """
    Parse the log file and extract server requests and client responses.
    """
    with open(filename, 'r') as file:
        content = file.readlines()
    
    requests = [line.strip() for line in content if "Incoming request POST" in line]
    responses = [line.strip() for line in content if "Received response at" in line]
    
    return requests, responses

def count_incoming_requests(requests):
    """
    Count the number of incoming requests from server logs.
    """
    return len(requests)

def count_received_responses(responses):
    """
    Count the number of received responses from client logs.
    """
    return len(responses)

def calculate_throughput(total_responses, total_time):
    """
    Calculate the throughput rate.
    """
    return total_responses / total_time if total_time != 0 else 0

def process_file(filename):
    requests, responses = parse_log_file(filename)
    
    total_requests = count_incoming_requests(requests)
    total_responses = count_received_responses(responses)
    
    # Extract timestamps from the first and last response to get the total time taken
    first_response_time = re.search(r"at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)", responses[0])
    last_response_time = re.search(r"at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)", responses[-1])
    
    if first_response_time and last_response_time:
        total_time = float(last_response_time.group(1).replace('Z', '').replace('T', '').replace(':', '').replace('-', '')) - \
                     float(first_response_time.group(1).replace('Z', '').replace('T', '').replace(':', '').replace('-', ''))
    else:
        total_time = 0
    
    throughput = calculate_throughput(total_responses, total_time)
    
    return total_requests, total_responses, throughput

def parse_logs():
    num_servers_pattern = re.compile(r'results_(\d+)_servers.txt')
    report = {}

    for filename in os.listdir('.'):
        print(f"Processing {filename}")
        match = num_servers_pattern.match(filename)
        if match:

            num_servers = int(match.group(1))
            total_requests, total_responses, throughput = process_file(filename)

            report[num_servers] = {
                'Total Requests': total_requests,
                'Total Responses': total_responses,
                'Throughput': throughput
            }

    return report

def plot_report(report):
    num_servers = []
    throughput = []
    for num_server, stats in sorted(report.items()):
        num_servers.append(num_server)
        throughput.append(stats['Throughput'])

    plt.plot(num_servers, throughput)
    plt.xlabel('Number of Servers')
    plt.ylabel('Throughput')
    plt.title('Throughput vs Number of Servers')

    # Save the plot
    plt.savefig('throughput.png')


def main():
    report = parse_logs()

    # Plot the report
    plot_report(report)

    # Print the report
    for num_servers, stats in sorted(report.items()):
        print(f"\nReport for {num_servers} servers:")
        for key, value in stats.items():
            print(f"{key}: {value:.3f}")

if __name__ == "__main__":
    import os
    main()
