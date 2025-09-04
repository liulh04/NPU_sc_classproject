import numpy as np
import random
from datetime import datetime, timedelta
from collections import defaultdict

# 分时电价时段定义（从7:00开始，单位：分钟）
time_slots = [
    {'start': 0,    'end': 180,  'price': 0.7181, 'type': '平峰'},    # 7:00-10:00
    {'start': 180,  'end': 240,  'price': 1.2238, 'type': '高峰'},    # 10:00-11:00
    {'start': 240,  'end': 360,  'price': 1.3472, 'type': '尖峰'},    # 11:00-13:00
    {'start': 360,  'end': 480,  'price': 1.2238, 'type': '高峰'},    # 13:00-15:00
    {'start': 480,  'end': 540,  'price': 0.7181, 'type': '平峰'},    # 15:00-16:00
    {'start': 540,  'end': 600,  'price': 1.3472, 'type': '尖峰'},    # 16:00-17:00
    {'start': 600,  'end': 660,  'price': 0.7181, 'type': '平峰'},    # 17:00-18:00
    {'start': 660,  'end': 840,  'price': 1.2238, 'type': '高峰'},    # 18:00-21:00
    {'start': 840,  'end': 960,  'price': 0.7181, 'type': '平峰'},    # 21:00-23:00
    {'start': 960,  'end': 1440, 'price': 0.2417, 'type': '低谷'}     # 23:00-7:00
]

# 机器能耗 (kWh/min)
r = [10, 6, 8]

# 加工时间 (分钟)
processing_time = [
    [20, 32, 14],  # 工件1
    [33, 34, 20],  # 工件2
    [45, 14, 30],  # 工件3
    [63, 22, 16],  # 工件4
    [38, 15, 35]   # 工件5
]

n_jobs = len(processing_time)
n_machines = len(processing_time[0])

class GeneticAlgorithm:
    def __init__(self, pop_size=50, max_gen=200):
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.population = []
        
    def initialize_population(self):
        # 生成随机排列作为初始种群
        self.population = [random.sample(range(1, n_jobs+1), n_jobs) for _ in range(self.pop_size)]
    
    def evaluate(self, sequence):
        # 评估单个序列的总成本
        scheduler = Scheduler(sequence)
        scheduler.generate_schedule()
        cost, _ = scheduler.calculate_cost()
        return cost
    
    def selection(self):
        # 轮盘赌选择
        costs = np.array([self.evaluate(ind) for ind in self.population])
        fitness = 1 / (costs + 1e-6)  # 最小化问题取倒数
        selected_idx = np.random.choice(
            len(self.population), 
            size=self.pop_size, 
            p=fitness/fitness.sum()
        )
        return [self.population[i] for i in selected_idx]
    
    def crossover(self, parent1, parent2):
        # 顺序交叉(OX)
        size = len(parent1)
        cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
        
        child1 = [None] * size
        child2 = [None] * size
        
        # 复制中间段
        child1[cxpoint1:cxpoint2+1] = parent1[cxpoint1:cxpoint2+1]
        child2[cxpoint1:cxpoint2+1] = parent2[cxpoint1:cxpoint2+1]
        
        # 填充剩余部分
        ptr1 = (cxpoint2 + 1) % size
        ptr2 = (cxpoint2 + 1) % size
        
        for i in range(size):
            current_pos = (cxpoint2 + 1 + i) % size
            if parent2[current_pos] not in child1:
                child1[ptr1] = parent2[current_pos]
                ptr1 = (ptr1 + 1) % size
            
            if parent1[current_pos] not in child2:
                child2[ptr2] = parent1[current_pos]
                ptr2 = (ptr2 + 1) % size
        
        return child1, child2
    
    def mutation(self, individual):
        # 交换变异
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual
    
    def run(self):
        self.initialize_population()
        best_sequence = None
        best_cost = float('inf')
        
        for gen in range(self.max_gen):
            # 评估
            costs = [self.evaluate(ind) for ind in self.population]
            min_cost = min(costs)
            if min_cost < best_cost:
                best_cost = min_cost
                best_sequence = self.population[costs.index(min_cost)]
            
            # 选择
            selected = self.selection()
            
            # 交叉
            offspring = []
            for i in range(0, len(selected), 2):
                if i+1 < len(selected) and random.random() < 0.8:
                    child1, child2 = self.crossover(selected[i], selected[i+1])
                    offspring.extend([child1, child2])
                else:
                    offspring.extend([selected[i], selected[i+1]] if i+1 < len(selected) else [selected[i]])
            
            # 变异
            for i in range(len(offspring)):
                if random.random() < 0.2:
                    offspring[i] = self.mutation(offspring[i])
            
            # 新一代
            self.population = offspring
        
        return best_sequence, best_cost

# 调度器类（与之前相同）
class Scheduler:
    def __init__(self, sequence):
        self.sequence = sequence
        self.machine_timeline = defaultdict(list)
        self.job_completion = {}
        self.schedule = []
    
    def generate_schedule(self):
        for job_idx in self.sequence:
            job = job_idx - 1  # 转换为0-based索引
            prev_end = 0
            
            for machine in range(n_machines):
                duration = processing_time[job][machine]
                
                if machine > 0:
                    prev_end = self.job_completion.get((job_idx, machine-1), 0)
                
                start_time = self.find_available_slot(machine, prev_end, duration)
                end_time = start_time + duration
                
                self.machine_timeline[machine].append((start_time, end_time, job_idx))
                self.job_completion[(job_idx, machine)] = end_time
                
                self.schedule.append({
                    'job': job_idx,
                    'machine': machine + 1,
                    'start': start_time,
                    'end': end_time,
                    'duration': duration
                })
    
    def find_available_slot(self, machine, earliest_start, duration):
        timeline = sorted(self.machine_timeline[machine], key=lambda x: x[0])
        
        if not timeline:
            return max(earliest_start, 0)
        
        # 检查第一个窗口
        if earliest_start + duration <= timeline[0][0]:
            return max(earliest_start, 0)
        
        # 检查中间窗口
        for i in range(len(timeline)-1):
            current_end = timeline[i][1]
            next_start = timeline[i+1][0]
            available_start = max(current_end, earliest_start)
            if next_start - available_start >= duration:
                return available_start
        
        # 检查最后一个窗口
        last_end = timeline[-1][1]
        return max(last_end, earliest_start)
    
    def calculate_cost(self):
        total_cost = 0
        peak_time = 0
        
        for record in self.schedule:
            start = record['start']
            end = record['end']
            machine = record['machine'] - 1
            remaining = record['duration']
            current_time = start
            
            while remaining > 0:
                slot = self.get_time_slot(current_time)
                available = min(remaining, slot['end'] - current_time)
                
                cost = available * slot['price'] * r[machine]
                total_cost += cost
                
                if slot['type'] == '尖峰':
                    peak_time += available
                
                remaining -= available
                current_time += available
        
        return total_cost, peak_time
    
    def get_time_slot(self, time):
        time = time % 1440
        for slot in time_slots:
            if slot['start'] <= time < slot['end']:
                return slot
        return time_slots[-1]

# 格式化输出（与之前相同）
def format_time(minutes):
    base_time = datetime.strptime("07:00", "%H:%M")
    delta = timedelta(minutes=minutes)
    return (base_time + delta).strftime("%H:%M")

def print_solution(sequence, cost, peak_time, schedule):
    print("=== 最优解 ===")
    print(f"总用电成本: {cost:.2f} 元")
    print(f"尖峰时段总加工时间: {peak_time:.1f} 分钟\n")
    
    job_order = " → ".join([f"J{job}" for job in sequence])
    print(f"最优工件顺序: {job_order}\n")
    
    print("=== 详细调度方案 ===\n")
    
    job_records = defaultdict(dict)
    for record in schedule:
        job = record['job']
        machine = record['machine']
        job_records[job][machine] = record
    
    for job in sequence:
        print(f"工件{job}:")
        for machine in range(1, n_machines+1):
            record = job_records[job][machine]
            start = record['start']
            end = record['end']
            duration = record['duration']
            
            print(f"  机器{machine}: {format_time(start)}-{format_time(end)}")
            print("    时段详情:")
            
            current_time = start
            remaining = duration
            
            while remaining > 0:
                slot = Scheduler([]).get_time_slot(current_time)
                available = min(remaining, slot['end'] - current_time)
                
                start_str = format_time(current_time)
                end_str = format_time(current_time + available)
                
                cost = available * slot['price'] * r[machine-1]
                print(f"    - {slot['type']} {start_str}-{end_str}: {available:.1f}分钟, "
                      f"电价={slot['price']:.4f}元/kWh, 电费={cost:.2f}元")
                
                remaining -= available
                current_time += available
            
            print()
        print()

# 主程序
if __name__ == "__main__":
    # 运行遗传算法求解最优序列
    ga = GeneticAlgorithm(pop_size=50, max_gen=200)
    best_sequence, best_cost = ga.run()
    
    # 生成详细调度方案
    scheduler = Scheduler(best_sequence)
    scheduler.generate_schedule()
    total_cost, peak_time = scheduler.calculate_cost()
    
    # 输出结果
    print_solution(best_sequence, total_cost, peak_time, scheduler.schedule)