# lib1.py

import cplex

# 读取lib1.data
import ast

data = {}
with open('lib1.data', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            key, value = line.split('=')
            data[key.strip()] = ast.literal_eval(value.strip())

# 提取数据
profit_coefficients = data['profit_coefficients']
casting_hours = data['casting_hours']
machining_hours = data['machining_hours']
assembly_hours = data['assembly_hours']
casting_limit = data['casting_limit']
machining_limit = data['machining_limit']
assembly_limit = data['assembly_limit']

# 创建Cplex问题实例
problem = cplex.Cplex()

# 设置为最大化问题
problem.objective.set_sense(problem.objective.sense.maximize)

# 添加决策变量
variable_names = ['x1', 'y1', 'x2', 'y2', 'x3']
problem.variables.add(
    obj=profit_coefficients,
    names=variable_names,
    lb=[0.0] * len(variable_names)  # 非负约束
)

# 添加约束
# 1. 铸造工时
problem.linear_constraints.add(
    lin_expr=[[variable_names, casting_hours]],
    senses=['L'],
    rhs=[casting_limit]
)

# 2. 机加工工时
problem.linear_constraints.add(
    lin_expr=[[variable_names, machining_hours]],
    senses=['L'],
    rhs=[machining_limit]
)

# 3. 装配工时
problem.linear_constraints.add(
    lin_expr=[[variable_names, assembly_hours]],
    senses=['L'],
    rhs=[assembly_limit]
)

# 求解
problem.solve()

# 打印结果
print("最优目标值（最大利润）：", problem.solution.get_objective_value())
for var_name, value in zip(variable_names, problem.solution.get_values()):
    print(f"{var_name} = {value}")
