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

        # STEP 1: Open login page
        page.goto("https://portal.manipal.edu/statistics/111")

        # STEP 2: Select Student
        page.select_option("select", label="Student")
        page.click("text=CONTINUE")

        # STEP 3: Login
        page.fill("input[type='text']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.click("text=LOGIN")

        page.wait_for_load_state("networkidle")
        print("✅ Logged in")

        # STEP 4: Click MORE
        page.click("text=MORE")
        page.wait_for_selector("table")  # wait until consultation table appears
        print("📊 Reached consultation table")

        # 🔁 Continuous checking loop
        while True:
            try:
                print("🔍 Checking slots...")

                checkboxes = page.locator("table input[type='checkbox']")
                count = checkboxes.count()

                for i in range(count):
                    cb = checkboxes.nth(i)

                    if cb.is_enabled():
                        print("🔥 SLOT FOUND! BOOKING NOW")
                        cb.click()

                        # Try clicking submit button
                        try:
                            page.get_by_role("button", name="Submit").click()
                        except:
                            page.click("text=Submit")

                        print("✅ BOOKED SUCCESSFULLY")
                        browser.close()
                        return

                time.sleep(1)

            except Exception as e:
                print("⚠️ Error:", e)
                time.sleep(2)

run()
