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
        page.goto("https://portal.manipal.edu/statistics/I11", timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        page.wait_for_selector("select", timeout=30000)
        page.select_option("select", label="Student")
        page.wait_for_timeout(500)

        page.click("text=CONTINUE")
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        print("🔑 Logging in...")
        page.locator("input[type='text']").fill(USERNAME)      # ✅ FIXED
        page.locator("input[type='password']").fill(PASSWORD)  # ✅ FIXED
        page.click("text=LOGIN")
        page.wait_for_load_state("networkidle", timeout=60000)
        page.wait_for_timeout(2000)

        if "I8" not in page.url:
            print(f"❌ Login failed! URL: {page.url}")
            browser.close()
            return

        print("✅ Logged in!")

        page.goto("https://portal.manipal.edu/statistics/I7")
        page.wait_for_load_state("networkidle")

        print("🔥 Scanning for open slots continuously...")
        booked_count = 0

        while True:
            try:
                page.reload()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)

                rows = page.locator("table tr")
                row_count = rows.count()

                for i in range(row_count):
                    row = rows.nth(i)
                    cb = row.locator("input[type='checkbox']")
                    if cb.count() == 0:
                        continue

                    checkbox = cb.first

                    if checkbox.is_enabled() and not checkbox.is_checked():
                        print(f"🔥 OPEN SLOT FOUND at row #{i}! Clicking...")
                        checkbox.scroll_into_view_if_needed()
                        checkbox.dispatch_event("click")
                        page.wait_for_timeout(2000)

                        try:
                            page.wait_for_load_state("networkidle", timeout=10000)
                        except:
                            pass

                        page.wait_for_timeout(2000)

                        if checkbox.is_checked():
                            booked_count += 1
                            print(f"✅ BOOKED! Total booked so far: {booked_count}")
                        else:
                            checkbox.click(force=True)
                            page.wait_for_timeout(3000)
                            booked_count += 1
                            print(f"✅ BOOKED (force click)! Total booked so far: {booked_count}")

                        break

                print(f"⏳ No open slots, retrying... (booked so far: {booked_count})")
                time.sleep(2)

            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(0.5)

run()

run()