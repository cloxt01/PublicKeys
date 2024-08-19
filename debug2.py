import asyncio
import time
from playwright.async_api import async_playwright

async def get_price(page):
    try:
        price_element = await page.query_selector('div[data-testid="lblOSPSummaryTotalHarga"] p')
        if price_element:
            price_text = await price_element.inner_text()
            return price_text
        return 'Elemen harga tidak ditemukan.'
    except Exception as e:
        return f"Error mengambil data: {str(e)}"

async def click_button(page):
    try:
        # Tunggu hingga tombol muncul di halaman
        await page.wait_for_selector('button[data-testid="occBtnPayment"]', state='attached', timeout=20000)
        
        # Dapatkan referensi ke tombol
        button = await page.query_selector('button[data-testid="occBtnPayment"]')
        
        if button:
            # Scroll ke elemen jika perlu
            await button.scroll_into_view_if_needed()

            # Tunggu sampai elemen benar-benar siap untuk diinteraksi
            await page.wait_for_function('document.querySelector("button[data-testid=\'occBtnPayment\']").offsetParent !== null')

            # Klik tombol dengan opsi force
            await button.click(force=True, timeout=10000)
            print("Tombol Bayar diklik.")
            
            # Tunggu beberapa detik untuk memastikan halaman benar-benar berubah
            await page.wait_for_timeout(10000)  # Menunggu 5 detik
            
            # Ambil URL terbaru
            new_url = page.url
            print(f"URL setelah klik tombol bayar: {new_url}")
        else:
            print("Tombol Bayar tidak ditemukan.")
    except Exception as e:
        print(f"Error saat mengklik tombol: {str(e)}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir='C:/Users/MyBook Hype/AppData/Local/Google/Chrome/User Data',
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=site-per-process',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-web-security',
                '--disable-cache',
                '--disable-cookies'
            ]
        )
        
        def block_resources(route):
            if route.request.resource_type in ['image', 'stylesheet', 'font','script']:
                return route.abort()
            return route.continue_()
        
        page = await browser.new_page()
        await page.route("**/*", block_resources)

        await page.set_viewport_size({"width": 400, "height": 300})  # Ukuran viewport lebih besar
        await page.goto("https://tokopedia.com/beli-langsung", wait_until='domcontentloaded')

        try:
            await page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p')
        except Exception as e:
            print(f"Error: {str(e)}")
            await browser.close()
            return

        initial_price = await get_price(page)
        print(f"Harga Awal: {initial_price}")
        try:
            while True:
                start_time = time.time()
                await page.reload(wait_until='domcontentloaded')
                try:
                    await page.wait_for_selector('div[data-testid="lblOSPSummaryTotalHarga"] p')
                except Exception as e:
                    print(f"Error: {str(e)}")
                    continue
                
                end_time = time.time()
                elapsed_time = end_time - start_time

                current_price = await get_price(page)
                print(f"Harga Terbaru: {current_price} | Waktu: {elapsed_time:.2f} detik")

                if current_price != initial_price:
                    print("Harga telah berubah!")
                    
                    await click_button(page)  # Klik tombol Bayar
                    initial_price = current_price
                    break

        except KeyboardInterrupt:
            print("Skrip dihentikan oleh pengguna.")
        
        finally:
            await browser.close()

asyncio.run(main())
