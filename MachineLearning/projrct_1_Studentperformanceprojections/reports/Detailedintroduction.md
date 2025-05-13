# **学生表现预测**


## Author: Liulanker  Date:2025-04-16
---

## **1. 问题描述**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本次工程要求基于学生的个人特征与历史成绩来预测学生在不同科目中的表现。任务的数据集包含33个特征，共649个样本。目标是通过这些特征预测学生在G1、G2和G3上的表现，并将这些成绩按0-20的范围划分为五个类别。基于任务要求，使用以下模型进行预测和对比：近邻法、逻辑回归以及决策树。

---


## **2. 方法**

### **2.1 数据预处理**

1. 根据[student-merge.R](./data/student-merge.R)文件中对R语言代码：
```R
d1=read.table("student-mat.csv",sep=";",header=TRUE)
d2=read.table("student-por.csv",sep=";",header=TRUE)

d3=merge(d1,d2,by=c("school","sex","age","address","famsize","Pstatus","Medu","Fedu","Mjob","Fjob","reason","nursery","internet"))
print(nrow(d3)) 
 
```
分析如下：
 
- **`read.table`**：该函数用于读取文件中的数据，并将其加载为数据框（data frame）。
  - `sep=";"`：指定数据文件中的列分隔符为分号（`;`）。这意味着 CSV 文件的每列是由分号分隔的，而不是逗号。
  - `header=TRUE`：表示数据文件的第一行包含列名（即表头），R 会将这一行自动识别为列名，而不是数据的一部分。

这两行代码分别读取了两个数据文件 `student-mat.csv` 和 `student-por.csv`，并将它们存储为数据框 `d1` 和 `d2`。

```R
d3 = merge(d1, d2, by = c("school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet"))
```

- **`merge`**：这个函数用于合并两个数据框。在这里，`d1` 和 `d2` 数据框被按指定的列进行合并。
  - `by=c("school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet")`：表示根据这13个列名进行合并。也就是说，R会根据这些列中每一对相同的值来连接两个数据框的行。
  - `d1` 和 `d2` 必须在这些列上具有匹配的值才能成功合并。如果某行在这13个列中的任意一列没有匹配项，那么该行就不会出现在合并后的数据框 `d3` 中。

`d1` 和 `d2` 数据框根据这些关键列进行内连接合并，生成一个新的数据框 `d3`。
 
- **`nrow(d3)`**：此函数用于获取数据框 `d3` 的行数，也就是合并后的数据框中包含的样本数。
- **`print`**：用于显示 `d3` 数据框的行数，即合并后的学生数据数量。



2.初代算法实现代码

[ver0.0.1.py](./src/ver0.0.1.py)

通过 `pd.read_csv()` 函数加载数据集，并根据任务要求对成绩（G1、G2、G3）进行等频分箱处理，将其划分为5个类别，确保成绩在0-20的范围内。具体分箱方式使用 `pd.qcut()`，它可以按分位数将成绩数据等分成5组。然后将数据按30个特征进行划分，去除G1、G2、G3列，只保留其余30个特征来训练预测模型。

#### **2.2 特征选择**
特征选择部分使用给定的30个特征进行模型训练，并根据任务要求，利用不同的特征集进行多步预测：
- **G1预测**：只使用前30个特征。
- **G2预测**：使用前30个特征和G1作为特征。
- **G3预测**：使用前30个特征和G1、G2作为特征。

#### **2.3 模型选择**
本算法选用了以下三种模型来进行预测：

1. **KNN**：通过近邻法预测学生的成绩，选择了 `n_neighbors=10` 和 `weights='distance'` 作为默认参数，并使用交叉验证评估其准确性。

    代码参考了csdn博客：
    [KNN](https://blog.csdn.net/m0_74405427/article/details/133714384?fromshare=blogdetail&sharetype=blogdetail&sharerId=133714384&sharerefer=PC&sharesource=LLH004&sharefrom=from_link)

2. **逻辑回归**：使用弹性网络正则化来训练模型，通过最大迭代次数设置为2000，以确保收敛。

    优化后的第二代代码[ver0.0.2.py](./src/ver0.0.2.py)，尝试了更大的最大迭代次数（max_iter=5000）并修改了求解器（solver='lbfgs'）来进一步优化模型。


3. **决策树**：使用决策树`DecisionTreeClassifier`来自 `sklearn.tree `库的一个类，用于分类任务的决策树模型
设定了树的最大深度为5，并限制最小样本分裂数为10。
主要的决策树算法为：
CART:一个二叉树的生成算法，每个节点都根据某个特征的最佳切分点将数据分成两个子集。在分类问题中，CART使用基尼指数作为划分标准。  
代码参考:
[机器学习：DecisionTreeClassifier决策树模型](https://blog.csdn.net/Wei_sx/article/details/144651991?fromshare=blogdetail&sharetype=blogdetail&sharerId=144651991&sharerefer=PC&sharesource=LLH004&sharefrom=from_link)


在本实验中，生成的决策树如下所示：
代码:[buildtreemod](./src/buildtree.py)
![决策树模型可视化](./outputs/decision_tree_visualization.png)


![决策树模型对比](./outputs/decision_tree_comparison.png)

#### **2.4 模型训练与评估**
每个模型使用[5折交叉验证](https://blog.csdn.net/Algernon98/article/details/125128281?fromshare=blogdetail&sharetype=blogdetail&sharerId=125128281&sharerefer=PC&sharesource=LLH004&sharefrom=from_link)来评估其性能，并记录每个任务（G1、G2、G3）的预测准确率

在代码中，cross_val_score 用于进行5折交叉验证，返回了一个包含5个分数的数组，每个分数对应一次训练和验证过程的准确率。最后的 np.mean(scores) 计算了这5次测试的平均准确率，作为模型的最终评估结果。

---

## **3. 实验结果**

以下是三个模型在预测G1、G2和G3上的表现：

| Task        | KNN  | Logistic Regression | Decision Tree |
|-------------|------|---------------------|---------------|
| Predict G1  | 0.340 | 0.329532            | 0.322828      |
| Predict G2  | 0.335 | 0.517225            | 0.563181      |
| Predict G3  | 0.401 | 0.647516            | 0.716447      |

运行结果如下：
![](./outputs/score_distributions01.png)

![](./outputs/score_distributions02.png)

分析结果中可以得：
- 在G3的预测任务中，**决策树模型**表现最好，其准确率为0.716。
- 对于G1和G2的预测，**KNN模型**在G1和G2任务中略好，但整体差距不大。
- **逻辑回归**模型的表现相对较差，特别是在G1和G2任务中，其准确率较低。


---

## **4.问题思考**

### 4.1逻辑回归的参数调整

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;考虑到在[ver0.0.1.py](./ver0.0.1.py)的运行求解结果的过程中，出现了：
```bash
D:\CodingEvn\Python3.10\lib\site-packages\sklearn\linear_model\_sag.py:348: ConvergenceWarning: The max_iter was reached which means the coef_ did not converge
  warnings.warn(
Best Logistic Regression parameters for Predict G1: {'C': 0.01, 'max_iter': 2000, 'penalty': 'l2', 'solver': 'saga'}
Best Logistic Regression score for Predict G1: 0.34674273095325725

```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这意味在参数迭代为 &nbsp; `2000` &nbsp;次数内未能完全收敛，因此对`evaluate_models(X, y)`算法优化并调参，增加最大次数为5000次；
```Python
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



```

得到了如下输出:

#### **第一次参数优化（对比ver0.0.1结果）**

| Task        | KNN  | Logistic Regression | Decision Tree |
|-------------|------|---------------------|---------------|
| Predict G1  | 0.340 | 0.329532            | 0.322828      |
| Predict G2  | 0.335 | 0.517225            | 0.563181      |
| Predict G3  | 0.401 | 0.647516            | 0.716447      |

 
- **逻辑回归模型**在调整超参数后，略有优化，在G1预测中的准确率从0.332上升至0.329532，但并没有显著提升。
 


### 4.2 决策树的构建与可视

![](./outputs/decision_tree_comparison.png)

准确率比较： 从准确率比较图来看，决策树模型在三个任务（预测 G1、预测 G2、预测 G3）中的表现有所不同。具体表现如下：

预测 G1：准确率最低，大约为 0.3。（ 0.322828）  

预测 G2：准确率略有提升，大约为 0.5。（ 0.563181  ）  

预测 G3：准确率最高，大约为 0.7。（0.716447 ）  

 
![](./outputs/decision_tree_visualization.png)


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;表现了模型在不同特征（如 G2、G1、absences、famsize 等）上的分裂。每一个分裂节点代表模型根据特征的阈值做出的决策。例如，根节点使用 G2 <= 0.077 进行决策，接下来的节点分别依据 absences、famsize、health 等特征进行分裂。决策树包含了多个分支，导致不同的预测结果（例如 y0、y1、y2 等）。

- 可以看到 G2、G1 和 absences 是决定最终分类的重要特征



---

## **5. 结果讨论**

从实验结果可以看到，不同的模型在不同的任务上有不同的表现：

- **KNN模型**在G1和G2的预测中较为准确，可能是由于其能够较好地捕捉到样本之间的相似性。

- **逻辑回归**在所有任务中表现较差，尤其是在G1和G2的任务中。可能是由于其假设特征之间是线性可分的，但在这个数据集中，这一假设不完全成立。

- **决策树模型**在G3任务中表现最好，这表明决策树对具有更多特征（如G1和G2）的任务能够做出更有效的分割，可能是因为它能自动选择对结果影响较大的特征进行分裂。
---


---

## **6. 结论**

通过实验可以得出以下结论：

- **KNN模型**适合于任务G1和G2，尤其是在没有太多特征时，KNN能够较好地利用相似数据进行预测。
- **逻辑回归**模型表现不佳，即使我进行了代码更新将迭代参数优化，其在5折交叉验证中的反馈变化不大，分析原因，可能是因为数据的特征之间没有足够的线性关系，导致该模型在处理这些数据时受到限制。
- **决策树**在任务G3中表现最佳，可能是由于其在处理多特征和复杂关系时具有更强的建模能力。



---

Author: **liulanker**  
Date: 2025-03-30  
Contact: liulanker@gmail.com
 