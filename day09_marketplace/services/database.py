import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).parent.parent / "data" / "marketplace.db"

# 分类列表
CATEGORIES = ["数码", "书籍", "日用品", "服饰", "其他"]

def init_db():
    """初始化数据库，创建表并插入预置数据"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建商品表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            contact TEXT NOT NULL,
            description TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # 插入预置测试数据
        sample_products = [
            ("二手iPhone 13", "数码", 2500.0, "13800138001", 
             "使用一年，九成新，无划痕，配件齐全", "iphone13.jpg"),
            ("机械键盘Cherry MX", "数码", 350.0, "13800138002", 
             "青轴，手感很好，因为换了新键盘所以出", "keyboard.jpg"),
            ("Python编程从入门到实践", "书籍", 25.0, "13800138003", 
             "第三版，几乎全新，适合Python入门", "python_book.jpg"),
            ("台灯", "日用品", 30.0, "13800138004", 
             "LED护眼台灯，三档调节亮度", "lamp.jpg"),
            ("Nike运动鞋", "服饰", 180.0, "13800138005", 
             "42码，穿过几次，九成新", "nike_shoes.jpg"),
            ("iPad Air 4", "数码", 3200.0, "13800138006", 
             "64G，Wi-Fi版，带Apple Pencil", "ipad.jpg")
        ]
        
        cursor.executemany("""
            INSERT INTO products (name, category, price, contact, description, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_products)
    
    conn.commit()
    conn.close()

def get_all_products(category=None, sort_by="newest"):
    """获取所有商品，支持分类筛选和排序"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM products"
    params = []
    
    # 分类筛选
    if category and category != "全部":
        query += " WHERE category = ?"
        params.append(category)
    
    # 排序
    if sort_by == "price_asc":
        query += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        query += " ORDER BY price DESC"
    else:  # newest
        query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    products = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return products

def get_product_by_id(product_id):
    """根据ID获取商品详情"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    conn.close()
    
    if product:
        return dict(product)
    return None

def search_products(keyword):
    """根据关键词搜索商品名称"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM products 
        WHERE name LIKE ? 
        ORDER BY created_at DESC
    """, (f"%{keyword}%",))
    
    products = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return products

def add_product(name, category, price, contact, description, image_path):
    """添加新商品"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO products (name, category, price, contact, description, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, category, price, contact, description, image_path))
    
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return product_id

def get_product_count():
    """获取商品总数"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

def get_category_counts():
    """获取各分类商品数量"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM products 
        GROUP BY category 
        ORDER BY count DESC
    """)
    
    counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    return counts
