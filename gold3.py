import json
import requests
import sys
import time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

# URL produk yang digunakan
url_product = "https://www.tokopedia.com/wingsofficial/soklin-pelembut-pakaian-sekali-bilas-twilight-violet-650-mll"

def load_cookies(file_path):
    try:
        with open(file_path, 'r') as file:
            cookies_list = json.load(file)
        
        cookie_string = []
        for cookie in cookies_list:
            name = cookie.get('name')
            value = cookie.get('value')
            if name and value:
                cookie_string.append(f"{name}={value}")
        
        return "; ".join(cookie_string)
    
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
        return ""
    except json.JSONDecodeError:
        print(f"Error dalam mengurai file '{file_path}'. Pastikan file dalam format JSON yang benar.")
        return ""
def extract_domain_and_product_key(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    domainname = path_parts[1] if len(path_parts) > 1 else None
    productkey = path_parts[2] if len(path_parts) > 2 else None
    return domainname, productkey

def gql(url, data, cookies, x_tkpd_akamai, url_product=url_product):
    headers = {
        'Content-Length': str(len(json.dumps(data))),
        'x-version': '28031fb',
        'x-tkpd-akamai': x_tkpd_akamai,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'X-Source': 'tokopedia-lite',
        'X-Device': 'default_v3',
        'X-Tkpd-Lite-Service': 'zeus',
        'Sec-CH-UA-Platform': '"Windows"',
        'Origin': 'https://www.tokopedia.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': url_product,
        'Cookie': cookies,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    httpcode = response.status_code
    
    if httpcode == 200:
        return response.json()
    else:
        print(f"{httpcode} Error in gql")
        print(f"Response: {response.text}")
        return None

cookies = load_cookies('cookies.json')
if not cookies:
    print("Tidak dapat memuat cookies, proses dihentikan.")
    sys.exit()
domainName, productKey = extract_domain_and_product_key(url_product)
print("ProductInfo")
print("------------------")
print("Domainname:", domainName)
print("Productkey:", productKey)

x_tkpd_akamai = 'pdpGetLayout'
url_getProductInfo = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"
payload_getProductInfo = {
    "operationName": "PDPGetLayoutQuery",
    "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {\n  title\n  description\n  contentMedia {\n    url\n    ratio\n    type\n    __typename\n  }\n  show\n  ctaText\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductDataInfo\n        ...ProductSocial\n        ...ProductDetailMediaComponent\n        ...ProductCategoryCarousel\n        ...ProductCustomInfo\n        ...ProductVariant\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
        "shopDomain": domainName,
        "productKey": productKey,
        "layoutID": "main",
        "apiVersion": 2.1,
        "userLocation": {"countryCode": "ID", "regionCode": "11", "cityCode": "1101"},
        "extParam": "",
        "tokonow": {"transactionID": "1"},
        "deviceID": "default_v3"
    }
}
product_info = gql(url_getProductInfo, payload_getProductInfo,cookies,x_tkpd_akamai)

try:
    if product_info:
        if 'errors' in product_info:
            print("Error getting productInfo")
            print(product_info)
            sys.exit()
        else:
            data = product_info.get('data', {})
            pdp_session = data.get('pdpGetLayout', '{}').get('pdpSession', {})
            whid = json.loads(pdp_session).get('whid', None)
            shop_id = data.get('pdpGetLayout', {}).get('basicInfo', {}).get('shopID', None)
            product_id = data.get('pdpGetLayout', {}).get('basicInfo', {}).get('id', None)
            data = {
                "shop_id" : shop_id,
                "product_id" : product_id,
                "whid" : whid
            }
    else:
        print("Tidak ada data produk yang diambil.")
        sys.exit
except NameError as e:
    print(f"Terjadi kesalahan saat mencoba mengambil productInfo")
    print(f"Error : {e}")
except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat mencoba mengirim ke productInfo")
    print(f"Error : {e}")
except Exception as e:
    print("Terjadi kesalahan di productInfo")
    print(f"Error : {e}")
x_tkpd_akamai = 'atcoccmulti'
url_addToCart = "https://gql.tokopedia.com/graphql/AddToCartOCCMulti"
payload_addToCart = [
    {
        "operationName": "AddToCartOCCMulti",
        "query": "mutation AddToCartOCCMulti($param: OneClickCheckoutMultiATCParam) {\n  add_to_cart_occ_multi(param: $param) {\n    error_message\n    status\n    data {\n      message\n      success\n      toaster_action {\n        text\n        show_cta\n        __typename\n      }\n      out_of_service {\n        id\n        code\n        image\n        title\n        description\n        buttons {\n          id\n          code\n          message\n          color\n          __typename\n        }\n        __typename\n      }\n      carts {\n        cart_id\n        notes\n        product_id\n        quantity\n        shop_id\n        warehouse_id\n        __typename\n      }\n      next_page\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "param": {
                "carts": [
                    {
                        "notes": "",
                        "product_id": product_id,
                        "quantity": 1,
                        "shop_id": shop_id,
                        "warehouse_id": whid
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
]
addToCart = gql(url_addToCart,payload_addToCart,cookies,x_tkpd_akamai,'None')
if addToCart[0]['data']['add_to_cart_occ_multi']['data']['message'][0]:
    addToCart_msg = addToCart[0]['data']['add_to_cart_occ_multi']['data']['message'][0]
    print(f"{addToCart_msg}")
else:
    print(f"{addToCart}")
sys.exit()

url_get_occ_multi = "https://gql.tokopedia.com/graphql/get_occ_multi"
payload_get_occ_multi = [
    {
        "operationName": "get_occ_multi",
        "query": "query get_occ_multi($source: String, $chosen_address: ChosenAddressParam) {\n  get_occ_multi(source: $source, chosen_address: $chosen_address) {\n    error_message\n    status\n    data {\n      errors\n      error_code\n      pop_up_message\n      max_char_note\n      kero_token\n      kero_unix_time\n      kero_discom_token\n      error_ticker\n      tickers {\n        id\n        message\n        page\n        title\n        __typename\n      }\n      messages {\n        ErrorFieldBetween\n        ErrorFieldMaxChar\n        ErrorFieldRequired\n        ErrorProductAvailableStock\n        ErrorProductAvailableStockDetail\n        ErrorProductMaxQuantity\n        ErrorProductMinQuantity\n        __typename\n      }\n      occ_main_onboarding {\n        force_show_coachmark\n        show_onboarding_ticker\n        coachmark_type\n        onboarding_ticker {\n          title\n          message\n          image\n          show_coachmark_link_text\n          coachmark_link_text\n          __typename\n        }\n        onboarding_coachmark {\n          skip_button_text\n          detail {\n            step\n            title\n            message\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      group_shop_occ {\n        group_metadata\n        errors\n        errors_unblocking\n        cart_string\n        is_disable_change_courier\n        auto_courier_selection\n        shipment_information {\n          shop_location\n          free_shipping {\n            eligible\n            badge_url\n            __typename\n          }\n          free_shipping_extra {\n            eligible\n            badge_url\n            __typename\n          }\n          preorder {\n            is_preorder\n            duration\n            __typename\n          }\n          __typename\n        }\n        courier_selection_error {\n          title\n          description\n          __typename\n        }\n        bo_metadata {\n          bo_type\n          bo_eligibilities {\n            key\n            value\n            __typename\n          }\n          additional_attributes {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        shop {\n          shop_id\n          shop_name\n          shop_alert_message\n          shop_ticker\n          maximum_weight_wording\n          maximum_shipping_weight\n          is_gold\n          is_gold_badge\n          is_official\n          gold_merchant {\n            is_gold\n            is_gold_badge\n            gold_merchant_logo_url\n            __typename\n          }\n          official_store {\n            is_official\n            os_logo_url\n            __typename\n          }\n          shop_type_info {\n            shop_tier\n            shop_grade\n            badge\n            badge_svg\n            title\n            title_fmt\n            __typename\n          }\n          postal_code\n          latitude\n          longitude\n          district_id\n          shop_shipments {\n            ship_id\n            ship_name\n            ship_code\n            ship_logo\n            is_dropship_enabled\n            ship_prods {\n              ship_prod_id\n              ship_prod_name\n              ship_group_name\n              ship_group_id\n              minimum_weight\n              additional_fee\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        cart_details {\n          products {\n            cart_id\n            parent_id\n            product_id\n            product_name\n            product_price\n            product_url\n            category_id\n            category\n            errors\n            wholesale_price {\n              qty_min_fmt\n              qty_max_fmt\n              qty_min\n              qty_max\n              prd_prc\n              prd_prc_fmt\n              __typename\n            }\n            product_weight\n            product_weight_actual\n            product_weight_fmt\n            product_weight_unit_text\n            is_preorder\n            product_cashback\n            product_min_order\n            product_max_order\n            product_invenage_value\n            product_switch_invenage\n            product_image {\n              image_src_200_square\n              __typename\n            }\n            product_notes\n            product_quantity\n            campaign_id\n            product_original_price\n            product_price_original_fmt\n            initial_price\n            initial_price_fmt\n            slash_price_label\n            product_finsurance\n            warehouse_id\n            free_shipping {\n              eligible\n              __typename\n            }\n            free_shipping_extra {\n              eligible\n              __typename\n            }\n            product_preorder {\n              duration_day\n              __typename\n            }\n            product_tracker_data {\n              attribution\n              tracker_list_name\n              __typename\n            }\n            variant_description_detail {\n              variant_name\n              variant_description\n              __typename\n            }\n            product_warning_message\n            product_alert_message\n            product_information\n            purchase_protection_plan_data {\n              protection_available\n              protection_type_id\n              protection_price_per_product\n              protection_price\n              protection_title\n              protection_subtitle\n              protection_link_text\n              protection_link_url\n              protection_opt_in\n              protection_checkbox_disabled\n              tokopedia_protection_price\n              unit\n              protection_price_per_product_fmt\n              protection_price_fmt\n              source\n              protection_config\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        toko_cabang {\n          message\n          badge_url\n          __typename\n        }\n        warehouse {\n          warehouse_id\n          is_fulfillment\n          __typename\n        }\n        __typename\n      }\n      profile {\n        address {\n          address_id\n          receiver_name\n          address_name\n          address_street\n          district_id\n          district_name\n          city_id\n          city_name\n          province_id\n          province_name\n          phone\n          longitude\n          latitude\n          postal_code\n          state\n          state_detail\n          status\n          __typename\n        }\n        payment {\n          enable\n          active\n          gateway_code\n          gateway_name\n          image\n          description\n          minimum_amount\n          maximum_amount\n          wallet_amount\n          metadata\n          mdr\n          credit_card {\n            number_of_cards {\n              available\n              unavailable\n              total\n              __typename\n            }\n            available_terms {\n              term\n              mdr\n              mdr_subsidized\n              min_amount\n              is_selected\n              __typename\n            }\n            bank_code\n            card_type\n            is_expired\n            tnc_info\n            is_afpb\n            unix_timestamp\n            token_id\n            tenor_signature\n            __typename\n          }\n          error_message {\n            message\n            button {\n              text\n              link\n              __typename\n            }\n            __typename\n          }\n          occ_revamp_error_message {\n            message\n            button {\n              text\n              action\n              __typename\n            }\n            __typename\n          }\n          ticker_message\n          is_disable_pay_button\n          is_enable_next_button\n          is_ovo_only_campaign\n          ovo_additional_data {\n            ovo_activation {\n              is_required\n              button_title\n              error_message\n              error_ticker\n              __typename\n            }\n            ovo_top_up {\n              is_required\n              button_title\n              error_message\n              error_ticker\n              is_hide_digital\n              __typename\n            }\n            phone_number_registered {\n              is_required\n              button_title\n              error_message\n              error_ticker\n              __typename\n            }\n            __typename\n          }\n          bid\n          specific_gateway_campaign_only_type\n          wallet_additional_data {\n            wallet_type\n            enable_wallet_amount_validation\n            activation {\n              is_required\n              button_title\n              success_toaster\n              error_toaster\n              error_message\n              is_hide_digital\n              header_title\n              url_link\n              __typename\n            }\n            top_up {\n              is_required\n              button_title\n              success_toaster\n              error_toaster\n              error_message\n              is_hide_digital\n              header_title\n              url_link\n              __typename\n            }\n            phone_number_registered {\n              is_required\n              button_title\n              success_toaster\n              error_toaster\n              error_message\n              is_hide_digital\n              header_title\n              url_link\n              __typename\n            }\n            __typename\n          }\n          payment_fee_detail {\n            fee\n            show_slashed\n            show_tooltip\n            slashed_fee\n            title\n            tooltip_info\n            type\n            __typename\n          }\n          __typename\n        }\n        shipment {\n          service_id\n          service_duration\n          service_name\n          sp_id\n          recommendation_service_id\n          recommendation_sp_id\n          is_free_shipping_selected\n          __typename\n        }\n        __typename\n      }\n      promo {\n        last_apply {\n          code\n          data {\n            global_success\n            success\n            message {\n              state\n              color\n              text\n              __typename\n            }\n            codes\n            promo_code_id\n            title_description\n            discount_amount\n            cashback_wallet_amount\n            cashback_advocate_referral_amount\n            cashback_voucher_description\n            invoice_description\n            is_coupon\n            gateway_id\n            is_tokopedia_gerai\n            clashing_info_detail {\n              clash_message\n              clash_reason\n              is_clashed_promos\n              options {\n                voucher_orders {\n                  cart_id\n                  code\n                  shop_name\n                  potential_benefit\n                  promo_name\n                  unique_id\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            tokopoints_detail {\n              conversion_rate {\n                rate\n                points_coefficient\n                external_currency_coefficient\n                __typename\n              }\n              __typename\n            }\n            voucher_orders {\n              code\n              success\n              cart_id\n              unique_id\n              order_id\n              shop_id\n              is_po\n              duration\n              warehouse_id\n              address_id\n              type\n              cashback_wallet_amount\n              discount_amount\n              title_description\n              invoice_description\n              message {\n                state\n                color\n                text\n                __typename\n              }\n              benefit_details {\n                code\n                type\n                order_id\n                unique_id\n                discount_amount\n                discount_details {\n                  amount\n                  data_type\n                  __typename\n                }\n                cashback_amount\n                cashback_details {\n                  amount_idr\n                  amount_points\n                  benefit_type\n                  __typename\n                }\n                promo_type {\n                  is_exclusive_shipping\n                  is_bebas_ongkir\n                  __typename\n                }\n                benefit_product_details {\n                  product_id\n                  cashback_amount\n                  cashback_amount_idr\n                  discount_amount\n                  is_bebas_ongkir\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            benefit_summary_info {\n              final_benefit_text\n              final_benefit_amount\n              final_benefit_amount_str\n              summaries {\n                section_name\n                section_description\n                description\n                type\n                amount_str\n                amount\n                details {\n                  section_name\n                  description\n                  type\n                  amount_str\n                  amount\n                  points\n                  points_str\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            tracking_details {\n              product_id\n              promo_codes_tracking\n              promo_details_tracking\n              __typename\n            }\n            ticker_info {\n              unique_id\n              status_code\n              message\n              __typename\n            }\n            additional_info {\n              message_info {\n                message\n                detail\n                __typename\n              }\n              error_detail {\n                message\n                __typename\n              }\n              empty_cart_info {\n                image_url\n                message\n                detail\n                __typename\n              }\n              usage_summaries {\n                description\n                type\n                amount_str\n                amount\n                currency_details_str\n                __typename\n              }\n              sp_ids\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        error_default {\n          title\n          description\n          __typename\n        }\n        __typename\n      }\n      image_upload {\n        show_image_upload\n        text\n        left_icon_url\n        right_icon_url\n        checkout_id\n        front_end_validation\n        lite_url\n        __typename\n      }\n      customer_data {\n        id\n        name\n        email\n        msisdn\n        __typename\n      }\n      payment_additional_data {\n        merchant_code\n        profile_code\n        signature\n        change_cc_link\n        callback_url\n        __typename\n      }\n      prompt {\n        type\n        title\n        description\n        image_url\n        buttons {\n          text\n          link\n          action\n          color\n          __typename\n        }\n        __typename\n      }\n      total_product_price\n      placeholder_note\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "chosen_address": {
                "address_id": 227511839,
                "district_id": 1530,
                "geolocation": "-6.329750022505787,106.39545891433954",
                "mode": 1,
                "postal_code": "42381"
            },
            "source": "pdp"
        }
    }
]
get_occ_multi = gql(url_get_occ_multi,payload_get_occ_multi,cookies,x_tkpd_akamai,'None')

if get_occ_multi[0]['data']['get_occ_multi']['data']['total_product_price'] and not get_occ_multi[0]['data']['get_occ_multi']['data']['errors'] :
    current_price = get_occ_multi[0]['data']['get_occ_multi']['data']['total_product_price']
    cart_id = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['cart_id']
    data['cart_id'] = cart_id
    data['price'] = current_price
    print(f"Data price disimpan")
elif get_occ_multi[0]['data']['get_occ_multi']['data']['errors'][0]:
    print(f"Gagal menyimpan data price")
    errors_msg=get_occ_multi[0]['data']['get_occ_multi']['data']['errors'][0]
    print(errors_msg)
    sys.exit()
else:
    print("Terjadi kesalahan saat menyimpan data")
url_updateCart = "https://gql.tokopedia.com/graphql/update_cart_occ_multi"
payload_updateCart = [
    {
        "operationName": "update_cart_occ_multi",
        "query": "mutation update_cart_occ_multi($param: OneClickCheckoutMultiUpdateCartParam) {\n  update_cart_occ_multi(param: $param) {\n    error_message\n    status\n    data {\n      messages\n      success\n      prompt {\n        type\n        title\n        description\n        image_url\n        buttons {\n          text\n          link\n          action\n          color\n          __typename\n        }\n        __typename\n      }\n      toaster_action {\n        text\n        show_cta\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "param": {
                "cart": [
                    {
                        "cart_id": cart_id,
                        "notes": "",
                        "product_id": product_id,
                        "quantity": 1
                    }
                ],
                "chosen_address": {
                    "address_id": 227511839,
                    "district_id": 1530,
                    "geolocation": "-6.329750022505787,106.39545891433954",
                    "mode": 1,
                    "postal_code": "42381"
                },
                "profile": {
                    "address_id": 227511839,
                    "gateway_code": "BCAVA",
                    "is_free_shipping_selected": False,
                    "metadata": "{\"success\":true,\"message\":\"\",\"gateway_code\":\"BCAVA\",\"express_checkout_param\":{\"account_name\":\"\",\"account_number\":\"\",\"bank_id\":\"\",\"pan\":\"\",\"issuer\":\"\",\"card_token\":\"\",\"card_type\":\"\",\"total_saved_card\":\"\",\"installment_term\":\"0\",\"expiry\":\"\",\"bank_code\":\"\",\"pocket_id\":\"\",\"cc_number\":\"\"},\"express_checkout_url\":\"\",\"high_risk_flag\":\"\",\"description\":\"\",\"image\":\"https://images.tokopedia.net/img/toppay/sprites/bca.png\",\"signature\":\"\",\"customer_name\":\"\",\"customer_email\":\"\",\"user_id\":246116973}",
                    "service_id": 1004,
                    "shipping_id": 26,
                    "sp_id": 50
                },
                "skip_shipping_validation": True,
                "source": "update_qty_notes"
            }
        }
    }
]
update_cart = gql(url_updateCart,payload_updateCart,cookies,'None')
data['results'] = update_cart

def run(playwright, cart_id,product_id):
    try:
        # Memuat cookies dari file
        with open("cookies.json", "r") as file:
            cookies_browser = json.load(file)

        browser = playwright.chromium.launch(headless=True, args=['--disable-http2', '--ignore-certificate-errors'])
        context = browser.new_context()

        # Menambahkan cookies ke konteks
        context.add_cookies(cookies_browser)

        print("Navigating to url...")
        page = context.new_page()
        print("Current URL:", page.url)
        print("Page Title:", page.title())
        page.goto("https://tokopedia.com/beli-langsung", wait_until="networkidle")
        
        updated_price = current_price
        while current_price == updated_price:
            # Updating price
            print("Updating price...")
            get_occ_multi = gql(url_get_occ_multi, payload_get_occ_multi, cookies, 'None')
            if get_occ_multi[0]['data']['get_occ_multi']['data']:
                id = get_occ_multi[0]['data']['get_occ_multi']['data']['customer_data']['id']
                address_id = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['address']['address_id']
                district_id = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['address']['district_id']
                postal_code = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['address']['postal_code']
                latitude = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['address']['latitude']
                longitude = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['address']['longitude']
                is_free_shipping_selected = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['shipment']['is_free_shipping_selected']
                service_id = get_occ_multi[0]['data']['get_occ_multi']['data']['profile']['shipment']['service_id']
                shop_shipments = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['shop_shipments']
                shop_postal_code = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['shop_id']
                shop_postal_code = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['postal_code']
                shop_district_id = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['district_id']
                shop_longitude = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['longitude']
                shop_latitude = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['latitude']
                cat_id = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['category_id']
                warehouse_id = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['warehouse']['warehouse_id']
                updated_price = get_occ_multi[0]['data']['get_occ_multi']['data']['total_product_price']
                product_preorder = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['is_preorder']
                product_id = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['product_id']
                product_name = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['product_name']
                product_fulfillment = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['warehouse']['is_fulfillment']
                product_insurance = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['product_finsurance']
                product_weight = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['product_weight']
                product_weight_actual = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['cart_details'][0]['products'][0]['product_weight_actual']
                discom_token = get_occ_multi[0]['data']['get_occ_multi']['data']['kero_discom_token']
                token = get_occ_multi[0]['data']['get_occ_multi']['data']['kero_token']
                ut = get_occ_multi[0]['data']['get_occ_multi']['data']['kero_unix_time']
                shop_tier = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['shop']['shop_type_info']['shop_tier']
                group_metadata = get_occ_multi[0]['data']['get_occ_multi']['data']['group_shop_occ'][0]['group_metadata']
                ship_prod_ids = []
                for shipments in shop_shipments:
                    for prod in shipments["ship_prods"]:
                        ship_prod_ids.append(str(prod["ship_prod_id"]))

                # Gabungkan ship_prod_id menjadi string yang dipisahkan koma
                spids = ",".join(ship_prod_ids)
                print(f"Price : {updated_price}")
            elif get_occ_multi[0]['errors']:
                print("Gagal menyimpan data")
            else:
                print("Terjadi kesalahan, saat menyimpan data")
            
        print("Sending POST request to RatesV3Query...")
        url_getOngkir = "https://gql.tokopedia.com/graphql/RatesV3Query"
        payload_getOngkir = [
            {
                "operationName": "RatesV3Query",
                "query": "query RatesV3Query($input: OngkirRatesV3Input!, $metadata: Metadata) {\n  ratesV3(input: $input, metadata: $metadata) {\n    ratesv3 {\n      id\n      rates_id\n      type\n      services {\n        service_name\n        service_id\n        service_order\n        status\n        range_price {\n          min_price\n          max_price\n          __typename\n        }\n        etd {\n          min_etd\n          max_etd\n          __typename\n        }\n        texts {\n          text_range_price\n          text_etd\n          text_notes\n          text_service_notes\n          text_price\n          text_service_desc\n          text_eta_summarize\n          text_service_ticker\n          error_code\n          __typename\n        }\n        products {\n          shipper_name\n          shipper_id\n          shipper_product_id\n          shipper_product_name\n          shipper_product_desc\n          shipper_weight\n          promo_code\n          is_show_map\n          status\n          recommend\n          checksum\n          ut\n          ui_rates_hidden\n          price {\n            price\n            formatted_price\n            __typename\n          }\n          eta {\n            text_eta\n            error_code\n            __typename\n          }\n          etd {\n            min_etd\n            max_etd\n            __typename\n          }\n          texts {\n            text_range_price\n            text_etd\n            text_notes\n            text_service_notes\n            text_price\n            text_service_desc\n            __typename\n          }\n          insurance {\n            insurance_price\n            insurance_type\n            insurance_type_info\n            insurance_used_type\n            insurance_used_info\n            insurance_used_default\n            insurance_actual_price\n            insurance_pay_type\n            __typename\n          }\n          error {\n            error_id\n            error_message\n            __typename\n          }\n          cod {\n            is_cod_available\n            cod_text\n            cod_price\n            formatted_price\n            __typename\n          }\n          features {\n            ontime_delivery_guarantee {\n              available\n              value\n              text_label\n              text_detail\n              icon_url\n              url_detail\n              __typename\n            }\n            dynamic_price {\n              text_label\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        error {\n          error_id\n          error_message\n          __typename\n        }\n        is_promo\n        cod {\n          is_cod\n          cod_text\n          __typename\n        }\n        order_priority {\n          is_now\n          price\n          formatted_price\n          inactive_message\n          available_label\n          static_messages {\n            duration_message\n            checkbox_message\n            warningbox_message\n            fee_message\n            pdp_message\n            __typename\n          }\n          __typename\n        }\n        features {\n          dynamic_price {\n            text_label\n            __typename\n          }\n          __typename\n        }\n        ui_rates_hidden\n        selected_shipper_product_id\n        __typename\n      }\n      recommendations {\n        service_name\n        shipping_id\n        shipping_product_id\n        price {\n          price\n          formatted_price\n          __typename\n        }\n        etd {\n          min_etd\n          max_etd\n          __typename\n        }\n        texts {\n          text_range_price\n          text_etd\n          text_notes\n          text_service_notes\n          text_price\n          text_service_desc\n          __typename\n        }\n        insurance {\n          insurance_price\n          insurance_type\n          insurance_type_info\n          insurance_used_type\n          insurance_used_info\n          insurance_used_default\n          insurance_actual_price\n          insurance_pay_type\n          __typename\n        }\n        error {\n          error_id\n          error_message\n          __typename\n        }\n        __typename\n      }\n      info {\n        cod_info {\n          failed_message\n          __typename\n        }\n        blackbox_info {\n          text_info\n          __typename\n        }\n        __typename\n      }\n      promo_stacking {\n        is_promo\n        promo_code\n        title\n        shipper_id\n        shipper_product_id\n        shipper_name\n        shipper_desc\n        promo_detail\n        benefit_desc\n        point_change\n        user_point\n        promo_tnc_html\n        shipper_disable_text\n        service_id\n        __typename\n      }\n      error {\n        error_id\n        error_message\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables": {
                    "input": {
                        "actual_weight": str(product_weight_actual / 1000),
                        "address_id": str(address_id),
                        "cat_id": str(cat_id),
                        "destination": f"{str(district_id)}|{str(postal_code)}|{str(latitude)},{str(longitude)}",
                        "from": "client",
                        "group_metadata": group_metadata,
                        "insurance": str(product_insurance),
                        "is_blackbox": 0,
                        "is_fulfillment": product_fulfillment,
                        "lang": "id",
                        "occ": "1",
                        "order_value": str(updated_price),
                        "origin": f"{str(shop_district_id)}|{str(shop_postal_code)}|{str(shop_latitude)},{str(shop_longitude)}",
                        "pdp": "0",
                        "po_time": 0,
                        "preorder": product_preorder,
                        "product_insurance": str(product_insurance),
                        "products": "[{\"product_id\":"+str(product_id)+",\"is_free_shipping\":"+str(is_free_shipping_selected)+"}]",
                        "psl_code": "",
                        "shop_id": shop_id,
                        "shop_tier": shop_tier,
                        "spids": spids,
                        "token": f"Tokopedia+Kero:{str(token)}",
                        "type": "default_v3",
                        "user_history": -1,
                        "ut": str(ut),
                        "vehicle_leasing": 0,
                        "warehouse_id": str(warehouse_id),
                        "weight": str(product_weight_actual / 1000)
                    },
                    "metadata": {}
                }
            }
        ]
        get_Ongkir = gql(url_getOngkir,payload_getOngkir,cookies,'None')
        if get_Ongkir:
            rates_id = get_Ongkir[0]['data']['ratesV3']['ratesv3']['rates_id']
            price_ongkir = get_Ongkir[0]['data']['ratesV3']['ratesv3']['services'][1]['products'][0]['price']['price']
            insurance_price = get_Ongkir[0]['data']['ratesV3']['ratesv3']['services'][1]['products'][0]['insurance']['insurance_price']
            shipping_id = get_Ongkir[0]['data']['ratesV3']['ratesv3']['services'][1]['products'][0]['shipper_id']
            sp_id = get_Ongkir[0]['data']['ratesV3']['ratesv3']['services'][1]['products'][0]['shipper_product_id']

        else:
            print("Failed to get response from gql")

        paymentAmount = updated_price + price_ongkir + insurance_price
        #Updating Paymentfee
        url_get_payment_fee = "https://gql.tokopedia.com/graphql/getPaymentFee"
        payload_get_payment_fee = [
    {
        "operationName": "getPaymentFee",
        "query": "query getPaymentFee($profileCode: String!, $gatewayCode: String!, $paymentAmount: Float!) {\n  getPaymentFee(profileCode: $profileCode, gatewayCode: $gatewayCode, paymentAmount: $paymentAmount) {\n    success\n    errors {\n      code\n      message\n      __typename\n    }\n    data {\n      code\n      title\n      fee\n      tooltip_info\n      show_tooltip\n      show_slashed\n      slashed_fee\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "gatewayCode": "BCAVA",
            "paymentAmount": paymentAmount,
            "profileCode": "TKPD_DEFAULT"
        }
    }
]
        
        get_payment_fee = gql(url_get_payment_fee, payload_get_payment_fee, cookies, 'None')

        slashed_fee = get_payment_fee[0]['data']['getPaymentFee']['data'][0]['slashed_fee']
        fee = get_payment_fee[0]['data']['getPaymentFee']['data'][0]['fee']
        total_price = updated_price + price_ongkir + insurance_price + fee + slashed_fee
        print(f"Total price : {total_price}")

        #Updating cart
        url_updateCart = "https://gql.tokopedia.com/graphql/update_cart_occ_multi"
        payload_updateCart = [
            {
                "operationName": "update_cart_occ_multi",
                "query": "mutation update_cart_occ_multi($param: OneClickCheckoutMultiUpdateCartParam) {\n  update_cart_occ_multi(param: $param) {\n    error_message\n    status\n    data {\n      messages\n      success\n      prompt {\n        type\n        title\n        description\n        image_url\n        buttons {\n          text\n          link\n          action\n          color\n          __typename\n        }\n        __typename\n      }\n      toaster_action {\n        text\n        show_cta\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
                "variables": {
                    "param": {
                        "cart": [
                            {
                                "cart_id": cart_id,  # Ganti dengan nilai cart_id
                                "notes": "",
                                "product_id": product_id,  # Ganti dengan nilai product_id
                                "quantity": 1
                            }
                        ],
                        "chosen_address": {
                            "address_id": str(address_id),
                            "district_id": str(district_id),
                            "geolocation": f"{latitude},{longitude}",
                            "mode": 1,
                            "postal_code": str(postal_code)
                        },
                        "profile": {
                            "address_id": str(address_id),
                            "gateway_code": "BCAVA",
                            "is_free_shipping_selected": False,
                            "metadata": "{\"success\":true,\"message\":\"\",\"gateway_code\":\"BCAVA\",\"express_checkout_param\":{\"account_name\":\"\",\"account_number\":\"\",\"bank_id\":\"\",\"pan\":\"\",\"issuer\":\"\",\"card_token\":\"\",\"card_type\":\"\",\"total_saved_card\":\"\",\"installment_term\":\"0\",\"expiry\":\"\",\"bank_code\":\"\",\"pocket_id\":\"\",\"cc_number\":\"\"},\"express_checkout_url\":\"\",\"high_risk_flag\":\"\",\"description\":\"\",\"image\":\"https://images.tokopedia.net/img/toppay/sprites/bca.png\",\"signature\":\"\",\"customer_name\":\"\",\"customer_email\":\"\",\"user_id\":"+str(id)+"}",
                            "service_id": service_id,
                            "shipping_id": shipping_id,
                            "sp_id": sp_id
                        },
                        "skip_shipping_validation": True,
                        "source": "update_qty_notes"
                    }
                }
            }
        ]
        try:
            update_cart = gql(url_updateCart, payload_updateCart, cookies, "None")
            if update_cart and 'data' in update_cart[0]:
                status_update_cart = update_cart[0]['data']['update_cart_occ_multi']['status']
                print(f"Update cart successfuly : {status_update_cart}")
            elif 'errors' in update_cart[0]:
                print("Updating cart failed")
                print(f"Response text: {update_cart}")
        except requests.exceptions.RequestException as e:
            print(f"Error from HTTP Requests while updating cart: {e}")
        except Exception as e:
            print(f"An error occurred while updating cart : {e}")

        
    except NameError as e:
        print(f"NameError: {e}")
        traceback.print_exc()
    except TypeError as e:
        print(f"TypeError: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()

    finally:
        browser.close()
with sync_playwright() as playwright:
    run(playwright, cart_id,product_id)