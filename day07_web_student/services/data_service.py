import pandas as pd

def get_dashboard_data(df):
    """获取看板数据"""
    # 基础指标
    total_users = len(df)
    churn_users = df['Churn'].sum()
    churn_rate = (churn_users / total_users * 100) if total_users > 0 else 0
    avg_orders = df['OrderCount'].mean() if 'OrderCount' in df.columns else 0
    avg_coupon = df['CouponUsed'].mean() if 'CouponUsed' in df.columns else 0
    avg_cashback = df['CashbackAmount'].mean() if 'CashbackAmount' in df.columns else 0
    
    # 按生命周期分组的流失率
    segment_data = []
    if 'TenureGroup' in df.columns:
        for group in sorted(df['TenureGroup'].dropna().unique()):
            group_df = df[df['TenureGroup'] == group]
            group_churn_rate = group_df['Churn'].mean() * 100
            segment_data.append({
                'stage': group,
                'count': len(group_df),
                'churn_rate': group_churn_rate
            })
    
    # 找到流失率最高的阶段
    highest_risk_stage = None
    highest_risk_rate = 0
    for seg in segment_data:
        if seg['churn_rate'] > highest_risk_rate:
            highest_risk_rate = seg['churn_rate']
            highest_risk_stage = seg['stage']
    
    # 品类分布
    category_data = []
    if 'PreferedOrderCat' in df.columns:
        cat_counts = df['PreferedOrderCat'].value_counts().head(5)
        for cat, count in cat_counts.items():
            cat_rate = (count / total_users * 100) if total_users > 0 else 0
            category_data.append({
                'category': cat,
                'count': count,
                'percentage': cat_rate
            })
    
    return {
        'total_users': int(total_users),
        'churn_users': int(churn_users),
        'churn_rate': round(churn_rate, 2),
        'avg_orders': round(avg_orders, 2),
        'avg_coupon': round(avg_coupon, 2),
        'avg_cashback': round(avg_cashback, 2),
        'segment_data': segment_data,
        'highest_risk_stage': highest_risk_stage,
        'highest_risk_rate': round(highest_risk_rate, 2),
        'category_data': category_data,
        'top_category': category_data[0]['category'] if category_data else 'N/A'
    }

def get_filtered_data(df, category):
    """根据品类筛选数据"""
    return df[df['PreferedOrderCat'] == category]
