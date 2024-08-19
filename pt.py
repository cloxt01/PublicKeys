from playwright.sync_api import sync_playwright

def run(playwright):
    # Launch the browser in headful mode
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        viewport={'width': 1280, 'height': 800},
        extra_http_headers={
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'ect': '4g',
            'referer': 'https://www.tokopedia.com/',
        }
    )

    # Clear cookies before opening the page
    context.clear_cookies()

    page = context.new_page()

    # Clear local storage and session storage
    page.evaluate('''() => {
        localStorage.clear();
        sessionStorage.clear();
    }''')

    # Disable cache for this page
    page.route('**/*', lambda route: route.continue_(options={'disable_cache': True}))

    # Event handler to print request headers
    def handle_request(request):
        if 'beli-langsung' in request.url:
            print(f"Request URL: {request.url}")
            print("Request headers:")
            for key, value in request.headers.items():
                print(f"{key}: {value}")
            print("\n")
    
    # Event handler to print response headers
    def handle_response(response):
        if 'beli-langsung' in response.url:
            print(f"Response URL: {response.url}")
            print("Response headers:")
            for key, value in response.headers.items():
                print(f"{key}: {value}")
            print("\n")
            print(f"Response status: {response.status}")
            print(f"Response body: {response.text()[:500]}...\n")  # print first 500 characters of response body
    
    # Attach the event handlers
    page.on('request', handle_request)
    page.on('response', handle_response)
    
    # Navigate to the website
    page.goto('https://www.tokopedia.com/beli-langsung')
    
    print("Browser is open. Press Enter to close it.")
    
    # Wait for user input to close the browser
    input()
    
    # Close the browser
    context.close()

with sync_playwright() as playwright:
    run(playwright)
