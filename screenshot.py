from playwright.sync_api import sync_playwright
import time

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})
        
        # Go to app
        page.goto("http://127.0.0.1:3000")
        
        # Select python
        page.select_option("#lang-select", "python")
        
        # Type code
        demo_code = """class DataProcessor:
    def __init__(self, token):
        self.auth_token = token
        
    def fetch_user_info(self, uid):
        return {"id": uid, "status": 200}
"""
        page.fill("#src-input", demo_code)
        
        # Click mask
        page.click("#action-btn")
        
        # Wait for response
        time.sleep(1)
        
        # Take screenshot
        page.screenshot(path="screenshot.png")
        browser.close()
        
if __name__ == "__main__":
    take_screenshot()
    print("Screenshot saved to screenshot.png")
