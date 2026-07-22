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

- 什么是特征，什么是标签：特征是判断时可以查看的信息，标签是希望预测的目标。
- 为什么要保留测试集：测试集模拟没有见过的新用户，用来检验模型效果。
- 为什么83%准确率仍可能没有用：如果模型永远预测多数类，准确率也能达到83%，但无法识别流失用户。
