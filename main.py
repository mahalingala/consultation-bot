import subprocess
import os
import time
from playwright.sync_api import sync_playwright

# 🔥 Install browser ONCE
subprocess.run(["playwright", "install", "chromium"])

# 🔐 Get credentials from Railway
USERNAME = os.getenv("251280070037")
PASSWORD = os.getenv("28/08/2003")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()

        # STEP 1: Open login page
        page.goto("https://portal.manipal.edu/statistics/I11")

        # STEP 2: Select Student
        page.select_option("select", label="Student")
        page.click("text=CONTINUE")

        page.wait_for_timeout(2000)

        # STEP 3: Login
        page.fill("input[type='text']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.click("text=LOGIN")

        page.wait_for_load_state("networkidle")

        print("✅ Logged in")

        # STEP 4: Click MORE
        page.click("text=MORE")
        page.wait_for_timeout(3000)

        print("📊 Reached consultation table")

        # ⚡ FAST LOOP
        while True:
            try:
                checkboxes = page.locator("input[type='checkbox']")
                count = checkboxes.count()

                for i in range(count):
                    cb = checkboxes.nth(i)

                    if cb.is_enabled():
                        print("🔥 SLOT FOUND! BOOKING NOW")

                        cb.click()

                        try:
                            page.click("text=Submit")
                        except:
                            pass

                        print("✅ BOOKED SUCCESSFULLY")

                        browser.close()
                        return

                time.sleep(0.5)

            except Exception as e:
                print("⚠️ Error:", e)
                time.sleep(1)

run()