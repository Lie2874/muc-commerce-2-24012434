"""Day 8 Flask API 测试"""
import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


def test_health_endpoint():
    """测试健康检查接口"""
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
        assert data['service'] == 'day08-flask-upgrade'
        print("✓ 测试1: 健康检查接口通过")


def test_metrics_api_requires_login():
    """测试指标接口需要登录"""
    with app.test_client() as client:
        response = client.get('/api/metrics')
        assert response.status_code == 302  # 重定向到登录页
        print("✓ 测试2: 指标接口需要登录验证通过")


def test_metrics_api_after_login():
    """测试登录后可以访问指标接口"""
    with app.test_client() as client:
        # 先登录
        client.post('/login', data={'username': 'student', 'password': 'day07'})
        
        # 访问指标接口
        response = client.get('/api/metrics')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
        assert 'metrics' in data
        assert len(data['metrics']) == 4  # 四个指标卡
        
        # 验证每个指标都有 label、value、note
        for metric in data['metrics']:
            assert 'label' in metric
            assert 'value' in metric
            assert 'note' in metric
        
        print("✓ 测试3: 登录后指标接口返回正确数据")


def test_categories_api():
    """测试品类筛选接口"""
    with app.test_client() as client:
        # 登录
        client.post('/login', data={'username': 'student', 'password': 'day07'})
        
        # 测试全部品类
        response = client.get('/api/categories?category=全部')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
        assert 'rows' in data
        assert len(data['rows']) > 0
        
        # 测试特定品类
        response = client.get('/api/categories?category=Mobile Phone')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
        
        print("✓ 测试4: 品类筛选接口通过")


def test_ask_api():
    """测试问答接口"""
    with app.test_client() as client:
        # 登录
        client.post('/login', data={'username': 'student', 'password': 'day07'})
        
        # 测试提问
        response = client.post('/api/ask', 
                              data=json.dumps({'question': '有多少用户？'}),
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
        assert 'answer' in data
        assert '用户' in data['answer']
        
        # 测试空问题
        response = client.post('/api/ask',
                              data=json.dumps({'question': ''}),
                              content_type='application/json')
        assert response.status_code == 400
        
        print("✓ 测试5: 问答接口通过")


if __name__ == '__main__':
    print("开始运行 Day 8 测试...\n")
    try:
        test_health_endpoint()
        test_metrics_api_requires_login()
        test_metrics_api_after_login()
        test_categories_api()
        test_ask_api()
        print("\n✅ 所有测试通过！")
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        sys.exit(1)
