#fcfs + round robin
def fcfs(processes):
    print("\n=== FCFS Scheduling ===")

    processes.sort(key=lambda x: x["arrival"])  # sort by arrival
    time = 0
    gantt = []
    waiting = []
    turnaround = []

    for p in processes:
        if time < p["arrival"]:
            time = p["arrival"]

        start = time
        finish = start + p["burst"]

        gantt.append((p["pid"], start, finish))

        wt = start - p["arrival"]
        tat = finish - p["arrival"]

        waiting.append(wt)
        turnaround.append(tat)

        time = finish

    # display Gantt Chart
    print("\nGantt Chart:")
    for g in gantt:
        print(f"| P{g[0]} ({g[1]} → {g[2]}) ", end="")
    print("|")

    print(f"\nAverage Waiting Time: {sum(waiting)/len(waiting):.2f}")
    print(f"Average Turnaround Time: {sum(turnaround)/len(turnaround):.2f}")


#round robin
def round_robin(processes, quantum):
    print("\n=== Round Robin Scheduling ===")

    # sort by arrival time
    processes.sort(key=lambda x: x["arrival"])

    # copy burst times
    remaining = {p["pid"]: p["burst"] for p in processes}

    time = 0
    gantt = []
    queue = []
    waiting = {p["pid"]: 0 for p in processes}
    last_exec = {p["pid"]: 0 for p in processes}

    i = 0  # process index

    while True:
        # add processes that have arrived
        while i < len(processes) and processes[i]["arrival"] <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            # if queue empty but processes remain, jump to next arrival
            if i < len(processes):
                time = processes[i]["arrival"]
                queue.append(processes[i])
                i += 1
            else:
                break

        current = queue.pop(0)
        pid = current["pid"]

        exec_time = min(quantum, remaining[pid])
        start = time
        end = start + exec_time
        gantt.append((pid, start, end))

        # update waiting time
        waiting[pid] += start - last_exec[pid] - (0 if last_exec[pid] == 0 else 0)
        last_exec[pid] = end

        remaining[pid] -= exec_time
        time = end

        # re-queue if still not finished
        if remaining[pid] > 0:
            # Add newly arrived processes during execution
            while i < len(processes) and processes[i]["arrival"] <= time:
                queue.append(processes[i])
                i += 1
            queue.append(current)

    # compute turnaround & waiting time
    tat_list = []
    wt_list = []

    for p in processes:
        turnaround = last_exec[p["pid"]] - p["arrival"]
        tat_list.append(turnaround)
        waiting_time = turnaround - p["burst"]
        wt_list.append(waiting_time)

    # Print Gantt Chart
    print("\nGantt Chart:")
    for g in gantt:
        print(f"| P{g[0]} ({g[1]} → {g[2]}) ", end="")
    print("|")

    print(f"\nAverage Waiting Time: {sum(wt_list)/len(wt_list):.2f}")
    print(f"Average Turnaround Time: {sum(tat_list)/len(tat_list):.2f}")


# main
processes = []
n = int(input("Enter number of processes: "))

for i in range(n):
    arrival = int(input(f"Arrival time of P{i+1}: "))
    burst = int(input(f"Burst time of P{i+1}: "))
    processes.append({"pid": i+1, "arrival": arrival, "burst": burst})

print("\nChoose scheduling algorithm:")
print("1 - FCFS (Non-preemptive)")
print("2 - Round Robin (Preemptive)")

choice = int(input("Enter choice: "))

if choice == 1:
    fcfs(processes)
elif choice == 2:
    quantum = int(input("Enter Time Quantum: "))
    round_robin(processes, quantum)
else:
    print("Invalid choice.")
