from scheduler import Process, RoundRobinScheduler
import pandas as pd

def main():
    
    process_list = [
        Process(process_id=1, arrival_time=0, burst_time=5),
        Process(process_id=2, arrival_time=1, burst_time=3),
        Process(process_id=3, arrival_time=2, burst_time=8),
        Process(process_id=4, arrival_time=3, burst_time=6),
        Process(process_id=5, arrival_time=4, burst_time=4),
    ]
    
    scheduler = RoundRobinScheduler(process_list, 3)
    result = scheduler.get_dataframe()
    
    print(result['attr'])
    print(result['gantt'])

if __name__ == "__main__":
    main()



    
