from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright

def parse_cookies(file):
    with open('cookie.txt', 'r') as file:
            cookie_string = file.read().strip()

        # Pisahkan cookies menjadi list
    cookies_list = []
    for cookie in cookie_string.split('; '):
        name, value = cookie.split('=', 1)
        cookies_list.append({
                'name': name,
                'value': value,
                'domain': '.shopee.co.id',
                'path': '/'  # Tambahkan path ke setiap cookie
            })
    return cookies_list
def main():
    with sync_playwright() as p:
        # Meluncurkan browser Firefox
        browser = p.chromium.launch(headless=False, args=["--disable-web-security"])
        
        # Membuat konteks barus
        browser_context = browser.new_context(
            viewport={"width": 434, "height": 842},
            #user_agent="Mozilla/5.0 (Android 12; Mobile; rv:129.0) Gecko/129.0 Firefox/129.0"
            #user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.111 Safari/537.36"
        )
        # Membuat halaman baru
        page = browser_context.new_page()
        cookies = parse_cookies('cookie.txt')
        # Menambahkan cookies
        page.context.add_cookies(cookies)

        url = 'https://shopee.co.id'
        print(f"Navigasi ke {url}")
        page.goto(url, timeout=60000)  # Mengatur timeout menjadi 60 detik
        page.wait_for_load_state("networkidle")
        print("Selesaikan CAPTCHA secara manual, lalu tekan Enter untuk melanjutkan.")
        input()  # Tunggu sampai CAPTCHA diselesaikan secara manual

        print(page.title())
        browser_context.close()

if __name__ == "__main__":
    main()