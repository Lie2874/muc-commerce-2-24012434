from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
from services.data_service import get_dashboard_data, get_filtered_data
from services.qa_service import answer_question

app = Flask(__name__)
app.secret_key = 'ecommerce_day07_secret_key_24012434'

# 加载清洗后的数据
DATA_PATH = '../output/day04_project/ecommerce_customer_cleaned.csv'
df = pd.read_csv(DATA_PATH)

# 演示账号
DEMO_USER = 'student'
DEMO_PASS = 'day07'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == DEMO_USER and password == DEMO_PASS:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    category = request.args.get('category', 'all')
    
    # 获取所有品类
    all_categories = df['PreferedOrderCat'].unique().tolist()
    all_categories.sort()
    
    # 根据筛选条件获取数据
    if category == 'all':
        dashboard_data = get_dashboard_data(df)
    else:
        filtered_df = get_filtered_data(df, category)
        dashboard_data = get_dashboard_data(filtered_df)
    
    return render_template('dashboard.html', 
                         data=dashboard_data,
                         categories=all_categories,
                         selected_category=category)

@app.route('/api/ask', methods=['POST'])
def ask():
    if not session.get('logged_in'):
        return jsonify({'error': '未登录'}), 401
    
    question = request.json.get('question', '')
    answer = answer_question(question, df)
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
