import pandas as pd

class Process:
    def __init__(self, process_id ,arrival_time, burst_time, priority=None):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.completion_time = None
        self.start_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.response_time = None
        self.time_segments = []
        
    def __repr__(self) -> str:
        return (
            f"Process("
            f"id={self.process_id}, "
            f"arrival={self.arrival_time}, "
            f"burst={self.burst_time}, "
            f"remaining={self.remaining_time}, "
            f"completion={self.completion_time}, "
            f"start={self.start_time}, "
            f"turnaround={self.turnaround_time}, "
            f"waiting={self.waiting_time}, "
            f"response={self.response_time}, "
            f"segments={self.time_segments}"
            f")"
        )



class RoundRobinScheduler:
    def __init__(self, process_list: list[Process], time_quantum):
        self.process_list = sorted(process_list, key=lambda process: process.arrival_time)
        self.time_quantum = time_quantum
        self.ready_queue = []
        self.terminated_queue = []
        self.waiting_queue = []
        self.time = 0
    
    def _schedule(self):
        
        while len(self.terminated_queue) < len(self.process_list):
            for process in self.process_list:
                if process.arrival_time <= self.time and process not in self.ready_queue and process not in self.waiting_queue and process not in self.terminated_queue:
                    self.ready_queue.append(process)
            
            self.ready_queue.extend(self.waiting_queue)
            self.waiting_queue.clear()
        
            if self.ready_queue:
                process = self.ready_queue.pop(0)
                
                if process.start_time == None:
                    process.start_time = self.time
                
                increment = min(process.remaining_time, self.time_quantum)
                segment = [self.time, self.time + increment]
                process.time_segments.append(segment)
                process.remaining_time -= increment
                self.time += increment
                
                if process.remaining_time:
                    self.waiting_queue.append(process)
                else:
                    process.completion_time = self.time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    process.response_time = process.start_time - process.arrival_time
                    self.terminated_queue.append(process)
            else:
                self.time += 1
                
        return sorted(self.terminated_queue, key=lambda process: process.process_id)
        
    def get_dataframe(self):
        data = self._schedule()
        return create_process_dataframes(data)

class PriorityScheduler:
    def __init__(self, process_list: list[Process], is_preemptive: bool):
        self.process_list = sorted(process_list, key=lambda process: process.arrival_time)
        self.is_preemptive = is_preemptive
        self.ready_queue = []
        self.terminated_queue = []
        self.waiting_queue = []
        self.time = 0
    
    def _preemptive(self):
        while len(self.terminated_queue) < len(self.process_list):
            for process in self.process_list:
                if process.arrival_time <= self.time and process not in self.ready_queue and process not in self.waiting_queue and process not in self.terminated_queue:
                    self.ready_queue.append(process)
            
            self.ready_queue.extend(self.waiting_queue)
            self.waiting_queue.clear()
            self.ready_queue = sorted(self.ready_queue, key=lambda process: process.priority)

            if self.ready_queue:
                process = self.ready_queue.pop(0)
                
                if process.start_time == None:
                    process.start_time = self.time
                

                if process.time_segments and process.time_segments[-1][1] == self.time:
                    time_segment = [process.time_segments[-1][0], self.time + 1]
                    process.time_segments[-1] = time_segment
                else:
                    time_segment = [self.time, self.time + 1]
                    process.time_segments.append(time_segment)
                
                process.remaining_time -= 1
                self.time += 1
                
                if process.remaining_time:
                    self.waiting_queue.append(process)
                else:
                    process.completion_time = self.time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    process.response_time = process.start_time - process.arrival_time
                    self.terminated_queue.append(process)
            else:
                self.time += 1
                
        return sorted(self.terminated_queue, key=lambda process: process.process_id)
    
    def _non_preemptive(self):
        while len(self.terminated_queue) < len(self.process_list):
            for process in self.process_list:
                if process.arrival_time <= self.time and process not in self.ready_queue and process not in self.waiting_queue and process not in self.terminated_queue:
                    self.ready_queue.append(process)
            
            self.ready_queue.extend(self.waiting_queue)
            self.waiting_queue.clear()
            self.ready_queue = sorted(self.ready_queue, key=lambda process: process.priority)

            if self.ready_queue:
                process = self.ready_queue.pop(0)
                
                if process.start_time == None:
                    process.start_time = self.time
                

                time_segment = [self.time, self.time + process.remaining_time]
                process.time_segments.append(time_segment)
                
                self.time += process.remaining_time
                process.remaining_time = 0

                
                if process.remaining_time:
                    self.waiting_queue.append(process)
                else:
                    process.completion_time = self.time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                    process.response_time = process.start_time - process.arrival_time
                    self.terminated_queue.append(process)
            else:
                self.time += 1
                
        return sorted(self.terminated_queue, key=lambda process: process.process_id)
    
    def get_dataframe(self):
        if self.is_preemptive:
            data = self._preemptive()
        else:
            data = self._non_preemptive()

        return create_process_dataframes(data)


        
        

def create_process_dataframes(process_list):
    """
    Creates two DataFrames:
    1. Process attributes (metrics like CT, TAT, WT)
    2. Gantt chart segments (time intervals for visualization)
    
    Args:
        process_list: List of Process objects
        
    Returns:
        (attributes_df, gantt_df) tuple of DataFrames
    """
    # DataFrame 1: Process Attributes
    attributes_data = []
    for p in process_list:
        attributes_data.append({
            'Process': p.process_id,
            'Arrival': p.arrival_time,
            'Burst': p.burst_time,
            'Priority': p.priority,
            'Start': p.start_time,
            'Completion': p.completion_time,
            'Turnaround': p.turnaround_time,
            'Waiting': p.waiting_time,
            'Response': p.response_time
        })
    attributes_df = pd.DataFrame(attributes_data)
    
    # DataFrame 2: Gantt Chart Segments
    gantt_data = []
    for p in process_list:
        for start, end in p.time_segments:
            gantt_data.append({
                'Process': p.process_id,
                'Start': start,
                'End': end,
                'Duration': end - start
            })
    gantt_df = pd.DataFrame(gantt_data).sort_values('Start')
    
    return {'attr': attributes_df, 'gantt': gantt_df}