import asyncio
import json
import random
from playwright.async_api import async_playwright

async def get_price(page):
    try:
        # Menunggu elemen harga muncul dengan lebih efisien
        price_element = await page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p', timeout=5000)
        if price_element:
            price_text = await price_element.inner_text()
            # Cek apakah harga tidak kosong dan bukan "Rp0"
            if price_text and price_text != "Rp0":
                return price_text
    except Exception as e:
        print(f"Error saat mengambil harga: {e}")
    return None  # Mengembalikan None jika terjadi kesalahan atau tidak ditemukan

async def fetch_price_and_reload(page):
    num_iterations = 10
    total_time = 0
    for _ in range(num_iterations):
        # Navigasi ke halaman Tokopedia beli langsung
        await page.goto('https://tokopedia.com/beli-langsung', wait_until="domcontentloaded")
        # Dapatkan harga
        start_time = asyncio.get_event_loop().time()
        price = await get_price(page)
        end_time = asyncio.get_event_loop().time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        if price:
            print(f"Harga ditemukan: {price} | {elapsed_time:.2f} detik")
        
        # Refresh halaman dengan cepat
        await page.reload()
        
        # Jeda acak untuk mencegah deteksi bot
        sleep_time = random.uniform(900, 1000)  # Jeda acak antara 5 dan 10 detik
        await asyncio.sleep(sleep_time)

    average_time = total_time / num_iterations
    print(f"Waktu rata-rata: {average_time:.2f} detik")

    # Simpan cookies ke file setelah menampilkan waktu rata-rata
    cookies = await page.context.cookies()
    with open('cookie.json', 'w') as f:
        json.dump(cookies, f, indent=4)
    print("Cookies telah disimpan ke dalam file 'cookie.json'.")

async def main():
    async with async_playwright() as p:
        firefox_path = "C:\\Users\\MyBook Hype\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gjq2e4ww.1"
        browser = await p.firefox.launch_persistent_context(
            firefox_path,
            headless=False,
            args=['--disable-extensions', '--disable-gpu', '--no-sandbox', '--disable-cache'],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        page = browser.pages[0]
        print("Memuat halaman...")
        try:
            # Jalankan tugas paralel
            tasks = [
                asyncio.create_task(fetch_price_and_reload(page))
            ]
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Error di main loop: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
