## <center><font size="5">实验一、线性规划</font></center>

### **一、实验目的：**

&nbsp;（1）理解线性规划的概念。

&nbsp;（2）对于一个问题，能够建立基本的线性规划模型。

&nbsp;（3）学会运用OPL语言解决线性规划问题。

&nbsp;（4）将不同问题转化为线性规划的数学模型。

### **二、实验内容：**

&nbsp;（1）完成实验手册给出的案例；

&nbsp;（2）针对实验手册的练习，建立数学规划模型、求解模型以及实验结果的分析。

### **三、操作步骤：**

#### （1）.建立数学规划模型

##### 1.问题分析

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;解决某公司关于甲、乙、丙三种产品的生产决策问题，涉及自行生产和外包协作的选择,目标最大化公司利润

- 1. 生产流程：三种产品都需要经过铸造、机加工和装配三个车间。


- 2. 外包限制：
     - 甲、乙产品的铸件可以外包或自行生产。
     - 丙产品的铸件必须自行生产。

- 3. 资源限制：
        - 铸造总工时：8000小时
        - 机加工总工时：12000小时
        - 装配总工时：10000小时

- 4. 成本与售价：
        - 自产铸件成本、外协铸件成本、机加工成本、装配成本。       
        - 每件产品的售价。


##### 2.决策变量定义

定义以下决策变量：

- \( x_1 \)：甲产品自行生产的数量。

- \( x_2 \)：乙产品自行生产的数量。

- \( x_3 \)：丙产品自行生产的数量（必须自行生产，因此不设置\(y_2）\)。

- \( y_1 \)：甲产品外协生产的数量。

- \( y_2 \)：乙产品外协生产的数量。


##### 3.目标函数:

目标是最大化利润，计算公式为：
\[
\text{利润} = \sum (\text{售价} - \text{总成本}) \times \text{数量}
\]

具体到每种产品：

- 甲产品：

  - 自行生产的总成本：铸造成本 + 机加工成本 + 装配成本 = 3 + 2 + 3 = 8 元

  - 外协生产的总成本：外协铸件成本 + 机加工成本 + 装配成本 = 6 + 2 + 3 = 11 元

  - 售价：23 元

  - 甲产品利润：自行生产 \( (23 - 8)x_1 = 15x_1 \)，外协生产 \( (23 - 11)y_1 = 12y_1 \)

  
- 乙产品：

  - 自行生产的总成本：5 + 1 + 2 = 8 元

  - 外协生产的总成本：7 + 1 + 2 = 10 元

  - 售价：18 元

  - 乙产品利润：自行生产 \( (18 - 8)x_2 = 10x_2 \)，外协生产 \( (18 - 10)y_2 = 8y_2 \)

  
- 丙产品：

  - 自行生产的总成本：4 + 3 + 2 = 9 元

  - 售价：16 元

  - 利润贡献：\( (16 - 9)x_3 = 7x_3 \)


总结上述相加,得到目标函数：

\[
\max z = 15x_1 + 12y_1 + 10x_2 + 8y_2 + 7x_3
\]

##### 4.约束条件

1. 资源约束：
   - 铸造工时：

     - 自行生产甲：5小时/件，乙：10小时/件，丙：7小时/件。

     - 外协生产甲、乙不占用铸造工时。

     - 约束：\( 5x_1 + 10x_2 + 7x_3 \leq 8000 \)

   - 机加工工时：

     - 甲：7小时/件，乙：5小时/件，丙：8小时/件。

     - 约束：\( 7(x_1 + y_1) + 5(x_2 + y_2) + 8x_3 \leq 12000 \)

   - 装配工时：

     - 甲：3小时/件，乙：2小时/件，丙：2小时/件。

     - 约束：\( 3(x_1 + y_1) + 2(x_2 + y_2) + 2x_3 \leq 10000 \)


2. 非负约束：
   - \( x_1, x_2, x_3, y_1, y_2 \geq 0 \)


#### （2）.分析模型并求解

##### 标准型总结
$$
\begin{aligned}
\max \quad & z = 15x_1 + 12y_1 + 10x_2 + 8y_2 + 7x_3 \\
\text{约束s.t.} \quad & 5x_1 + 10x_2 + 7x_3 \leq 8000 \\
& 7x_1 + 7y_1 + 5x_2 + 5y_2 + 8x_3 \leq 12000 \\
& 3x_1 + 3y_1 + 2x_2 + 2y_2 + 2x_3 \leq 10000 \\
& x_1, x_2, x_3, y_1, y_2 \geq 0
\end{aligned}
$$
 

我使用了2种求解方法，第一种为课程实验`ibm cplex`求解器,第二种为python代码导入`cplex`模块进行求解

##### IBM cplex求解：

.Mod 文件

```opl

// 决策变量
dvar float+ Self[Products];  // 自产量
dvar float+ Out[Products];   // 外协量（仅甲、乙可用）

// 外协限制（丙必须自产）
execute {
    Out["C"].UB = 0;
}

// 目标函数：最大化总利润
maximize
    sum(p in Products) (
        (Price[p] - SelfCastCost[p] - ProcessCost["Machine"][p] - ProcessCost["Assembly"][p]) * Self[p] +
        (Price[p] - OutCastCost[p] - ProcessCost["Machine"][p] - ProcessCost["Assembly"][p]) * Out[p]
    );

// 约束条件
subject to {
    // 铸造工时约束（仅自产消耗）
    sum(p in Products) Time["Cast"][p] * Self[p] <= MaxTime["Cast"];
    
    // 机加工工时约束（自产+外协都消耗）
    sum(p in Products) Time["Machine"][p] * (Self[p] + Out[p]) <= MaxTime["Machine"];
    
    // 装配工时约束（自产+外协都消耗）
    sum(p in Products) Time["Assembly"][p] * (Self[p] + Out[p]) <= MaxTime["Assembly"];
}

```

.Data 文件
```opl
// 定义集合
{string} Products = {"A", "B", "C"};  // 产品：甲(A)、乙(B)、丙(C)
{string} Processes = {"Cast", "Machine", "Assembly"}; // 工序

// 工时参数（小时/件）
float Time[Processes][Products] = [
    [5, 10, 7],   // 铸造工时
    [7, 5, 8],    // 机加工工时
    [3, 2, 2]     // 装配工时
];

// 成本与售价（元/件）
float SelfCastCost[Products] = [3, 5, 4];    // 自产铸件成本
float OutCastCost[Products] = [6, 7, 9999];  // 外协铸件成本（丙设为极大值表示不可外包）
float ProcessCost[Processes][Products] = [
    [0, 0, 0],      // 铸造成本已单独考虑
    [2, 1, 3],      // 机加工成本
    [3, 2, 2]       // 装配成本
];
float Price[Products] = [23, 18, 16];       // 产品售价

// 资源约束（小时）
float MaxTime[Processes] = [8000, 12000, 10000]; // 各工序最大工时

```
 
 
运行模型后，得到以下决策变量的最优解：

如图所示:
![](../outputs/001.png)
- 自行生产甲产品1600 件，乙产品0 件，丙产品 0 件。
- 外协生产甲产品114.29件，乙产品 0件。
- 最大利润为 25371.4285714286 元。

##### python `cplex`模块求解

我更习惯使用py调用库和通过json读data来解决数据

**tip:(征得老师同意，后面的问题求解更偏向于使用此方法)**

线性规划模型`.py`求解
```Python
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


```

定义`.data`文件

```json
# lib1.data

# 利润系数
profit_coefficients = [15, 12, 10, 8, 7]
# 铸造工时系数
casting_hours = [5, 0, 10, 0, 7]
# 机加工工时系数
machining_hours = [7, 7, 5, 5, 8]
# 装配工时系数
assembly_hours = [3, 3, 2, 2, 2]
# 资源总量
casting_limit = 8000
machining_limit = 12000
assembly_limit = 10000
```
 
运行求解得到：

![](../outputs/002.png)

与cplex求解得到了相同结果

#### （3）实验结果分析

##### 结果

2个模型求解得到了生产计划如下：
- 自行生产甲产品1600 件，乙产品0 件，丙产品 0 件。
- 外协生产甲产品114.29件，乙产品 0件。
- 最大利润为 25371.4285714286 元。

##### 利润构成
- 甲产品自行生产利润：1600 × 15 = 24,000元
- 甲产品外协生产利润：114.29 × 12 ≈ 1,371元
- **总利润**：25,371.43元






### **四、实验中遇到的主要问题及解决方法**

#### 1.**Q2: cplex报错运行` ÔËÐÐÅäÖá°配置 1¡±²»´æÔڡ£	 `未知	OPL 问题标**
 参考博客[解决cplex出现ÔËÐÐÅäÖá°配置 1¡±²»´æÔڡ£的问题](https://blog.csdn.net/qq_20412595/article/details/130985038?fromshare=blogdetail&sharetype=blogdetail&sharerId=130985038&sharerefer=PC&sharesource=LLH004&sharefrom=from_link)
将项目配置文件改为英文config1，（只要是英文就行）
其原因是因为cplexstdio中文兼容不好

#### 2.进行线性规划求解时候，获得的答案不是整数

引用本题结果得到

        自行生产甲产品1600 件，乙产品0 件，丙产品 0 件。
        外协生产甲产品114.29件，乙产品 0件。
       

虽然本体是线性规划，但是作为实际案例来讨论，进行外包选择小数114.29显然是不可行的，因此，需要对结果分析考量，做出优化

        自行生产甲产品1600 件，乙产品0 件，丙产品 0 件。
        外协生产甲产品114件，乙产品 0件。

如此得到最大利润为：

`25,377元`

使用整数规划加整数约束显然更符合


#### 3.约束条件的探究

本题的约束条件有：

    -  外包限制：
        - 甲、乙产品的铸件可以外包或自行生产。
        - 丙产品的铸件必须自行生产。

    -  资源限制：
            - 铸造总工时：8000小时
            - 机加工总工时：12000小时
            - 装配总工时：10000小时


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;需要区分的是，对外包的数量是没有限制的，但是后面的机加工和装配时长间接限制了外包数量，而机加工，装配本身不能使用外包运作，所以要考率到$y_1,y_2$变量在约束条件中的不同作用


---

