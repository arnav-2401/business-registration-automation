from playwright.sync_api import sync_playwright
import time
from config import Config

class FormAutomator:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = None

    def detect_captcha(self):
        return self.page.query_selector("#captcha") is not None

    def fill_field(self, field, value):
        selectors = [
            f'[name="{field}"]',
            f'[id="{field}"]',
            f'[aria-label*="{field}"]',
            f'text={field} >> .. >> input'
        ]
        
        for selector in selectors:
            if self.page.locator(selector).count() > 0:
                self.page.fill(selector, str(value))
                return True
        return False

    def submit_form(self, url, data_map, max_retries=3):
        self.page = self.browser.new_page()
        try:
            self.page.goto(url)
            
            for retry in range(max_retries):
                if self.detect_captcha():
                    raise Exception("CAPTCHA detected - human intervention required")
                
                for field, value in data_map.items():
                    if not self.fill_field(field, value):
                        raise Exception(f"Field {field} not found")
                
                
                if self.page.query_selector(".error-message"):
                    errors = self.page.inner_text(".error-message")
                    raise Exception(f"Validation errors: {errors}")
                
                self.page.click("button[type='submit']")
                if "confirmation" in self.page.url:
                    return self.page.inner_text(".confirmation-number")
                
            raise Exception("Max submission retries exceeded")
            
        finally:
            self.page.screenshot(path=f"submission_{time.time()}.png")
            self.browser.close()