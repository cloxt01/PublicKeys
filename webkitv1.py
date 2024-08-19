import time
from playwright.sync_api import sync_playwright

def get_price(page):
    while True:
        try:
            # Mencari elemen harga dengan waktu tunggu yang sangat singkat
            price_element = page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p', timeout=1000)
            if price_element:
                price_text = price_element.inner_text()
                # Cek apakah harga tidak kosong dan bukan "Rp0"
                if price_text and price_text != "Rp0":
                    return price_text
        except Exception:
            pass  # Abaikan exception dan terus mencari harga

def main():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False, args=['--disable-extensions', '--disable-gpu', '--no-sandbox', '--disable-cache'])
        context = browser.new_context()
        page = context.new_page()
        print("Memuat halaman...")
        while True:
            # Navigasi ke halaman Tokopedia beli langsung
            page.goto('https://tokopedia.com/beli-langsung', wait_until="domcontentloaded")
            
            # Dapatkan harga
            print(page.title())
            start_time = time.time()
            price = get_price(page)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if price:
                print(f"Harga ditemukan: {price} | {elapsed_time:.2f} detik")
            
            # Refresh halaman dengan cepat
            page.reload()

if __name__ == "__main__":
    main()
