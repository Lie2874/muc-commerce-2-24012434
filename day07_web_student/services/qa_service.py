import pandas as pd
import re

def answer_question(question, df):
    """离线问答服务"""
    question_lower = question.lower()
    
    # 总体规模
    if any(kw in question_lower for kw in ['多少用户', '用户数', '总用户', 'total']):
        total = len(df)
        return f"系统中共有 {total} 位用户。"
    
    # 流失情况
    if any(kw in question_lower for kw in ['流失率', '流失', 'churn']):
        total = len(df)
        churn = df['Churn'].sum()
        rate = (churn / total * 100) if total > 0 else 0
        return f"共有 {int(churn)} 位用户流失，流失率为 {rate:.2f}%。"
    
    # 偏好品类
    if any(kw in question_lower for kw in ['品类', '最多', '热门', 'popular']):
        if 'PreferedOrderCat' in df.columns:
            top_cat = df['PreferedOrderCat'].value_counts().idxmax()
            top_count = df['PreferedOrderCat'].value_counts().max()
            return f"用户最多的品类是 {top_cat}，共有 {top_count} 位用户。"
        return "暂无品类数据。"
    
    # 生命周期
    if any(kw in question_lower for kw in ['生命周期', 'tenure', '阶段', '风险', 'highest']):
        if 'TenureGroup' in df.columns:
            highest_risk = None
            highest_rate = 0
            for group in df['TenureGroup'].dropna().unique():
                group_df = df[df['TenureGroup'] == group]
                rate = group_df['Churn'].mean() * 100
                if rate > highest_rate:
                    highest_rate = rate
                    highest_risk = group
            return f"流失率最高的生命周期阶段是 {highest_risk}，流失率为 {highest_rate:.2f}%。"
        return "暂无生命周期数据。"
    
    # 订单情况
    if any(kw in question_lower for kw in ['订单', 'order', '平均订单', '中位数']):
        if 'OrderCount' in df.columns:
            avg = df['OrderCount'].mean()
            median = df['OrderCount'].median()
            return f"平均订单数为 {avg:.2f}，中位数为 {median}。"
        return "暂无订单数据。"
    
    # 优惠券
    if any(kw in question_lower for kw in ['优惠券', 'coupon']):
        if 'CouponUsed' in df.columns:
            avg = df['CouponUsed'].mean()
            total = df['CouponUsed'].sum()
            return f"平均每位用户使用 {avg:.2f} 张优惠券，总计使用 {int(total)} 张。"
        return "暂无优惠券数据。"
    
    # 返现
    if any(kw in question_lower for kw in ['返现', 'cashback']):
        if 'CashbackAmount' in df.columns:
            avg = df['CashbackAmount'].mean()
            total = df['CashbackAmount'].sum()
            return f"平均返现金额为 {avg:.2f} 元，总计返现 {total:.2f} 元。"
        return "暂无返现数据。"
    
    # 不支持的问题
    return "抱歉，我暂时无法回答这个问题。请尝试询问用户数、流失率、品类、生命周期、订单、优惠券或返现相关的问题。"
