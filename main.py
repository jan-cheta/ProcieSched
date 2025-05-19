from scheduler import Process, RoundRobinScheduler, PriorityScheduler
import pandas as pd

def main():
    
    # sample process data (process_id, arrival_time, burst_time)
    process_list = [
        (1, 0, 5, 2),   # Process 1: arrives at time 0, needs 5 units of burst time
        (2, 1, 3, 1),   # Process 2: arrives at time 1, needs 3 units of burst time
        (3, 2, 8, 0),   # Process 3: arrives at time 2, needs 8 units of burst time
        (4, 3, 6, 10),   # Process 4: arrives at time 3, needs 6 units of burst time
        (5, 4, 4, 5),   # Process 5: arrives at time 4, needs 4 units of burst time
    ]
    
    # Time quanta for Round Robin scheduling (e.g., 4 units)
    time_quanta = 4
    
    # Sample function call with extended process list
    # result_df = post_request_sample_roundrobin(process_list=process_list, time_quanta=time_quanta)

    # result_df = post_request_sample_priority(process_list=process_list, is_preemptive=False)
    
    # Print the result
    # print(result_df['attr'])
    # print(result_df['gantt'])

def post_request_sample_roundrobin(**kargs):
    process_list = kargs.get("process_list", [])
    time_quanta = kargs.get("time_quanta", None)
    
    p_list = []
    for process in process_list:
        p_list.append(Process(process_id=process[0], arrival_time=process[1], burst_time=process[2]))
    
    scheduler = RoundRobinScheduler(p_list, time_quanta)
    
    return scheduler.get_dataframe()

def post_request_sample_priority(**kargs):
    process_list = kargs.get("process_list", [])
    is_preemptive = kargs.get("is_preemptive", None)
    
    p_list = []
    for process in process_list:
        p_list.append(Process(process_id=process[0], arrival_time=process[1], burst_time=process[2], priority=process[3]))
    
    scheduler = PriorityScheduler(p_list, is_preemptive)
    
    return scheduler.get_dataframe()

if __name__ == "__main__":
    main()



    
