from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Menentukan path ke direktori profil Chrome
        user_data_dir = "C:\\Users\\MyBook Hype\\AppData\\Local\\Google\\Chrome\\User Data"

        # Meluncurkan browser Chrome dengan profil yang sudah ada
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            #viewport={"width": 434, "height": 842},
            args=["--disable-web-security"],
            #user_agent="Mozilla/5.0 (Linux; Android 12; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        )

        # Membuat halaman baru
        page = browser.new_page()

        url = 'https://shopee.co.id'
        print(f"Navigasi ke {url}")
        page.goto(url, timeout=60000)  # Mengatur timeout menjadi 60 detik

        page.wait_for_load_state("networkidle")
        print("Selesaikan CAPTCHA secara manual, lalu tekan Enter untuk melanjutkan.")
        input()  # Tunggu sampai CAPTCHA diselesaikan secara manual

        print(page.title())
        browser.close()

if __name__ == "__main__":
    main()
