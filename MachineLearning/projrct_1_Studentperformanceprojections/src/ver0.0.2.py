import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import os

print(os.getcwd())

# 1. 数据加载与预处理
def load_data():
    try:
        mat = pd.read_csv('./data/student-mat.csv', sep=';')
        por = pd.read_csv('./data/student-por.csv', sep=';')
    except FileNotFoundError:
        print("Error: One or both data files are missing.")
        return None
    
    merged = pd.concat([mat, por])
    return merged

# 2. 目标变量处理
def process_target(df):
    for col in ['G1', 'G2', 'G3']:
        df = df[(df[col] >= 0) & (df[col] <= 20)]  # 确保成绩在有效范围
    
    # 将G1, G2, G3按分位数分成5类
    df['G1_class'] = pd.qcut(df['G1'], q=5, labels=False, duplicates='drop')
    df['G2_class'] = pd.qcut(df['G2'], q=5, labels=False, duplicates='drop')
    df['G3_class'] = pd.qcut(df['G3'], q=5, labels=False, duplicates='drop')
    
    print(df['G1_class'].value_counts())
    print(df['G2_class'].value_counts())
    print(df['G3_class'].value_counts())
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    axes[0].hist(df['G1_class'], bins=5, edgecolor='black', alpha=0.7, label="G1 Classes")
    axes[0].set_title('G1 Score Distribution')
    axes[0].legend(title="Score Classes", loc='best')
    
    axes[1].hist(df['G2_class'], bins=5, edgecolor='black', alpha=0.7, label="G2 Classes")
    axes[1].set_title('G2 Score Distribution')
    axes[1].legend(title="Score Classes", loc='best')
    
    axes[2].hist(df['G3_class'], bins=5, edgecolor='black', alpha=0.7, label="G3 Classes")
    axes[2].set_title('G3 Score Distribution')
    axes[2].legend(title="Score Classes", loc='best')
    
    plt.tight_layout()
    plt.savefig('./outputs/score_distributions02.png')
    plt.close()
    
    return df

# 3. 特征工程
def prepare_features(df):
    base_features = [
        'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
        'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures',
        'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet',
        'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences'
    ]
    
    feature_sets = {
        'G1_features': base_features,
        'G2_features': base_features + ['G1'],
        'G3_features': base_features + ['G1', 'G2']
    }
    
    return feature_sets

# 4. 模型训练与评估
def evaluate_models(X, y):
    models = [
        ('KNN', KNeighborsClassifier(n_neighbors=10, weights='distance')),
        ('Logistic Regression', LogisticRegression(
            max_iter=5000,  # 增加最大迭代次数
            solver='lbfgs',  # 尝试使用lbfgs优化器
            penalty='l2',  # 使用L2正则化
            random_state=42,
            class_weight='balanced'  # 处理类别不平衡
        )),
        ('Decision Tree', DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42))
    ]
    
    results = {}
    for name, model in models:
        scores = cross_val_score(model, X, y, cv=5)
        results[name] = np.mean(scores)  # 存储平均准确率
    
    return results

# 5. 超参数调优 - 改进逻辑回归
def tune_logistic_regression(X, y):
    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10],  # 调整正则化参数C
        'penalty': ['l2'],  # 使用L2正则化
        'solver': ['lbfgs'],  # 使用lbfgs优化器
        'max_iter': [5000]  # 增加迭代次数
    }
    grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5)
    grid_search.fit(X, y)
    return grid_search.best_params_, grid_search.best_score_

# 主流程
def main():
    df = load_data()
    if df is None:
        return

    df = process_target(df)
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
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 对KNN进行模型训练
        results = evaluate_models(X_scaled, y)
        results['Task'] = task_name
        final_results.append(results)
        
        # 对逻辑回归进行超参数调优
        if task_name == 'Predict G1':  
            best_params, best_score = tune_logistic_regression(X_scaled, y)
            print(f"Best Logistic Regression parameters for {task_name}: {best_params}")
            print(f"Best Logistic Regression score for {task_name}: {best_score}")
    
    result_df = pd.DataFrame(final_results)
    print(result_df)
    
    # 确保 Task 列保留并进行图形绘制
    result_df.set_index('Task', inplace=True)
    
    # 只针对数值型列计算标准差并绘图
    result_df.plot(kind='bar', yerr=result_df.std(), figsize=(12, 6))
    plt.title('Model Performance Comparison')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./outputs/results_comparison02.png')

if __name__ == "__main__":
    main()
