from scheduler import Process, RoundRobinScheduler
import pandas as pd

def main():
    
    # sample process data (process_id, arrival_time, burst_time)
    process_list = [
        (1, 0, 5),   # Process 1: arrives at time 0, needs 5 units of burst time
        (2, 1, 3),   # Process 2: arrives at time 1, needs 3 units of burst time
        (3, 2, 8),   # Process 3: arrives at time 2, needs 8 units of burst time
        (4, 3, 6),   # Process 4: arrives at time 3, needs 6 units of burst time
        (5, 4, 4),   # Process 5: arrives at time 4, needs 4 units of burst time
        (6, 5, 7),   # Process 6: arrives at time 5, needs 7 units of burst time
        (7, 6, 2),   # Process 7: arrives at time 6, needs 2 units of burst time
        (8, 7, 9),   # Process 8: arrives at time 7, needs 9 units of burst time
        (9, 8, 5),   # Process 9: arrives at time 8, needs 5 units of burst time
        (10, 9, 4),  # Process 10: arrives at time 9, needs 4 units of burst time
    ]
    
    # Time quanta for Round Robin scheduling (e.g., 4 units)
    time_quanta = 4
    
    # Sample function call with extended process list
    result_df = post_request_sample(process_list=process_list, time_quanta=time_quanta)
    
    # Print the result
    print(result_df['attr'])
    print(result_df['gantt'])

def post_request_sample(**kargs):
    process_list = kargs.get("process_list", [])
    time_quanta = kargs.get("time_quanta", None)
    
    p_list = []
    for process in process_list:
        p_list.append(Process(process_id=process[0], arrival_time=process[1], burst_time=process[2]))
    
    scheduler = RoundRobinScheduler(p_list, time_quanta)
    
    return scheduler.get_dataframe()

if __name__ == "__main__":
    main()



    
