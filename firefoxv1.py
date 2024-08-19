import time
from playwright.sync_api import sync_playwright

def get_price(page):
    while True:  # Loop terus menerus sampai harga ditemukan
        try:
            # Mencari elemen harga dengan waktu tunggu tertentu
            price_element = page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p', timeout=2000)
            if price_element:
                price_text = price_element.inner_text()
                # Cek apakah harga tidak kosong dan bukan "Rp0"
                if price_text and price_text != "Rp0":
                    return price_text
        except Exception as e:
            pass  # Abaikan exception dan terus mencari harga

def main():
    with sync_playwright() as p:
        firefox_path = "C:\\Users\\MyBook Hype\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gjq2e4ww.1"
        browser = p.firefox.launch_persistent_context(
            firefox_path,
            headless=False # Nonaktifkan ekstensi, GPU, dan sandbox
        )
        
        page = browser.new_page()
        print("Memuat halaman...")
        while True:
            # Navigasi ke halaman Tokopedia beli langsung
            page.goto('https://tokopedia.com/beli-langsung', wait_until="domcontentloaded")  # Tunggu hingga DOM selesai dimuat
            page.wait_for_load_state("domcontentloaded")  # Pastikan halaman benar-benar dimuat

            # Dapatkan harga
            start_time = time.time()
            price = get_price(page)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if price:
                print(f"Harga ditemukan: {price} | {elapsed_time:.2f} detik")
            time.sleep(3600)
            # Refresh halaman dengan cepat
            page.reload()

        # Tutup browser
        browser.close()

if __name__ == "__main__":
    main()
