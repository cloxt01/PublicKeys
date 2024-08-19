from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()
        page.goto('https://tokopedia.com')
        print(f"Judul halaman: {page.title()}")
        browser.close()

if __name__ == "__main__":
    main()
