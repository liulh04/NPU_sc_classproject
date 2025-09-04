import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import StandardScaler
import os

# 1. 数据加载与预处理
def load_data():
    try:
        mat = pd.read_csv('./data/student-mat.csv', sep=';')
        por = pd.read_csv('./data/student-por.csv', sep=';')

    except FileNotFoundError:
        print("Error: One or both data files are missing.")
        return None
    
    merged = pd.concat([mat, por])  # 合并两个数据框
    return merged

# 2. 目标变量处理
def process_target(df):
    # 过滤成绩在0到20之间的记录
    for col in ['G1', 'G2', 'G3']:
        df = df[(df[col] >= 0) & (df[col] <= 20)]  
    
    # 将成绩按分位数划分为5类
    df['G1_class'] = pd.qcut(df['G1'], q=5, labels=False, duplicates='drop')
    df['G2_class'] = pd.qcut(df['G2'], q=5, labels=False, duplicates='drop')
    df['G3_class'] = pd.qcut(df['G3'], q=5, labels=False, duplicates='drop')
    
    return df

# 3. 特征工程
def prepare_features(df):
    base_features = [
        'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
        'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures',
        'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet',
        'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences'
    ]
    
    # 使用不同的特征集合来训练不同任务
    feature_sets = {
        'G1_features': base_features,
        'G2_features': base_features + ['G1'],
        'G3_features': base_features + ['G1', 'G2']
    }
    
    return feature_sets

# 4. 决策树模型训练与评估
def evaluate_decision_tree(X, y):
    # 初始化决策树分类器
    dtree = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
    
    # 训练模型
    dtree.fit(X, y)
    
    # 进行交叉验证，评估模型表现
    scores = cross_val_score(dtree, X, y, cv=5)  # 使用5折交叉验证
    return dtree, np.mean(scores)  # 返回训练好的决策树和平均准确率

# 5. 可视化决策树
def plot_decision_tree(dtree, feature_names):
    plt.figure(figsize=(20, 10))
    plot_tree(dtree, filled=True, feature_names=feature_names, class_names=True, rounded=True, fontsize=12)
    plt.title("Decision Tree Visualization")
    plt.tight_layout()
    plt.savefig('./outputs/decision_tree_visualization.png')
    plt.show()

# 主流程
def main():
    # 加载数据
    df = load_data()
    if df is None:
        return

    # 数据预处理
    df = process_target(df)
    
    # 准备特征集
    feature_sets = prepare_features(df)
    
    tasks = [
        ('Predict G1', 'G1_class', feature_sets['G1_features']),
        ('Predict G2', 'G2_class', feature_sets['G2_features']),
        ('Predict G3', 'G3_class', feature_sets['G3_features'])
    ]
    
    final_results = []
    
    for task_name, target, features in tasks:
        X = pd.get_dummies(df[features])  # 处理分类变量
        y = df[target]
        
        # 获取处理后的特征名称
        feature_names = X.columns
        
        # 特征缩放
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 对决策树模型进行训练和评估
        dtree, accuracy = evaluate_decision_tree(X_scaled, y)
        result = {
            'Task': task_name,
            'Decision Tree Accuracy': accuracy
        }
        final_results.append(result)
        
        # 可视化决策树
        plot_decision_tree(dtree, feature_names)
    
    result_df = pd.DataFrame(final_results)
    print(result_df)

    # 创建目录 ../outputsc （如果不存在的话）
    os.makedirs('./outputs', exist_ok=True)

    # 生成图形并保存到 ./outputs 目录
    result_df.set_index('Task', inplace=True)
    result_df.plot(kind='bar', figsize=(12, 6))
    plt.title('Decision Tree Model Accuracy Comparison')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 保存到 ./outputs 目录下
    plt.savefig('./outputs/decision_tree_comparison.png')
    plt.show()

if __name__ == "__main__":
    main()
