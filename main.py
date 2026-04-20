import os
import time
from playwright.sync_api import sync_playwright

USERNAME = os.getenv("USERNAME_VAL")
PASSWORD = os.getenv("PASSWORD")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        print("🌐 Opening login page...")
        page.goto("https://portal.manipal.edu/statistics/l11")
        page.wait_for_load_state("networkidle")

        page.select_option("select", label="Student")
        page.wait_for_timeout(500)

        page.click("text=CONTINUE")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)

        print("🔑 Logging in...")
        page.fill("input[type='text']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.click("text=LOGIN")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        if "l8" not in page.url:
            print(f"❌ Login failed! URL: {page.url}")
            browser.close()
            return

        print("✅ Logged in!")

        # Go to consultation list
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
                        cb.click()  # just click, no submit
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