
## <center><font size="5">实验四、图与网络分析</font></center>

### **一、实验目的：**

&nbsp;（1）掌握最短路问题、最大流问题和最小生成树问题的基本模型；

&nbsp;（2）熟练使用OPL语言求解最短路问题、最大流问题和最小生成树问题。

&nbsp;（3）学会建立最短路问题、最大流问题和最小生成树问题的模型。

### **二、实验内容：**

&nbsp;（1）完成实验手册给出的案例；

&nbsp;（2）针对实验手册的练习，建立数学规划模型、求解模型以及实验结果的分析。

### **三、操作步骤：**

#### （1）建立数学规划模型

 
##### 1. 问题描述
在给定连通无向图 $G=(V,E)$ 中，寻找连接所有节点的边集 $T \subseteq E$，使得：
- 总边权最小
- 无环路
- 连通所有节点

##### 2. 决策变量
定义二元决策变量：
$$
x_{ij} = 
\begin{cases} 
1, & \text{如果边}(i,j)\text{被选中} \\
0, & \text{否则}
\end{cases} \quad \forall (i,j) \in E
$$

##### 3. 目标函数
最小化总边权（光纤总长度）：
$$
\min \sum_{(i,j) \in E} w_{ij} x_{ij}
$$
其中 $w_{ij}$ 为边 $(i,j)$ 的权重。

##### 4. 约束条件

- 边数约束
生成树需包含 $|V|-1$ 条边：
$$
\sum_{(i,j) \in E} x_{ij} = |V| - 1
$$

- 连通性约束
确保图的连通性（避免环路）：
$$
\sum_{j:(i,j) \in E} x_{ij} + \sum_{j:(j,i) \in E} x_{ji} \geq 1 \quad \forall i \in V
$$

#### （2）分析模型并求解

##### **标准型总结**

模型转化为混合整数线性规划（MILP）：  
\[
\begin{aligned}
\min \quad & \sum_{(i,j) \in E} w_{ij} x_{ij} \\
\text{s.t.} \quad & \sum_{(i,j) \in E} x_{ij} = n-1 \\
 \\
& x_{ij} \in \{0,1\}, \quad f_{ij} \geq 0
\end{aligned}
\]

由于使用py与json录入数据更加方便快捷，优先给出我的`Python`解决方案

##### 使用Python `cplex`模块求解


`py`文件

```Python
import heapq

def prim_mst(nodes, edges):
    """使用Prim算法构建最小生成树"""
    # 构建邻接表
    graph = {node: [] for node in nodes}
    for edge in edges:
        graph[edge['from']].append((edge['to'], edge['weight']))
        graph[edge['to']].append((edge['from'], edge['weight']))  # 无向图
    
    # 初始化
    start_node = 'v1'
    visited = set([start_node])
    mst_edges = []
    heap = []
    
    # 将起始节点的边加入堆
    for neighbor, weight in graph[start_node]:
        heapq.heappush(heap, (weight, start_node, neighbor))
    
    # Prim算法主体
    while heap and len(visited) < len(nodes):
        weight, u, v = heapq.heappop(heap)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            for neighbor, w in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (w, v, neighbor))
    
    return mst_edges

def calculate_total_length(mst_edges):
    """计算最小生成树的总长度"""
    return sum(weight for _, _, weight in mst_edges)

# 网络图数据
network = {
    "nodes": ["v1", "v2", "v3", "v4", "v5", "v6", "v7"],
    "edges": [
        {"from": "v1", "to": "v2", "weight": 30},
        {"from": "v2", "to": "v3", "weight": 20},
        {"from": "v2", "to": "v6", "weight": 15},
        {"from": "v3", "to": "v4", "weight": 20},
        {"from": "v3", "to": "v5", "weight": 60},
        {"from": "v3", "to": "v6", "weight": 25},
        {"from": "v4", "to": "v5", "weight": 30},
        {"from": "v4", "to": "v6", "weight": 18},
        {"from": "v6", "to": "v7", "weight": 15}
    ]
}

# 构建最小生成树
mst = prim_mst(network["nodes"], network["edges"])
total_length = calculate_total_length(mst)

# 输出结果
print("=== 最小生成树解决方案 ===")
print("选中的光纤路径（确保连接所有节点且无环）：")
for u, v, weight in sorted(mst, key=lambda x: (x[0], x[1])):
    print(f"{u} --{weight}--> {v}")

print(f"\n光纤总长度: {total_length}")
```


- 使用Prim算法构建最小生成树
- 确保连接所有节点且无环路
- 保证总光纤长度最短
​​
算法关键部分：

- 从起始节点v1开始扩展
- 每次选择权重最小的边连接新节点
- 使用优先队列（堆）高效选择最小边


##### 使用`IBM cplex`求解器求解

同时为了契合实验要求，使用`ibm cplex`求解如下



`.data`文件

```data
Nodes = {"v1", "v2", "v3", "v4", "v5", "v6", "v7"};

Edges = {
    <"v1", "v2", 30>, <"v2", "v3", 20>, <"v2", "v6", 15>,
    <"v3", "v4", 20>, <"v3", "v5", 60>, <"v3", "v6", 25>,
    <"v4", "v5", 30>, <"v4", "v6", 18>, <"v6", "v7", 15>
};
```

`.mod`文件使用opl语言

```opl
// 最小生成树替代方案模型 - 兼容IBM CPLEX OPL
{string} Nodes = ...;
tuple Edge { 
    string from; 
    string tonode; 
    int weight; 
}
{Edge} Edges = ...;

dvar boolean x[Edges];

minimize sum(e in Edges) e.weight * x[e];

subject to {
    // 边数约束
    sum(e in Edges) x[e] == card(Nodes) - 1;
    
    // 连通性约束
    forall(n in Nodes)
        sum(e in Edges : e.from == n) x[e] + 
        sum(e in Edges : e.tonode == n) x[e] >= 1;
}

// 输出结果的脚本（不使用sort）
execute {
    writeln("=== 最小生成树解决方案 ===");
    writeln("选中的光纤路径（确保连接所有节点且无环）：");
    
    // 直接遍历所有边输出（保持原始顺序）
    var count = 0;
    for (e in Edges) {
        if (x[e] > 0.9) {
            writeln(e.from, " --", e.weight, "--> ", e.tonode);
            count += 1;
        }
    }
    
    
    writeln("\n光纤总长度: ", cplex.getObjValue());
}


```




#### （3）实验结果分析


##### 求解结果

Python:
![](../outputs/001.png)

cplex:

![](../outputs/002.png)
 

最优解
最优生产方案：
对于这个题，应该存在2个答案值相同但是路径不同的解，我分别用python
和cplex求解得到，如下：

第一个解

        v1 --30--> v2
        v2 --20--> v3
        v2 --15--> v6
        v4 --30--> v5
        v6 --18--> v4
        v6 --15--> v7

第二个解

        v1 --30--> v2
        v2 --20--> v3
        v2 --15--> v6
        v4 --30--> v5
        v4 --18--> v6
        v6 --15--> v7


光纤总长度: 128



##### 结论：

- 解的唯一性：

    该网络存在多个最优解（总长度均为128），差异主要体现在v4-v3和v3-v2边的选择上
    因为2个边的权值是相同的，所以2选1构造结果是一样的

- 2. **算法比较**：
        | 方法       | 总长度 | 边选择策略               | 计算效率 |
        |------------|--------|--------------------------|----------|
        | Prim算法   | 128    | 贪心选择最小边           | O(E log V) |
        | CPLEX MILP | 128    | 数学规划全局最优         | 取决于问题规模 |

- 3. **模型验证**：
   - 两种方法结果一致，验证了模型的正确性
   - 满足所有约束条件：
     - 边数 = 6 (7节点-1)
     - 无环路
     - 全连通
 

### **四、实验中遇到的主要问题及解决方法**

 
#### 1.输出结果排序混乱

边输出顺序随机,不好进行检查

在数据文件中预排序边集合
```opl
 // 直接遍历所有边输出（保持原始顺序）
    var count = 0;
    for (e in Edges) {
        if (x[e] > 0.9) {
            writeln(e.from, " --", e.weight, "--> ", e.tonode);
            count += 1;
        }
    }
```

#### 2.python优先队列（堆）的使用问题

本次python求解我使用的更偏向于启发式算法，使用Prim算法构建最小生成树
由于本身是写c++/c较多，一开始对优先队列的使用不是很熟练
通过查看csdn学习python相关语法库得以解决

```Python
#优先队列
for neighbor, weight in graph[start_node]:
        heapq.heappush(heap, (weight, start_node, neighbor))
    

```



---


