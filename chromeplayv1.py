from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # Meluncurkan browser dengan profil pengguna
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir='C:/Users/MyBook Hype/AppData/Local/Google/Chrome/User Data',
            headless=False
        )
        
        # Membuka halaman baru
        page = browser_context.new_page()
        
        # URL yang ingin ditangkap
        target_url = 'https://gql.tokopedia.com/graphql/update_cart_occ_multi'
        
        # Menangkap permintaan jaringan
        def on_request(request):
            if request.url == target_url:
                print(f"URL: {request.url}")
                try:
                    # Mengakses post_data sebagai properti
                    post_data = request.post_data
                    if post_data:
                        print(f"Request Body: {post_data}")
                    else:
                        print("Request Body: No data")
                except Exception as e:
                    print(f"Error accessing request body: {e}")
        # Menangkap respons jaringan
        def on_response(response):
            if response.url == target_url:
                try:
                    # Respons body adalah binary, jadi decode
                    response_body = response.body().decode('utf-8')
                    print(f"Response Body: {response_body}")
                except Exception as e:
                    print(f"Error accessing response body: {e}")

        # Mendaftarkan event listener
        page.on('request', on_request)
        page.on('response', on_response)
        
        # Membuka URL yang diinginkan
        page.goto('https://www.tokopedia.com/beli-langsung')
        
        # Menunggu beberapa waktu agar semua permintaan selesai
        page.wait_for_timeout(10000)  # 10 detik

        # Menutup browser
        browser_context.close()

if __name__ == "__main__":
    main()
