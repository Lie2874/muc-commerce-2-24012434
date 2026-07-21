from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from services.database import (
    init_db,
    get_all_products,
    get_product_by_id,
    search_products,
    add_product,
    get_product_count,
    get_category_counts,
    CATEGORIES
)

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = "campus_marketplace_secret_key_2024"

# 配置
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# 确保上传目录存在
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# 初始化数据库
init_db()


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """保存上传的文件，返回文件名"""
    if file and file.filename and allowed_file(file.filename):
        # 生成唯一文件名
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = UPLOAD_FOLDER / unique_name
        file.save(file_path)
        return unique_name
    return None


# ==================== 路由 ====================

@app.route("/")
def index():
    """首页 - 显示商品列表和统计信息"""
    # 获取筛选和排序参数
    category = request.args.get("category", "全部")
    sort_by = request.args.get("sort", "newest")
    
    # 获取商品列表
    products = get_all_products(category, sort_by)
    
    # 获取统计数据
    total_count = get_product_count()
    category_counts = get_category_counts()
    
    return render_template(
        "index.html",
        products=products,
        categories=CATEGORIES,
        selected_category=category,
        sort_by=sort_by,
        total_count=total_count,
        category_counts=category_counts
    )


@app.route("/publish", methods=["GET", "POST"])
def publish():
    """发布商品页面"""
    if request.method == "POST":
        # 获取表单数据
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        price_str = request.form.get("price", "").strip()
        contact = request.form.get("contact", "").strip()
        description = request.form.get("description", "").strip()
        
        # 验证必填项
        if not all([name, category, price_str, contact]):
            flash("请填写所有必填项", "error")
            return redirect(url_for("publish"))
        
        # 验证价格
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            flash("价格必须是大于0的数字", "error")
            return redirect(url_for("publish"))
        
        # 处理图片上传
        image_file = request.files.get("image")
        image_path = None
        if image_file and image_file.filename:
            saved_name = save_uploaded_file(image_file)
            if saved_name:
                image_path = saved_name
            else:
                flash("图片格式不支持，请上传 png/jpg/gif 格式", "error")
                return redirect(url_for("publish"))
        
        # 添加到数据库
        product_id = add_product(name, category, price, contact, description, image_path)
        flash(f"商品发布成功！ID: {product_id}", "success")
        return redirect(url_for("index"))
    
    # GET请求显示表单
    return render_template("publish.html", categories=CATEGORIES)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    """商品详情页"""
    product = get_product_by_id(product_id)
    if not product:
        flash("商品不存在", "error")
        return redirect(url_for("index"))
    
    return render_template("product_detail.html", product=product)


@app.route("/search")
def search():
    """搜索商品"""
    keyword = request.args.get("keyword", "").strip()
    
    if not keyword:
        flash("请输入搜索关键词", "error")
        return redirect(url_for("index"))
    
    # 搜索商品
    products = search_products(keyword)
    
    return render_template(
        "search.html",
        products=products,
        keyword=keyword
    )


# ==================== 启动应用 ====================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
