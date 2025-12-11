# banker’s algorithm implementation

def bankers_algorithm(processes, resources, allocation, maximum, available):
    need = [[maximum[i][j] - allocation[i][j] for j in range(resources)] for i in range(processes)]  # calculate needed resources

    finish = [False] * processes  # tracks which processes are done
    safe_sequence = []  # stores safe order
    work = available.copy()  # work holds temporary available resources

    while len(safe_sequence) < processes:
        executed = False  # checks if at least one process ran this loop

        for i in range(processes):
            # check if process can run with current available resources
            if not finish[i] and all(need[i][j] <= work[j] for j in range(resources)):
                work = [work[j] + allocation[i][j] for j in range(resources)]  # simulate releasing resources after completion
                finish[i] = True  # mark process as finished
                safe_sequence.append(i)  # add to safe sequence
                executed = True  # mark that progress was made
                break  

        if not executed:
            return False, []  # no process can run → unsafe state

    return True, safe_sequence  # return safe state and order


# main
print("=== Banker's Algorithm ===")

p = int(input("Enter number of processes: "))
r = int(input("Enter number of resources: "))

allocation = []
print("\nEnter Allocation Matrix:")
for i in range(p):
    row = list(map(int, input(f"Allocation for P{i}: ").split()))
    allocation.append(row)

maximum = []
print("\nEnter Maximum Matrix:")
for i in range(p):
    row = list(map(int, input(f"Maximum for P{i}: ").split()))
    maximum.append(row)

available = list(map(int, input("\nEnter Available Resources: ").split()))

safe, sequence = bankers_algorithm(p, r, allocation, maximum, available)

if safe:
    print("\nSystem is in a SAFE state.")
    print("Safe Sequence:", " → ".join([f"P{num}" for num in sequence]))
else:
    print("\nSystem is in an UNSAFE state.")
