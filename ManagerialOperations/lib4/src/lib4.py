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