import numpy as np

# Function to initialize the system
def initialize_system(num_processes, num_resources):
    global num_res, resources, max_claim, allocation, need

    num_res = num_resources
    resources = np.zeros(num_res, dtype=int)
    max_claim = np.zeros((num_processes, num_res), dtype=int)
    allocation = np.zeros((num_processes, num_res), dtype=int)
    need = np.zeros((num_processes, num_res), dtype=int)

    print("Initializing the system...\n")
    for i in range(num_res):
        resources[i] = int(input(f"Enter the number of units for Resource {i}: "))

    for i in range(num_processes):
        print(f"Process {i} maximum claim for each resource:")
        for j in range(num_res):
            max_claim[i][j] = int(input(f"Resource {j}: "))

        # Initialize the need matrix
        need[i] = max_claim[i] - allocation[i]

# Function to check if a request can be granted
def check_request(process, request):
    global num_res, resources, max_claim, allocation, need

    # Check if the request is within bounds
    if any(request > need[process]) or any(request > resources):
        return False

    # Try allocating resources temporarily and check for safety
    temp_allocation = allocation.copy()
    temp_need = need.copy()
    temp_resources = resources.copy()

    temp_allocation[process] += request
    temp_need[process] = max_claim[process] - temp_allocation[process]
    temp_resources -= request

    # Safety check using Banker's algorithm
    finish = [False] * num_processes
    work = temp_resources.copy()

    while True:
        for i in range(num_processes):
            if not finish[i] and all(temp_need[i] <= work):
                work += temp_allocation[i]
                finish[i] = True

        if all(finish):
            return True

        if not any(finish):
            return False

# Function to handle resource requests
def request_resources(process, request):
    global num_res, resources, max_claim, allocation, need

    if check_request(process, request):
        resources -= request
        allocation[process] += request
        need[process] -= request
        print("Request granted.")
        return True
    else:
        print("Request denied. Granting this request may lead to an unsafe state.")
        return False

# Function to handle resource releases
def release_resources(process, release):
    global num_res, resources, max_claim, allocation, need

    if all(release <= allocation[process]):
        resources += release
        allocation[process] -= release
        need[process] += release
        print("Resources released.")
        return True
    else:
        print("Release denied. The process does not own these resources.")
        return False

# Main program
if __name__ == "__main__":
    num_processes = int(input("Enter the number of processes: "))
    num_resources = int(input("Enter the number of resources: "))

    initialize_system(num_processes, num_resources)

    while True:
        print("\nCommands: request(i, j, k) or release(i, j, k) or exit")
        command = input("Enter a command: ")

        if command == "exit":
            break

        try:
            cmd, process, res, units = command.split()
            process, res, units = int(process), int(res), int(units)

            if cmd == "request":
                request_resources(process, np.array([units]))
            elif cmd == "release":
                release_resources(process, np.array([units]))
            else:
                print("Invalid command. Use 'request' or 'release'.")
        except ValueError:
            print("Invalid command format. Use 'request(i, j, k)' or 'release(i, j, k)'.")
