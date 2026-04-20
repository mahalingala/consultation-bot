import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Opening login page...")
        page.goto("https://portal.manipal.edu/statistics/l11", timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(3000)  # extra wait for JS to render

        # take screenshot to see what the page looks like
        page.screenshot(path="page1.png")
        print(f"📸 Page loaded. URL: {page.url}")
        print(f"📄 Page title: {page.title()}")

        # wait specifically for the select element
        page.wait_for_selector("select", timeout=30000)
        page.select_option("select", label="Student")
        page.wait_for_timeout(500)

        page.click("text=CONTINUE")
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        page.screenshot(path="page2.png")
        print("🔑 Logging in...")

        page.fill("input[type='text']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.click("text=LOGIN")
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        if "l8" not in page.url:
            page.screenshot(path="login_failed.png")
            print(f"❌ Login failed! URL: {page.url}")
            browser.close()
            return

        print("✅ Logged in!")

        page.goto("https://portal.manipal.edu/statistics/l7")
        page.wait_for_load_state("networkidle")

        print("🔥 Scanning for open slots...")

        while True:
            try:
                page.reload()
                page.wait_for_load_state("networkidle")

                checkboxes = page.locator("input[type='checkbox']")
                count = checkboxes.count()

                for i in range(count):
                    cb = checkboxes.nth(i)
                    if cb.is_enabled() and not cb.is_checked():
                        print(f"🔥 OPEN SLOT FOUND! Clicking slot #{i}...")
                        cb.click()
                        page.wait_for_timeout(500)
                        page.screenshot(path="booked.png")
                        print("✅ DONE!")
                        browser.close()
                        return

                print("⏳ No open slots, retrying...")

            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(0.5)

run()