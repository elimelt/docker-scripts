import argparse
import subprocess
import time

def run_simulation(num_servers):

     # define the output file
    output_file = f"results_{num_servers}_servers.txt"

    # start the simulation subprocess with output redirection
    with open(output_file, "w") as file:
        proc = subprocess.Popen(["./deploy-with.sh", str(num_servers)], stdout=file, stderr=subprocess.PIPE)

    # wait
    time.sleep(20)

    # stop subprocess
    print("Stopping the simulation...")
    proc.terminate()
    proc.wait()

    print(f"Simulation for {num_servers} servers completed.")

if __name__ == "__main__":
    # interactive mode

    # parser = argparse.ArgumentParser(description="Run simulation with Docker Compose for a specified number of servers.")
    # parser.add_argument("-n", "--num-servers", type=int, required=True, help="Number of server containers.")
    # args = parser.parse_args()

    # batch mode
    for i in [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64]:
        print(f"Running simulation for {i} servers...")
        run_simulation(i)
