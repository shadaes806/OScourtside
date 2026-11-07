import tkinter as tk
from tkinter import ttk

#main window

root = tk.Tk()
root.title("Courtside OS | CPU scheduling simulator")
root.geometry("1100x850")
root.configure(bg="#F4F1EA")

#Header
title = tk.Label(root, text="A basketball themed CPU scheduling simulator", font=("Arial", 12), bg="#F4F1EA", fg="#C65322")
title.pack(pady=(20,5))


section_title = tk.Label(root,text="BASKETBALL PROCESSES",font=("Arial", 15, "bold"),bg="#F4F1EA",fg="#222222")
section_title.pack(pady=5)

columns = ( "Process ID","Basketball Action","Arrival Time","Burst Time", "Priority","State")

process_table = ttk.Treeview(root,  columns=columns,  show="headings", height=5)
# Set the heading and width of each column
for column in columns:
    process_table.heading("Priority", text="Priority")
    process_table.column("Priority", width=80, anchor="center")
    process_table.heading(column, text=column)
    process_table.column(column, width=160, anchor="center")

process_table.pack(padx=25, pady=10, fill="x")


# 5. Add sample processes

# Store processes that the user adds
processes = []
process_priorities = {}
next_process_id = 1

# Input section
input_frame = tk.Frame(root, bg="#F4F1EA")
input_frame.pack(pady=10)

# Basketball action dropdown
tk.Label(
    input_frame,
    text="Basketball Action:",
    bg="#F4F1EA"
).grid(row=0, column=0, padx=5, pady=5)

action_choice = ttk.Combobox(
    input_frame,
    values=["Passing", "Shooting", "Defending",
            "Rebounding", "Stealing", "Blocking"],
    state="readonly",
    width=15
)
action_choice.grid(row=0, column=1, padx=5, pady=5)
action_choice.set("Passing")

# Arrival time
tk.Label(
    input_frame,
    text="Arrival Time:",
    bg="#F4F1EA"
).grid(row=0, column=2, padx=5, pady=5)

arrival_entry = tk.Entry(input_frame, width=8)
arrival_entry.grid(row=0, column=3, padx=5, pady=5)
arrival_entry.insert(0, "0")

# Burst time
tk.Label(
    input_frame,
    text="Burst Time:",
    bg="#F4F1EA"
).grid(row=1, column=0, padx=5, pady=5)

burst_entry = tk.Entry(input_frame, width=8)
burst_entry.grid(row=1, column=1, padx=5, pady=5)
burst_entry.insert(0, "3")

# Priority
tk.Label(
    input_frame,
    text="Priority:",
    bg="#F4F1EA"
).grid(row=1, column=2, padx=5, pady=5)

priority_entry = tk.Entry(input_frame, width=8)
priority_entry.grid(row=1, column=3, padx=5, pady=5)
priority_entry.insert(0, "1")



# Message displayed to the user
message_label = tk.Label(
    root,
    text="Add a basketball process to get started.",
    bg="#F4F1EA",
    fg="#333333"
)
message_label.pack(pady=5)

# Function to add a process
def add_process():
    global next_process_id

    action = action_choice.get()

    try:
        arrival_time = int(arrival_entry.get())
        burst_time = int(burst_entry.get())
        priority = int(priority_entry.get())

    except ValueError:
        message_label.config(
            text="Please enter whole numbers for the times and priority.",
            fg="red"
        )
        return

    if arrival_time < 0 or burst_time <= 0 or priority <= 0:
        message_label.config(
            text="Arrival must be 0 or greater. Burst and priority must be greater than 0.",
            fg="red"
        )
        return

    process_id = f"P{next_process_id}"

    process = (
        process_id,
        action,
        arrival_time,
        burst_time,
        "Ready"
    )

    processes.append(process)
    process_priorities[process_id] = priority

    process_table.insert(
        "",
        "end",
        values=(
            process_id,
            action,
            arrival_time,
            burst_time,
            priority,
            "Ready"
        )
    )

    next_process_id += 1

    message_label.config(
        text=f"{process_id} ({action}) added successfully!",
        fg="green"
    )

    arrival_entry.delete(0, tk.END)
    arrival_entry.insert(0, "0")

    burst_entry.delete(0, tk.END)
    burst_entry.insert(0, "3")

    priority_entry.delete(0, tk.END)
    priority_entry.insert(0, "1")


# Add Process button
add_button = tk.Button(
    root,
    text="Add Process +",
    command=add_process,
    bg="#C65322",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=5
)

add_button.pack(pady=5)

# -----------------------------
# FCFS Results Section
# -----------------------------

results_title = tk.Label(
    root,
    text="CPU SCHEDULING RESULTS",
    font=("Arial", 15, "bold"),
    bg="#F4F1EA",
    fg="#222222"
)
results_title.pack(pady=10)

result_columns = (
    "Process ID",
    "Action",
    "Arrival",
    "Burst",
    "Start",
    "Completion",
    "Waiting",
    "Turnaround"
)

result_table = ttk.Treeview(
    root,
    columns=result_columns,
    show="headings",
    height=5
)

for column in result_columns:
    result_table.heading(column, text=column)
    result_table.column(column, width=105, anchor="center")

result_table.pack(padx=15, pady=5, fill="x")



# -----------------------------
# FCFS Scheduling Algorithm
# -----------------------------

def run_fcfs():

    # Check whether processes have been added
    if len(processes) == 0:
        message_label.config(
            text="Please add some processes first!",
            fg="red"
        )
        return

    # Clear previous results
    for item in result_table.get_children():
        result_table.delete(item)

    # Sort processes by arrival time
    sorted_processes = sorted(
        processes,
        key=lambda process: process[2]
    )

    current_time = 0

    total_waiting = 0
    total_turnaround = 0

    # Process each basketball action
    for process in sorted_processes:

        process_id = process[0]
        action = process[1]
        arrival_time = process[2]
        burst_time = process[3]

        # Determine when the process starts
        start_time = max(current_time, arrival_time)

        # Determine when the process finishes
        completion_time = start_time + burst_time

        # Calculate waiting and turnaround time
        waiting_time = start_time - arrival_time
        turnaround_time = completion_time - arrival_time

        # Add results to the table
        result_table.insert(
            "",
            "end",
            values=(
                process_id,
                action,
                arrival_time,
                burst_time,
                start_time,
                completion_time,
                waiting_time,
                turnaround_time
            )
        )

        total_waiting += waiting_time
        total_turnaround += turnaround_time

        # Update the CPU's current time
        current_time = completion_time

    # Calculate averages
    average_waiting = total_waiting / len(processes)
    average_turnaround = total_turnaround / len(processes)

    message_label.config(
        text=(
            f"FCFS completed! Average Waiting Time: "
            f"{average_waiting:.2f} | Average Turnaround Time: "
            f"{average_turnaround:.2f}"
        ),
        fg="green"
    )




# -----------------------------
# SJF Scheduling Algorithm
# -----------------------------

def run_sjf():

    # Check whether processes have been added
    if len(processes) == 0:
        message_label.config(
            text="Please add some processes first!",
            fg="red"
        )
        return

    # Clear previous results
    for item in result_table.get_children():
        result_table.delete(item)

    # Make a copy of the processes
    remaining_processes = processes.copy()

    current_time = 0

    total_waiting = 0
    total_turnaround = 0

    # Continue until every process has run
    while remaining_processes:

        # Find processes that have arrived
        available_processes = [
            process for process in remaining_processes
            if process[2] <= current_time
        ]

        # If no process is available, move time forward
        if not available_processes:
            current_time = min(
                process[2] for process in remaining_processes
            )

            available_processes = [
                process for process in remaining_processes
                if process[2] <= current_time
            ]

        # Choose the available process with the shortest burst
        selected_process = min(
            available_processes,
            key=lambda process: (
                process[3],
                process[2],
                processes.index(process)
            )
        )

        # Get process information
        process_id = selected_process[0]
        action = selected_process[1]
        arrival_time = selected_process[2]
        burst_time = selected_process[3]

        # Calculate scheduling times
        start_time = current_time
        completion_time = start_time + burst_time

        waiting_time = start_time - arrival_time
        turnaround_time = completion_time - arrival_time

        # Display the results
        result_table.insert(
            "",
            "end",
            values=(
                process_id,
                action,
                arrival_time,
                burst_time,
                start_time,
                completion_time,
                waiting_time,
                turnaround_time
            )
        )

        # Update totals
        total_waiting += waiting_time
        total_turnaround += turnaround_time

        # Move CPU time forward
        current_time = completion_time

        # Remove the completed process
        remaining_processes.remove(selected_process)

    # Calculate averages
    average_waiting = total_waiting / len(processes)
    average_turnaround = total_turnaround / len(processes)

    message_label.config(
        text=(
            f"SJF completed! Average Waiting Time: "
            f"{average_waiting:.2f} | Average Turnaround Time: "
            f"{average_turnaround:.2f}"
        ),
        fg="green"
    )


def run_round_robin():

    # Check whether processes have been added
    if len(processes) == 0:
        message_label.config(
            text="Please add some processes first!",
            fg="red"
        )
        return

    # Get the time quantum
    try:
        quantum = int(quantum_entry.get())

        if quantum <= 0:
            message_label.config(
                text="Time quantum must be greater than 0!",
                fg="red"
            )
            return

    except ValueError:
        message_label.config(
            text="Please enter a valid time quantum!",
            fg="red"
        )
        return

    # Clear previous results
    for item in result_table.get_children():
        result_table.delete(item)

    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda p: p[2])

    # Track remaining burst time for each process
    remaining_times = {
        process[0]: process[3] for process in sorted_processes
    }

    # Store process information
    process_info = {
        process[0]: process for process in sorted_processes
    }

    first_start_times = {}
    completion_times = {}

    ready_queue = []
    current_time = 0
    next_process = 0

    # Continue until all processes finish
    while next_process < len(sorted_processes) or ready_queue:

        # Add processes that have arrived
        while (
            next_process < len(sorted_processes)
            and sorted_processes[next_process][2] <= current_time
        ):
            ready_queue.append(
                sorted_processes[next_process][0]
            )
            next_process += 1

        # If nobody is ready, move time forward
        if not ready_queue:
            current_time = sorted_processes[next_process][2]
            continue

        # Select the first process in the queue
        process_id = ready_queue.pop(0)
        process = process_info[process_id]

        # Record the first time the process starts
        if process_id not in first_start_times:
            first_start_times[process_id] = current_time

        # Run the process for the quantum or remaining time
        run_time = min(quantum, remaining_times[process_id])

        current_time += run_time
        remaining_times[process_id] -= run_time

        # Add newly arrived processes to the queue
        while (
            next_process < len(sorted_processes)
            and sorted_processes[next_process][2] <= current_time
        ):
            ready_queue.append(
                sorted_processes[next_process][0]
            )
            next_process += 1

        # Check whether the process is finished
        if remaining_times[process_id] > 0:
            ready_queue.append(process_id)
        else:
            completion_times[process_id] = current_time

    # Calculate and display results
    total_waiting = 0
    total_turnaround = 0

    for process in sorted_processes:
        process_id, action, arrival, burst, state = process

        start = first_start_times[process_id]
        completion = completion_times[process_id]

        turnaround = completion - arrival
        waiting = turnaround - burst

        total_waiting += waiting
        total_turnaround += turnaround

        result_table.insert(
            "",
            "end",
            values=(
                process_id,
                action,
                arrival,
                burst,
                start,
                completion,
                waiting,
                turnaround
            )
        )

    # Calculate averages
    average_waiting = total_waiting / len(processes)
    average_turnaround = total_turnaround / len(processes)

    message_label.config(
        text=(
            f"Round Robin Complete! "
            f"Average Waiting Time: {average_waiting:.2f} | "
            f"Average Turnaround Time: {average_turnaround:.2f}"
        ),
        fg="green"
    )


# -----------------------------
# Round Robin Time Quantum
# -----------------------------

quantum_frame = tk.Frame(root, bg="#F4F1EA")
quantum_frame.pack(pady=10)

quantum_label = tk.Label(
    quantum_frame,
    text="Time Quantum:",
    bg="#F4F1EA",
    font=("Arial", 11, "bold")
)
quantum_label.grid(row=0, column=0, padx=5)

quantum_entry = tk.Entry(
    quantum_frame,
    width=8,
    font=("Arial", 11)
)
quantum_entry.grid(row=0, column=1, padx=5)

quantum_entry.insert(0, "2")

# -----------------------------
# Scheduling Algorithm Buttons
# -----------------------------

button_frame = tk.Frame(root, bg="#F4F1EA")
button_frame.pack(pady=15)

# FCFS Button
fcfs_button = tk.Button(
    button_frame,
    text="Run FCFS",
    command=run_fcfs,
    bg="#3876A8",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=10
)
fcfs_button.grid(row=0, column=0, padx=10)

# SJF Button
sjf_button = tk.Button(
    button_frame,
    text="Run SJF",
    command=run_sjf,
    bg="#398568",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=10
)
sjf_button.grid(row=0, column=1, padx=10)

# Round Robin Button
rr_button = tk.Button(
    button_frame,
    text="Run Round Robin",
    command=run_round_robin,
    bg="#D97932",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=10
)
rr_button.grid(row=0, column=2, padx=10)
# -----------------------------
# 6. Add an explanation
# -----------------------------
explanation = tk.Label(
    root,
    text="Arrival Time = when a process becomes available\n"
         "Burst Time = how much CPU time a process needs",
    font=("Arial", 10),
    bg="#F4F1EA",
    fg="#444444",
    justify="left"
)
explanation.pack(pady=15)

root.mainloop()

