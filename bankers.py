
import numpy as np
import json

class BankersProcess:
    def __init__(self, name, max, alloc, need):
        self.name = name
        self.max = np.array(max)
        self.alloc = np.array(alloc)
        self.need = np.array(need)

        if not max:
            self.max = self.alloc + self.need
        elif not alloc:
            self.alloc = self.max - self.need
        else:
            self.need = self.max - self.alloc
    
    def to_dict(self):
        return {
            "name": self.name,
            "max": self.max.tolist(),
            "alloc": self.alloc.tolist(),
            "need": self.need.tolist()
        }



class BankersAlgorithm:
    def __init__(self, process_list, total_avail):
        self.process_list = process_list
        self.total_avail = np.array(total_avail)
        self.avail_list = [self.total_avail.tolist()]
        self.safe_sequence = []
        self.safe = False

    def bankers(self):
        list_len = len(self.process_list)

        for i in range(list_len):
            for process in self.process_list:
                if not process in self.safe_sequence and all(process.need <= self.total_avail):
                    self.total_avail += process.alloc
                    self.avail_list.append(self.total_avail.tolist())
                    self.safe_sequence.append(process)
        
        if len(self.process_list) == len(self.safe_sequence):
            self.safe = True
        
        return json.dumps({
            'process_list': [p.to_dict() for p in self.process_list],
            'avail_list': self.avail_list,
            'safe_sequence': [p.name for p in self.safe_sequence],
            'is_safe': self.safe
        }, indent=2)

        
if __name__ == '__main__':
    processes = [
            BankersProcess("P0", [7, 5, 3], [0, 1, 0], None),
            BankersProcess("P1", [3, 2, 2], [2, 0, 0], None),
            BankersProcess("P2", [9, 0, 2], [3, 0, 2], None),
            BankersProcess("P3", [2, 2, 2], [2, 1, 1], None),
            BankersProcess("P4", [4, 3, 3], [0, 0, 2], None)
        ]

    total_available = [3, 3, 2]

    ba = BankersAlgorithm(processes, total_available)
    print(ba.bankers())
            
