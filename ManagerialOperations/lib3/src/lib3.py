import json
from docplex.mp.model import Model

def load_data(file_path):
    """加载数据文件"""
    with open(file_path, 'r') as f:
        return json.load(f)

def build_model(data):
    """构建生产规划模型"""
    model = Model(name="Production_Planning")
    
    # 创建决策变量
    x = {p: model.continuous_var(lb=0, name=f"x_{p}") for p in data["Products"]}
    y = {p: model.binary_var(name=f"y_{p}") for p in data["Products"]}
    
    # 目标函数：最大化利润
    model.maximize(
        model.sum(
            (data["Price"][i] - data["VariableCost"][i]) * x[p] - data["FixedCost"][i] * y[p]
            for i, p in enumerate(data["Products"])
        )
    )
    
    # 资源约束
    for r_idx, r in enumerate(data["Resources"]):
        model.add_constraint(
            model.sum(
                data["Consumption"][r][i] * x[p] 
                for i, p in enumerate(data["Products"])
            ) <= data["ResourceLimit"][r_idx],
            ctname=f"resource_{r}"
        )
    
    # 固定费用约束
    for i, p in enumerate(data["Products"]):
        model.add_constraint(
            x[p] <= data["ResourceLimit"][0] * y[p],  # 使用资源A的总量作为大M
            ctname=f"fixed_cost_{p}"
        )
    
    return model, x, y

def solve_and_print(model, x, y, data):
    """求解并打印结果（与求解器格式匹配）"""
    solution = model.solve()
    
    if solution:
        print("// solution (optimal) with objective", solution.get_objective_value())
        print("\n决策变量值:")
        for p in data["Products"]:
            print(f"x_{p}: {solution.get_value(x[p])}")
            print(f"y_{p}: {round(solution.get_value(y[p]))}")  # 四舍五入消除浮点误差
        
        print("\n生产计划:")
        for i, p in enumerate(data["Products"]):
            if solution.get_value(x[p]) > 1e-6:  # 忽略极小值
                print(f"产品{p}: 生产{solution.get_value(x[p])}单位 (固定成本支付: {round(solution.get_value(y[p]))})")
    else:
        print("未找到可行解")

if __name__ == "__main__":
    # 加载数据
    data = load_data("lib3.data")
    
    # 构建并求解模型
    model, x, y = build_model(data)
    solve_and_print(model, x, y, data)