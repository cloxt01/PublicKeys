from playwright.sync_api import sync_playwright
import time

def measure_performance(browser_type, headless=True, block_resources=None):
    # Meluncurkan browser dengan opsi headless dan blocking resources
    browser = browser_type.launch(headless=headless)
    page = browser.new_page()

    # Memblokir sumber daya yang tidak penting
    if block_resources:
        page.route("**/*", lambda route, request: route.abort()
                   if request.resource_type in block_resources
                   else route.continue_())

    # Mencatat waktu sebelum memulai navigasi
    start_time = time.time()
    
    # Memuat halaman
    page.goto('https://www.tokopedia.com')
    
    # Mencatat waktu setelah halaman selesai dimuat
    end_time = time.time()
    
    # Menghitung durasi waktu yang dibutuhkan
    duration = end_time - start_time
    print(f"Time taken to load page: {duration:.2f} seconds")

    # Tutup browser
    browser.close()

block_resources = ["image", "media", "font"]
with sync_playwright() as p:
    for browser_type in [p.firefox, p.webkit]:
        print(f"Testing with {browser_type.name}")
        measure_performance(browser_type, headless=True, block_resources=block_resources)
