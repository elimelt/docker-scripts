import datetime
import re
import matplotlib.pyplot as plt
import os

def parse_log_file(filename):
    """
    Parse the log file and extract server requests and client responses.
    """
    with open(filename, 'r') as file:
        content = file.readlines()
    
    requests = [line.strip() for line in content if "Incoming request POST" in line]
    responses = [line.strip() for line in content if "Received response at" in line]
    errors = [line.strip() for line in content if "Error" in line]

    return requests, responses, errors

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
    requests, responses, errors = parse_log_file(filename)
    
    total_requests = len(requests)
    total_responses = len(responses)
    total_errors = len(errors)
    
    first_response_time_str = re.search(r"at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)", responses[0]).group(1)
    last_response_time_str = re.search(r"at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z)", responses[-1]).group(1)
    
    first_response_time = datetime.datetime.fromisoformat(first_response_time_str[:-1])  # Removing the 'Z' at the end
    last_response_time = datetime.datetime.fromisoformat(last_response_time_str[:-1])    # Removing the 'Z' at the end
    
    # Calculate total time
    total_time = (last_response_time - first_response_time).total_seconds()


    throughput = calculate_throughput(total_responses, total_time)
    
    return total_requests, total_responses, total_errors, total_time, throughput,

def parse_logs():
    num_servers_pattern = re.compile(r'results_(\d+)_servers.txt')
    report = {}

    for filename in os.listdir('.'):
        print(f"Processing {filename}")
        match = num_servers_pattern.match(filename)
        if match:

            num_servers = int(match.group(1))
            total_requests, total_responses, total_errors, total_time, throughput = process_file(filename)

            report[num_servers] = {
                'Total Requests': total_requests,
                'Total Responses': total_responses,
                'Total Errors': total_errors,
                'Total Time': total_time,
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

    # save plot
    plt.savefig('throughput.png')


def main():
    report = parse_logs()
    plot_report(report)

    # print report
    for num_servers, stats in sorted(report.items()):
        print(f"\nReport for {num_servers} servers:")
        for key, value in stats.items():
            print(f"{key}: {value:.3f}")

if __name__ == "__main__":
    main()
