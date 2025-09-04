# 图像分类项目

这是一个基于 MNIST 数据集的图像分类任务，使用了支持向量机（SVM）、人工神经网络（ANN）和卷积神经网络（CNN）等模型进行分类实验。

## 项目结构

```
工程2+2022303210+刘力豪/
│
├── data/                  # MNIST 数据集
│   └── MNIST/            # 预处理后的数据集
│       └── raw/          # 原始数据文件
├── outputs/              # 训练结果和评估报告
│   └── res.png           # 结果可视化图表
├── src3/                  # 源代码
│   ├── preprocess.py     # 数据预处理脚本
│   ├── svm_experiment.py # SVM 实验脚本
│   ├── ann_experiment.py # ANN 实验脚本 
│   ├── cnn_experiment.py # CNN 实验脚本
│   └── evaluate.py       # 模型评估脚本
├── report/               # 实验报告文档
│   └── 工程2.pdf         # PDF 格式项目报告
├── requirements.txt      # 项目依赖
└── README.md             # 项目说明文件
```

## 安装依赖

```bash
# 创建虚拟环境（Windows PowerShell）
python -m venv venv
venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

## 数据预处理

项目已包含预处理完成的MNIST数据集，路径为：`data/MNIST/`

评估结果将保存在：
- 可视化图表：outputs/res.png

## 结果查看

1. PDF实验报告：report/工程2.pdf
2. 训练过程可视化：outputs/runingres.png
3. 模型对比结果：outputs/res.png
