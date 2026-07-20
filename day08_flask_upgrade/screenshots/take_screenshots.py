import os
import time
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = "http://127.0.0.1:5500"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # 1. 登录页
        print("截图1: 登录页...")
        page.goto(f"{BASE}/login")
        time.sleep(1)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "01_login.png"))

        # 登录
        page.fill("input[name='username']", "student")
        page.fill("input[name='password']", "day07")
        page.click("button[type='submit']")
        time.sleep(2)

        # 2. 数据看板
        print("截图2: 数据看板...")
        page.goto(f"{BASE}/dashboard")
        time.sleep(2)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "02_dashboard.png"))

        # 3. 品类筛选交互
        print("截图3: 品类筛选交互...")
        page.select_option("select[name='category']", "Fashion")
        time.sleep(2)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "03_interaction.png"))

        # 4. 助手页面
        print("截图4: 助手页面...")
        page.goto(f"{BASE}/assistant")
        time.sleep(2)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "04_assistant.png"))

        browser.close()
        print("全部截图完成！")

if __name__ == "__main__":
    main()
