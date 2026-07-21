# Day 9 Flask实训项目：校园二手交易平台

## 学生信息

- 姓名：金睿博
- 学号：24012434

## 项目说明

这是一个基于Flask的校园二手物品交易平台，学生可以发布闲置物品、浏览商品、搜索商品、查看商品详情。

## 核心功能

1. **发布商品** - 使用 `request.form` 和 `request.files` 处理表单和图片上传
2. **商品列表** - 支持分类筛选和价格排序
3. **商品搜索** - 使用 `request.args.get("keyword")` 实现关键词搜索
4. **商品详情** - 使用动态路由 `/product/<id>` 展示商品信息

## 技术栈

- **后端**：Flask + SQLite
- **前端**：HTML + CSS + JavaScript
- **数据库**：SQLite（零配置，文件型数据库）

## 运行方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

浏览器访问 `http://localhost:5000`

## 项目结构

```
day09_marketplace/
├── app.py                    # Flask主应用
├── services/
│   ├── __init__.py
│   └── database.py           # 数据库操作
├── templates/
│   ├── base.html             # 基础模板
│   ├── index.html            # 首页（商品列表）
│   ├── publish.html          # 发布商品
│   ├── product_detail.html   # 商品详情
│   └── search.html           # 搜索结果
├── static/
│   ├── css/style.css         # 样式文件
│   └── uploads/              # 上传图片存储
├── data/
│   └── marketplace.db        # SQLite数据库（自动生成）
└── requirements.txt          # 依赖列表
```

## 核心考点

| 功能 | Flask知识点 |
|------|------------|
| 发布商品 | `request.form` 获取表单数据，`request.files` 处理文件上传 |
| 商品列表 | 模板渲染，`request.args` 获取查询参数 |
| 商品搜索 | `request.args.get("keyword")` |
| 商品详情 | 动态路由 `/product/<int:product_id>` |

## 预置数据

首次运行时会自动创建数据库并插入6条测试数据：
- 二手iPhone 13（数码）
- 机械键盘Cherry MX（数码）
- Python编程从入门到实践（书籍）
- 台灯（日用品）
- Nike运动鞋（服饰）
- iPad Air 4（数码）

## 演示要点

1. 访问首页查看商品列表和统计数据
2. 使用分类筛选和排序功能
3. 搜索商品（如搜索"iPhone"）
4. 点击商品查看详情
5. 发布新商品（填写表单、上传图片）
6. 验证新商品出现在列表中
