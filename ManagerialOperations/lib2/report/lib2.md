
## <center><font size="5">实验二、运输问题</font></center>

### **一、实验目的：**

&nbsp;（1）掌握运输问题的基本模型；

&nbsp; （2）掌握不平衡运输问题的求解方法。

&nbsp;（3）将不同问题转化为运输问题进行求解。

&nbsp;（4）熟练使用OPL语言求解运输问题。

### **二、实验内容：**

&nbsp;（1）完成实验手册给出的案例；

&nbsp;（2）针对实验手册的练习，建立数学规划模型、求解模型以及实验结果的分析。

### **三、操作步骤：**

#### （1）.建立数学规划模型

##### 1.问题分析

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;该煤矿供应电厂的运输问题，涉及三个煤矿（A、B、C）和四个电厂（I、II、III、IV）。目标是找到运费最少的煤炭调拨方案。

- 煤矿产量：
  - A：55万吨
  - B：55万吨
  - C：50万吨
  - 总产量：160万吨

- 电厂需求：

  - 最低需求量：I（30）、II（70）、III（0）、IV（10）

  - 最高需求量：I（50）、II（70）、III（30）、IV（不限）

  - 总最低需求：110万吨

  - 总最高需求：150万吨（IV按最低需求计算）

- 运价表：

  - 煤矿到电厂的运价（元/吨）：

    - A：I（16）、II（13）、III（22）、IV（17）

    - B：I（14）、II（13）、III（19）、IV（15）

    - C：I（19）、II（20）、III（23）、IV（-，表示不允许运输）


##### 2.决策变量定义

定义决策变量：
- \( x_{ij} \)：从煤矿 \( i \) 运到电厂 \( j \) 的煤炭量（万吨），其中：

  - \( i \in \{A, B, C\} \)

  - \( j \in \{I, II, III, IV\} \)


3.目标函数

目标是最小化总运输成本：
\[
\min z = 16x_{AI} + 13x_{AII} + 22x_{AIII} + 17x_{AIV} + 14x_{BI} + 13x_{BII} + 19x_{BIII} + 15x_{BIV} + 19x_{CI} + 20x_{CII} + 23x_{CIII}
\]

4.约束条件

1. 煤矿供应约束：
   - A：\( x_{AI} + x_{AII} + x_{AIII} + x_{AIV} \leq 55 \)

   - B：\( x_{BI} + x_{BII} + x_{BIII} + x_{BIV} \leq 55 \)

   - C：\( x_{CI} + x_{CII} + x_{CIII} \leq 50 \)（C到IV不允许运输）


2. 电厂需求约束：
   - 最低需求：

     - I：\( x_{AI} + x_{BI} + x_{CI} \geq 30 \)

     - II：\( x_{AII} + x_{BII} + x_{CII} \geq 70 \)

     - III：\( x_{AIII} + x_{BIII} + x_{CIII} \geq 0 \)

     - IV：\( x_{AIV} + x_{BIV} \geq 10 \)（C不到IV）

   - 最高需求：

     - I：\( x_{AI} + x_{BI} + x_{CI} \leq 50 \)

     - II：\( x_{AII} + x_{BII} + x_{CII} \leq 70 \)

     - III：\( x_{AIII} + x_{BIII} + x_{CIII} \leq 30 \)

     - IV：\( x_{AIV} + x_{BIV} \) 不限（无上限）


3. 非负约束：
   - \( x_{ij} \geq 0 \) 对所有 \( i, j \)


#### （2）.分析模型并求解

##### 标准型总结

\[
\begin{aligned}
\min \quad & z = 16x_{AI} + 13x_{AII} + 22x_{AIII} + 17x_{AIV} + 14x_{BI} + 13x_{BII} + 19x_{BIII} + 15x_{BIV} + 19x_{CI} + 20x_{CII} + 23x_{CIII} \\
\text{s.t.} \quad & x_{AI} + x_{AII} + x_{AIII} + x_{AIV} \leq 55 \\
& x_{BI} + x_{BII} + x_{BIII} + x_{BIV} \leq 55 \\
& x_{CI} + x_{CII} + x_{CIII} \leq 50 \\
& x_{AI} + x_{BI} + x_{CI} \geq 30 \\
& x_{AI} + x_{BI} + x_{CI} \leq 50 \\
& x_{AII} + x_{BII} + x_{CII} \geq 70 \\
& x_{AII} + x_{BII} + x_{CII} \leq 70 \\
& x_{AIII} + x_{BIII} + x_{CIII} \geq 0 \\
& x_{AIII} + x_{BIII} + x_{CIII} \leq 30 \\
& x_{AIV} + x_{BIV} \geq 10 \\
& x_{ij} \geq 0 \quad \forall i, j
\end{aligned}
\]

由于使用py与json录入数据更加方便快捷，优先给出我的`Python`解决方案

##### 使用Python `cplex`模块求解

```python
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

```


`.data`文件，采用json格式

```json
{
  "variables": [
    "x_AI", "x_AII", "x_AIII", "x_AIV",
    "x_BI", "x_BII", "x_BIII", "x_BIV",
    "x_CI", "x_CII", "x_CIII"
  ],
  "obj_coeff": [16, 13, 22, 17, 14, 13, 19, 15, 19, 20, 23],
  "supply_constraints": {
    "names": ["A", "B", "C"],
    "coefficients": [
      [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
    ],
    "limits": [55, 55, 50]
  },
  "demand_constraints": {
    "min": {
      "names": ["I", "II", "III", "IV"],
      "coefficients": [
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
      ],
      "limits": [30, 70, 0, 10]
    },
    "max": {
      "names": ["I", "II", "III"],
      "coefficients": [
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
      ],
      "limits": [50, 70, 30]
    }
  }
}
```
##### 使用`IBM cplex`求解器求解

同时为了契合实验要求，使用`ibm cplex`求解如下

`.data`文件

```data
// 可以单独使用数据文件或直接在.mod文件中定义
Mines = {"A", "B", "C"};
Plants = {"I", "II", "III", "IV"};

Supply = [55, 55, 50];
MinDemand = [30, 70, 0, 10];
MaxDemand = [50, 70, 30, 10000];

Cost = [
    [16, 13, 22, 17],
    [14, 13, 19, 15], 
    [19, 20, 23, 10000]
];
```

`.mod`文件使用opl语言

```opl
//1. 定义决策变量
dvar float+ Transport[Mines][Plants]; // 运输量

// 2. 目标函数：最小化总运费
minimize sum(m in Mines, p in Plants) Cost[m][p] * Transport[m][p];

// 3. 约束条件
subject to {
    // 煤矿供应约束
    forall(m in Mines)
        sum(p in Plants) Transport[m][p] <= Supply[m];
    
    // 电厂需求约束
    forall(p in Plants) {
        // 最低需求
        sum(m in Mines) Transport[m][p] >= MinDemand[p];
        // 最高需求
        sum(m in Mines) Transport[m][p] <= MaxDemand[p];
    }
    
    // 特殊约束：C矿不能运到IV电厂
    Transport["C"]["IV"] == 0;
}

// 4. 输出结果
execute {
    writeln("最优运输方案：");
    for(var m in Mines) {
        for(var p in Plants) {
            if(Transport[m][p] > 0) {
                writeln("从煤矿", m, "运到电厂", p, ": ", Transport[m][p], "万吨");
            }
        }
    }
    writeln("最小总运费：", cplex.getObjValue(), "万元");
}

```

运行求解器得到结果：
![](../outputs/002.png)


如图，得到与python输出一致的结果


#### （3）实验结果分析


##### 求解结果

![](../outputs/001.png)



运行上述代码后，得到最优解： 

| 运输路线 | 运量（万吨） | 运价（元/吨） | 运费（万元） |
|---------|------------|------------|------------|
| A→II    | 55         | 13         | 715        |
| B→I     | 30         | 14         | 420        |
| B→II    | 15         | 13         | 195        |
| B→IV    | 10         | 15         | 150        |
| 合计 | 110    | -          | 1480   |


约束满足情况：
| 电厂 | 最低需求 | 实际接收 | 满足状态 |
|-----|--------|--------|--------|
| I   | 30     | 30     | ✔      |
| II  | 70     | 70     | ✔      |
| III | 0      | 0      | ✔      |
| IV  | 10     | 10     | ✔      |
 

##### 结论

CPLEX求解器输出的1480万元方案是最优解。 

        煤矿C没有被使用；
        电厂Ⅰ、Ⅱ、Ⅳ的最小需求全部满足；
        电厂Ⅲ无最低需求，因此未分配煤；
        所有运输方案均在各自供需限制范围内；
        成本最小化已达成最优解。


### **四、实验中遇到的主要问题及解决方法**


#### 1.使用cplex设置二维变量问题

由于本题我在定义决策变量时候使用的是二维变量，在使用`cplex`求解器进行求解时候，对二维数组这个数据结构不是很理解,相较于c/c++/py中的二维数组，其下标都是`int`整型数据，而在cplex中，可以使用字符串来进行命名，这就便于数据的理解和运用，而我在通过学习`cplex使用手册了解到可以这样设置后`，修改了代码逻辑：

    Mines = {"A", "B", "C"};
    Plants = {"I", "II", "III", "IV"};

相较于使用json结构的data文件：

    "names": ["A", "B", "C"],
        "coefficients": [
          [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
        ],
        "limits": [55, 55, 50]
      },
      "demand_constraints": {
        "min": {
          "names": ["I", "II", "III", "IV"],
          "coefficients": [
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
          ],
          "limits": [30, 70, 0, 10]
        },

cplex的变量设置更加简洁
因为`json`中维护了对应变量的一个系数矩阵
每个约束行的1/0值对应变量是否参与该约束
例如煤矿A的约束 [1,1,1,1,0...] 表示只包含$x_{AI}到x_{AIV}$四个变量



---