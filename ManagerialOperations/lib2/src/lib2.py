import cplex
import json

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def build_model(data):
    problem = cplex.Cplex()
    problem.objective.set_sense(problem.objective.sense.minimize)
    
    # 添加变量
    problem.variables.add(
        obj=data["obj_coeff"],
        names=data["variables"],
        lb=[0.0] * len(data["variables"])
    )
    
    # 添加煤矿供应约束
    for coeff, limit in zip(data["supply_constraints"]["coefficients"], data["supply_constraints"]["limits"]):
        problem.linear_constraints.add(
            lin_expr=[[data["variables"], coeff]],
            senses=["L"],
            rhs=[limit]
        )
    
    # 添加电厂最低需求约束
    for coeff, limit in zip(data["demand_constraints"]["min"]["coefficients"], data["demand_constraints"]["min"]["limits"]):
        problem.linear_constraints.add(
            lin_expr=[[data["variables"], coeff]],
            senses=["G"],
            rhs=[limit]
        )
    
    # 添加电厂最高需求约束
    for coeff, limit in zip(data["demand_constraints"]["max"]["coefficients"], data["demand_constraints"]["max"]["limits"]):
        problem.linear_constraints.add(
            lin_expr=[[data["variables"], coeff]],
            senses=["L"],
            rhs=[limit]
        )
    
    return problem

def solve_and_print(problem):
    problem.solve()
    print("最优目标值（最小运费）：", problem.solution.get_objective_value())
    for var, value in zip(problem.variables.get_names(), problem.solution.get_values()):
        print(f"{var} = {value}")

if __name__ == "__main__":
    data = load_data("lib2.data")
    model = build_model(data)
    solve_and_print(model)