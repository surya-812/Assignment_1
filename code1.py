from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self):
        self.tasks = {}
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.duration = {}
    
    def add_task(self, task_id, duration):
        self.tasks[task_id] = task_id
        self.duration[task_id] = duration
        self.in_degree[task_id] = 0
    
    def add_dependency(self, task_from, task_to):
        self.graph[task_from].append(task_to)
        self.in_degree[task_to] += 1
    
    def calculate_times(self):
        EST = {task: 0 for task in self.tasks}
        EFT = {task: 0 for task in self.tasks}
        LFT = {task: float('inf') for task in self.tasks}
        LST = {task: float('inf') for task in self.tasks}
        
        # Topological sort
        zero_in_degree = deque([task for task in self.tasks if self.in_degree[task] == 0])
        topo_order = []
        
        while zero_in_degree:
            current = zero_in_degree.popleft()
            topo_order.append(current)
            
            for neighbor in self.graph[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)
        
        # Calculate EST and EFT
        for task in topo_order:
            EFT[task] = EST[task] + self.duration[task]
            for neighbor in self.graph[task]:
                EST[neighbor] = max(EST[neighbor], EFT[task])
        
        # Assume project completion time is max EFT
        project_completion_time = max(EFT.values())
        
        # Calculate LFT and LST
        for task in topo_order:
            LFT[task] = project_completion_time
        
        for task in reversed(topo_order):
            LFT[task] = min(LFT[task], project_completion_time)
            LST[task] = LFT[task] - self.duration[task]
            for neighbor in self.graph[task]:
                LFT[task] = min(LFT[task], LST[neighbor])
        
        earliest_completion = max(EFT.values())
        latest_completion = max(LFT.values())
        
        return earliest_completion, latest_completion

# Example Usage
scheduler = TaskScheduler()
scheduler.add_task('T1', 3)
scheduler.add_task('T2', 2)
scheduler.add_task('T3', 1)
scheduler.add_task('T4', 2)

scheduler.add_dependency('T1', 'T2')
scheduler.add_dependency('T1', 'T3')
scheduler.add_dependency('T2', 'T4')
scheduler.add_dependency('T3', 'T4')

earliest, latest = scheduler.calculate_times()
print(f"Earliest completion time: {earliest}")
print(f"Latest completion time: {latest}")
