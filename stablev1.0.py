import time
from playwright.sync_api import sync_playwright, TimeoutError

def get_price(page):
    while True:
        try:
            price_element = page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p', timeout=2000)
            if price_element:
                price_text = price_element.inner_text()
                if price_text and price_text != "Rp0":
                    return price_text
        except TimeoutError:
            pass
        except Exception as e:
            print(f"Error: {e}")

def main():
    with sync_playwright() as p:
        firefox_path = "C:\\Users\\MyBook Hype\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ljbho8pc.Default User-1722598259338"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

        browser = p.firefox.launch_persistent_context(
            firefox_path,
            headless=False,
            viewport={"width": 1280, "height": 800},
            user_agent=user_agent,
            java_script_enabled=True,
            bypass_csp=True,
            locale="id-ID",
            timezone_id="Asia/Jakarta",
            extra_http_headers={
                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "upgrade-insecure-requests": "1",
                "dnt": "1",
                "ect": "4g",
                "referer": "https://www.tokopedia.com/login?ld=%2Fbeli-langsung"
            }
        )

        page = browser.pages[0]
        print("Memuat halaman...")
        
        while True:
            page.goto('https://tokopedia.com/beli-langsung', wait_until="domcontentloaded")
            page.wait_for_load_state("domcontentloaded")
            
            # Coba menghapus/mengganti cache
            page.evaluate('window.__cache = undefined; window.__memoCache = undefined;')

            # Atau, kosongkan cache
            # page.evaluate('window.__cache = {}; window.__memoCache = {};')

            # Cek konten halaman
            page_source = page.content()
            print("Page Source:\n", page_source)

            start_time = time.time()
            price = get_price(page)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if price:
                print(f"Harga ditemukan: {price} | {elapsed_time:.2f} detik")
            time.sleep(1000)
            page.reload()

        browser.close()

if __name__ == "__main__":
    main()
