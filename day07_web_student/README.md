# 电商用户分析系统 - Day 07

## 项目信息

- **学生姓名**: 金睿博
- **学号**: 24012434
- **日期**: 2026年7月

## 项目概述

基于 Flask 框架构建的电商用户行为分析 Web 系统，集成数据清洗、可视化展示和智能问答功能。

## 核心功能

### 1. 用户登录系统
- 演示账号: `student`
- 密码: `day07`
- 支持 Session 管理和登出功能

### 2. 数据看板
- **4个核心指标卡**: 总用户数、流失用户、总体流失率、平均订单数
- **数据表格**: 展示生命周期各阶段用户数和流失率
- **数据观察**: 自动识别流失率最高的生命周期阶段

### 3. 品类筛选
- 支持按 `PreferedOrderCat` 字段筛选数据
- URL 参数: `?category=品类名称`
- 筛选后实时更新所有指标和表格

### 4. 智能问答
- 支持自然语言提问
- 可回答的问题类型:
  - 用户总数: "系统中有多少用户？"
  - 流失情况: "总体流失率是多少？"
  - 品类分析: "哪个品类用户最多？"
  - 生命周期: "哪个阶段风险最高？"
  - 订单情况: "平均订单数是多少？"
  - 优惠券: "平均使用多少优惠券？"
  - 返现: "平均返现金额是多少？"

## 拓展功能

**已完成拓展A: 导出当前筛选结果**

### 功能说明
- 新增 `/download` 路由
- 支持导出当前筛选品类的数据为 CSV 文件
- 访问方式: `/download?category=品类名称`
- 文件名格式: `ecommerce_品类名称_data.csv`

### 使用示例
- 导出全部数据: `/download?category=all`
- 导出特定品类: `/download?category=Mobile Phone`

## 技术栈

- **后端**: Flask 3.0.0
- **数据处理**: Pandas 2.2.2
- **前端**: HTML5 + CSS3 + JavaScript
- **可视化**: Matplotlib (Day 06 生成)

## 运行方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用
```bash
python app.py
```

### 3. 访问系统
浏览器打开: http://127.0.0.1:5000

## 项目结构

```
day07_web_student/
├── app.py                    # 主应用入口
├── services/
│   ├── __init__.py
│   ├── data_service.py       # 数据处理服务
│   └── qa_service.py         # 问答服务
├── templates/
│   ├── base.html             # 基础模板
│   ├── login.html            # 登录页面
│   └── dashboard.html        # 数据看板
├── static/
│   └── images/               # 可视化图表
├── data/
│   └── ecommerce_customer_cleaned.csv  # 清洗后数据
└── README.md
```

## 数据来源

- **原始数据**: E Commerce Dataset.xlsx (5630条用户记录)
- **清洗处理**: Day 04 完成数据清洗和预处理
- **可视化图表**: Day 06 使用 Matplotlib 生成

## 截图

请查看 `screenshots/` 目录获取功能截图。
