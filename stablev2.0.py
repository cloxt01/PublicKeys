import asyncio
import json
import aiohttp
from urllib.parse import urlparse

async def gql(url, payload):
    timeout = aiohttp.ClientTimeout(total=10)  # Timeout setelah 10 detik
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(url, json=payload) as response:
                print(f"Status Code: {response.status}")  # Debugging
                response.raise_for_status()
                response_json = await response.json()
                print(f"Response from {url}: {response_json}")  # Debugging
                return response_json
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error in gql request: {e.status} - {e.message}")
            return None
        except Exception as e:
            print(f"Error in gql request: {e}")
            return None


def extract_domain_and_product_key(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    domainname = path_parts[1] if len(path_parts) > 1 else None
    productkey = path_parts[2] if len(path_parts) > 2 else None
    return domainname, productkey

async def get_product_info(productKey, domainName):
    print("Fetching product info...")  # Debugging
    url_getProductInfo = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"
    payload_getProductInfo = [
    {
        "operationName": "PDPGetLayoutQuery",
        "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {\n  title\n  description\n  contentMedia {\n    url\n    ratio\n    type\n    __typename\n  }\n  show\n  ctaText\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductDataInfo\n        ...ProductSocial\n        ...ProductDetailMediaComponent\n        ...ProductCategoryCarousel\n        ...ProductCustomInfo\n        ...ProductVariant\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "apiVersion": 1,
            "deviceID": "",
            "extParam": "",
            "layoutID": "",
            "productKey": productKey,
            "shopDomain": domainName,
            "tokonow": {
                "serviceType": "ooc",
                "shopID": "11530573",
                "whID": "0"
            },
            "userLocation": {
                "addressID": "227511839",
                "cityID": "141",
                "districtID": "1530",
                "latlon": "-6.329750022505787,106.39545891433954",
                "postalCode": "42381"
            }
        }
    }
]

    print(f"Sending request to {url_getProductInfo} with payload: {payload_getProductInfo}")  # Debugging
    
    product = await gql(url_getProductInfo, payload_getProductInfo)
    if product is None:
        return None, None, None
    
    print(f"Raw response: {product}")  # Debugging
    
    if isinstance(product, dict) and 'data' in product:
        data = product.get('data', {})
        print(f"Product data received: {data}")  # Debugging
        if 'pdpGetLayout' in data:
            pdp_session = json.loads(data['pdpGetLayout'].get('pdpSession', '{}'))
            shop_id = data['pdpGetLayout']['basicInfo'].get('shopID', 'ID produk tidak tersedia')
            product_id = data['pdpGetLayout']['basicInfo'].get('id', 'ID produk tidak tersedia')
            warehouse_id = pdp_session.get('patcs', {}).get('whid', 'Warehouse ID tidak tersedia')
            return shop_id, product_id, warehouse_id
    return None, None, None

async def add_to_cart(product_id, shop_id, warehouse_id):
    print("Adding to cart...")  # Debugging
    url_addToCartOCC = "https://gql.tokopedia.com/graphql/AddToCartOCCMulti"
    payload_addToCartOCC = {
        "operationName": "AddToCartOCCMulti",
        "query": """mutation AddToCartOCCMulti($param: OneClickCheckoutMultiATCParam) {
          add_to_cart_occ_multi(param: $param) {
            error_message
            status
            data {
              carts {
                cart_id
                __typename
              }
              __typename
            }
            __typename
          }
        }""",
        "variables": {
            "param": {
                "carts": [
                    {
                        "notes": "",
                        "product_id": product_id,
                        "quantity": 1,
                        "shop_id": shop_id,
                        "warehouse_id": warehouse_id
                    }
                ],
                "chosen_address": {
                    "address_id": 227511839,
                    "district_id": 1530,
                    "geolocation": "-6.329750022505787,106.39545891433954",
                    "mode": 1,
                    "postal_code": "42381"
                },
                "lang": "id",
                "source": "pdp"
            }
        }
    }
    cart_response = await gql(url_addToCartOCC, payload_addToCartOCC)
    if cart_response is None:
        return None
    return cart_response['data']['add_to_cart_occ_multi']['data']['carts'][0]['cart_id']

async def update_cart_element(cart_id):
    print(f"Updating cart {cart_id}")  # Debugging
    return f"Cart {cart_id} updated"

async def check_current_price(price_now):
    print(f"Checking current price: {price_now}")  # Debugging
    return price_now

async def main(price_now):
    url_product = "https://www.tokopedia.com/notebookgamingid/axioo-hype-7-amd-ryzen-7-5700u-16gb-512gb-ssd-radeon-14-fhd-ips-w11pro-r5-8-256-dos-non-antigores-d2385"
    #url_product = input("Masukan url product : ") 
    domainName, productKey = extract_domain_and_product_key(url_product)
    
    if not domainName or not productKey:
        print("Gagal mengekstrak domainName dan productKey dari URL produk")
        return
    
    print("ProductInfo")
    print("------------------")
    print("Domainname:", domainName)
    print("Productkey:", productKey)
    
    shop_id, product_id, warehouse_id = await get_product_info(productKey, domainName)
    if not all([shop_id, product_id, warehouse_id]):
        print("Gagal mendapatkan informasi produk")
        return
    
    print(f"Shop ID: {shop_id}, Product ID: {product_id}, Warehouse ID: {warehouse_id}")  # Debugging
    
    cart_id = await add_to_cart(product_id, shop_id, warehouse_id)
    if cart_id is None:
        print("Gagal menambahkan produk ke keranjang")
        return
    
    current_price, update_result = await asyncio.gather(
        check_current_price(price_now),
        update_cart_element(cart_id)
    )
    
    print(f"Current price : {current_price}")
    print(f"Results : {update_result}")

# Asumsi price_now sudah didefinisikan sebelumnya
price_now = 100  # Contoh nilai price_now

asyncio.run(main(price_now))
