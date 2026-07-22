# 第9天学生项目：机器学习零基础数据准备

## 运行方法

```bash
python -m pip install -r requirements.txt
python validate_day09_environment.py
jupyter lab
```

打开`notebooks/day09_ml_preparation_student.ipynb`。Notebook已经提供完整处理骨架，你只需完成少量关键填空、运行检查点并撰写解释。

## 学生信息

- 姓名：金睿博
- 学号：24012434
- 班级：中央民族大学

## 用自己的话回答

- 什么是特征，什么是标签：特征是从每条数据中提取的信息（如Tenure、Complain），标签是我们想要预测的目标（Churn是否流失）。
- 为什么要保留测试集：测试集模拟没有见过的新用户，用来检验模型是否真正学到了规律，而不是对训练数据过拟合。
- 为什么83%准确率仍可能没有用：因为最低参照线永远预测多数类（未流失），召回率为0，一个流失用户都没找到。准确率高只是因为数据中流失用户占比低，对识别流失毫无价值。
