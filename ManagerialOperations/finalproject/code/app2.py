from docplex.mp.model import Model
import math
from collections import defaultdict

def calculate_C(p):
    """计算生产期限上界C"""
    max_p = max([p[i][j] for i in range(len(p)) for j in range(len(p[0]))])
    sum_max = sum([max([p[i][j] for i in range(len(p))]) for j in range(len(p[0]))])
    return max_p + sum_max

def main_scenario_peak():
    # 初始化模型
    mdl = Model('FlowShop_With_Peak')
    
    # ========== 参数定义 ==========
    n = 5                   # 工件数
    m = 3                   # 机器数
    r = [10, 6, 8]          # 机器能耗(kWh/min)
    p = [                   # 加工时间(分钟)
        [20, 32, 14],
        [33, 34, 20],
        [45, 14, 30],
        [63, 22, 16],
        [38, 15, 35]
    ]
    beta = 1.75             # 生产紧急系数
    C = calculate_C(p)
    T = beta * C            # 生产期限
    print(f"生产期限T={T}分钟 ({T/60:.2f}小时)")

    # ========== 分时电价定义（含尖峰时段） ==========
    time_slots = [
        # 平峰时段 7:00-10:00 (0-180分钟)
        {'start': 0,    'end': 180,  'price': 0.7181, 'type': '平峰'},
        # 高峰时段 10:00-11:00 (180-240分钟)
        {'start': 180,  'end': 240,  'price': 1.2238, 'type': '高峰'},
        # 尖峰时段 11:00-13:00 (240-360分钟)
        {'start': 240,  'end': 360,  'price': 1.3472, 'type': '尖峰'},
        # 高峰时段 13:00-15:00 (360-480分钟)
        {'start': 360,  'end': 480,  'price': 1.2238, 'type': '高峰'},
        # 平峰时段 15:00-16:00 (480-540分钟)
        {'start': 480,  'end': 540,  'price': 0.7181, 'type': '平峰'},
        # 尖峰时段 16:00-17:00 (540-600分钟)
        {'start': 540,  'end': 600,  'price': 1.3472, 'type': '尖峰'},
        # 平峰时段 17:00-18:00 (600-660分钟)
        {'start': 600,  'end': 660,  'price': 0.7181, 'type': '平峰'},
        # 高峰时段 18:00-21:00 (660-840分钟)
        {'start': 660,  'end': 840,  'price': 1.2238, 'type': '高峰'},
        # 平峰时段 21:00-23:00 (840-960分钟)
        {'start': 840,  'end': 960,  'price': 0.7181, 'type': '平峰'},
        # 低谷时段 23:00-7:00 (960-1440分钟)
        {'start': 960,  'end': 1440, 'price': 0.2417, 'type': '低谷'}
    ]
    
    # 筛选有效时段（仅保留在T内的部分）
    valid_slots = []
    for slot in time_slots:
        slot_start = slot['start']
        slot_end = min(slot['end'], T)
        if slot_start < slot_end:
            valid_slots.append({
                'start': slot_start,
                'end': slot_end,
                'price': slot['price'],
                'type': slot['type']
            })
    
    print("\n有效电价时段:")
    for idx, s in enumerate(valid_slots):
        print(f"时段{idx}: {s['start']/60:.1f}h-{s['end']/60:.1f}h {s['type']} 价格={s['price']}元/kWh")

    # ========== 决策变量 ==========
    # 1. 顺序变量（工件i是否在工件j之前）
    y = {(i, j): mdl.binary_var(name=f'y_{i}_{j}') for i in range(n) for j in range(n) if i != j}
    
    # 2. 时间变量（工件i在机器j上的开始和完成时间）
    s = {(i, j): mdl.continuous_var(lb=0, ub=T, name=f's_{i}_{j}') for i in range(n) for j in range(m)}
    c = {(i, j): mdl.continuous_var(lb=0, ub=T, name=f'c_{i}_{j}') for i in range(n) for j in range(m)}
    
    # 3. 时段加工时间（机器j在时段k的加工时长）
    t = {(j, k): mdl.continuous_var(lb=0, name=f't_{j}_{k}') for j in range(m) for k in range(len(valid_slots))}
    
    # 4. 尖峰时段使用标志（可选，用于分析）
    peak_usage = {(j, k): mdl.binary_var(name=f'peak_{j}_{k}') 
                 for j in range(m) for k, slot in enumerate(valid_slots) if slot['type'] == '尖峰'}

    # ========== 约束条件 ==========
    # 1. 唯一顺序约束
    for i in range(n):
        for j in range(n):
            if i < j:
                mdl.add_constraint(y[i, j] + y[j, i] == 1, ctname=f'order_{i}_{j}')
    
    # 2. 同一机器顺序约束
    M = T * 2  # 大M值
    for j in range(m):
        for i in range(n):
            for ip in range(n):
                if i != ip:
                    mdl.add_constraint(
                        s[ip, j] >= c[i, j] - M*(1 - y[i, ip]),
                        ctname=f'machine_{j}_order_{i}_{ip}'
                    )
    
    # 3. 跨机器顺序约束
    for i in range(n):
        for j in range(m-1):
            mdl.add_constraint(s[i, j+1] >= c[i, j], ctname=f'cross_{i}_{j}')
    
    # 4. 加工时间约束
    for i in range(n):
        for j in range(m):
            mdl.add_constraint(c[i, j] == s[i, j] + p[i][j], ctname=f'process_{i}_{j}')
    
    # 5. 生产期限约束
    for i in range(n):
        mdl.add_constraint(c[i, m-1] <= T, ctname=f'deadline_{i}')
    
    # 6. 分时电价时段加工时间计算
    for j in range(m):
        for k, slot in enumerate(valid_slots):
            slot_start = slot['start']
            slot_end = slot['end']
            
            # 计算机器j在时段k的总加工时间
            total_time = 0
            for i in range(n):
                # 计算工件i在机器j的加工时间段与当前时段的交集
                overlap_start = mdl.max(s[i, j], slot_start)
                overlap_end = mdl.min(c[i, j], slot_end)
                duration = mdl.max(0, overlap_end - overlap_start)
                total_time += duration
            
            mdl.add_constraint(t[j, k] == total_time, ctname=f'time_{j}_{k}')
            
            # 尖峰时段使用标志约束
            if slot['type'] == '尖峰':
                mdl.add_constraint(peak_usage[j, k] >= t[j, k]/M)
                mdl.add_constraint(peak_usage[j, k] <= t[j, k])

    # ========== 禁用特定顺序 [5,1,2,3,4] ==========
    # y[4,0] = 1 (J5在J1前)
    # y[0,1] = 1 (J1在J2前)
    # y[1,2] = 1 (J2在J3前)
    # y[2,3] = 1 (J3在J4前)
    mdl.add_constraint(
        y[4,0] + y[0,1] + y[1,2] + y[2,3] <= 3,
        ctname='forbid_sequence_5_1_2_3_4'
    )

    # ========== 目标函数 ==========
    # 基础电费成本
    base_cost = sum(r[j] * t[j, k] * slot['price'] 
                   for j in range(m) for k, slot in enumerate(valid_slots))
    
    # 尖峰时段惩罚项（可选）
    peak_penalty = 10 * sum(peak_usage[j, k] 
                          for j in range(m) for k, slot in enumerate(valid_slots) 
                          if slot['type'] == '尖峰')
    
    mdl.minimize(base_cost + peak_penalty)

    # ========== 模型求解 ==========
    solution = mdl.solve(log_output=True)
    
    # ========== 结果输出 ==========
    if solution:
        # 辅助函数：分钟转时间字符串
        def minutes_to_time(mins, start_hour=7):
            total_mins = int(round(mins))
            hours = (start_hour + total_mins // 60) % 24
            minutes = total_mins % 60
            return f"{hours:02d}:{minutes:02d}"
        
        print("\n=== 最优解 ===")
        print(f"总用电成本: {solution.get_objective_value():.2f} 元")
        
        # 统计尖峰时段使用情况
        peak_usage_total = sum(solution.get_value(t[j, k]) 
                             for j in range(m) for k, slot in enumerate(valid_slots) 
                             if slot['type'] == '尖峰')
        print(f"尖峰时段总加工时间: {peak_usage_total:.1f} 分钟")
        
        # 获取工件顺序 - 拓扑排序
        precedence = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(n):
                if i != j and solution.get_value(y[i, j]) > 0.5:
                    precedence[i].append(j)
        
        in_degree = {i: 0 for i in range(n)}
        for i in precedence:
            for j in precedence[i]:
                in_degree[j] += 1
        
        queue = [i for i in range(n) if in_degree[i] == 0]
        seq_order = []
        while queue:
            node = queue.pop(0)
            seq_order.append(node+1)  # 转换为1-based编号
            for neighbor in precedence[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        print("\n最优工件顺序:", " → ".join([f"J{x}" for x in seq_order]))
        
        print("\n=== 详细调度方案 ===")
        printed_jobs = set()
        for job in seq_order:
            i = job - 1
            if i in printed_jobs:
                continue
            printed_jobs.add(i)
            
            print(f"\n工件{job}:")
            for j in range(m):
                start = solution.get_value(s[i, j])
                end = solution.get_value(c[i, j])
                print(f"  机器{j+1}: {minutes_to_time(start)}-{minutes_to_time(end)}")
                
                # 计算各时段加工详情
                print("    时段详情:")
                for k, slot in enumerate(valid_slots):
                    slot_start = slot['start']
                    slot_end = slot['end']
                    overlap_start = max(start, slot_start)
                    overlap_end = min(end, slot_end)
                    duration = max(0, overlap_end - overlap_start)
                    
                    if duration > 0.1:  # 忽略极小值
                        cost = r[j] * duration * slot['price']
                        print(f"    - {slot['type']} {minutes_to_time(overlap_start)}-{minutes_to_time(overlap_end)}: "
                              f"{duration:.1f}分钟, 电价={slot['price']}元/kWh, 电费={cost:.2f}元")
    else:
        print("未找到可行解")

if __name__ == "__main__":
    main_scenario_peak()