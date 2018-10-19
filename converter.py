#!/usr/bin/env python3.5
import json, requests, csv
from os import listdir
from transliterate import translit, get_available_language_codes
from download_images import main as download
from config import Config
import logging

def category(value, type_cateory):
    category_id = [str(17000)]
    category_data = json.loads(open(Config.CATEGORY_FILE_PATH + type_cateory + '.json', encoding='utf8').read())
    for index in category_data:
        if value in category_data[index]:
            category_id = [str(category_data[index][0]), str(index)]
        else:
            continue
    return category_id

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]




def convert_product_to_csv(data, type_category, shop):
    product_array_category = []
    image_list = []
    product_array = []
    logging.info('')
    for item_data in data:
        if len(item_data['_NAME_']) > 0:
            name = item_data['_NAME_'].replace('купить', '')[1:]
            seo_keyword = translit(name, 'ru', reversed=True)
            if len(item_data['price']) == 0:
                end_price = ""
            else:
                price = int(item_data['price'])
                #     price = int(''.join(item_data['price'][0]).replace(' ', ''))
                if ''.join(item_data['manufacturer']).lower() in Config.BRAND_NO_CHANGE_PRICE:
                    end_price = price
                else:
                    end_price = int(price - (price * 5 / 100))
            product_array.append({
                "_ID_": "",
                "_MAIN_CATEGORY": "",
                "_CATEGORY_ID_": ','.join(category(''.join(item_data['category']).lower(), type_category)),
                "_NAME_": name,
                "_MODEL_": '',
                "_SKU_": "DIN" + ''.join(item_data['articule']),
                "_EAN_": "",
                "_JAN_": "",
                "_ISBN_": "",
                "_MPN_": "",
                "_UPC_": "",
                "_MANUFACTURER_": ''.join(item_data['manufacturer']),
                "_SHIPPING_": 0,
                "_LOCATION_": Config.SHOP_TRANSLATE[shop],
                "_PRICE_": end_price,
                "_POINTS_": 0,
                "_REWARD_POINTS_": '',
                "_QUANTITY_": 10,
                "_STOCK_STATUS_ID_": 7,
                "_STOCK_STATUS_": ''.join(item_data['stock']),
                "_LENGTH_": 0,
                "_WIDTH_": 0,
                "_HEIGHT_": 0,
                "_WEIGHT_": 0,
                "_META_TITLE_": "Купить " + name + " в интернет магазине Евтерпа доставка по России цена, магазин Москва",
                "_META_H1_": name,
                "_META_KEYWORDS_": "Купить " + name + " в интернет магазине Евтерпа доставка по России цена, магазин Москва",
                "_META_DESCRIPTION_": name + " по лучшей цене заходите у нас отличный выбор " +
                                      name + " только оригинал бесплатная доставка по Москве и России.",
                "_DESCRIPTION_": item_data['description'].replace('Динатон', 'evterpashop'),
                "_PRODUCT_TAG_": '',
                "_IMAGE_": ''.join(item_data['img']).replace('https://dynatone.ru/image/cache/_product/', ''),
                "_SORT_ORDER_": 100,
                "_STATUS_": 1,
                "_SEO_KEYWORD_": seo_keyword.replace(' ', '-').replace('/', '-').replace('.', '').replace(',', '').replace('\'', ''),
                "_DISCOUNT_": '',
                "_SPECIAL_": '',
                "_OPTIONS_": '',
                "_FILTERS_": '',
                "_ATTRIBUTES_": '',
                "_STORE_ID_": '0',
                "_URL_": ''
            })


    for item_product in product_array:
        if item_product['_CATEGORY_ID_'] != '17000':
            image_list.append('https://dynatone.ru/image/cache/_product/' + item_product['_IMAGE_'])
            product_array_category.append(item_product)
    logging.info('After sorting the goods into categories, there are %s goods to import and donwloads images' % (len(product_array_category)))

    # Download image
    # Делим большой список на несколько маленьких
    # image_list_parted = split_list(image_list, wanted_parts=Config.PART_OF_IMAGE_LIST)
    # Проходим по спискам и качаем
    # for item_image_list in image_list_parted:
    #     download(item_image_list)



    with open(Config.OUTPUT_PATH + shop + '/' + type_category + '.json', 'w') as outfile:
        json.dump(product_array_category, outfile)



    with open(Config.OUTPUT_PATH + shop + '/' + type_category + '.csv', "w", newline="", encoding='utf8') as file:
        columns =[
            "_ID_",
            "_MAIN_CATEGORY",
            "_CATEGORY_ID_",
            "_NAME_",
            "_MODEL_",
            "_SKU_",
            "_EAN_",
            "_JAN_",
            "_ISBN_",
            "_MPN_",
            "_UPC_",
            "_MANUFACTURER_",
            "_SHIPPING_",
            "_LOCATION_",
            "_PRICE_",
            "_POINTS_",
            "_REWARD_POINTS_",
            "_QUANTITY_",
            "_STOCK_STATUS_ID_",
            "_STOCK_STATUS_",
            "_LENGTH_",
            "_WIDTH_",
            "_HEIGHT_",
            "_WEIGHT_",
            "_META_TITLE_",
            "_META_H1_",
            "_META_KEYWORDS_",
            "_META_DESCRIPTION_",
            "_DESCRIPTION_",
            "_PRODUCT_TAG_",
            "_IMAGE_",
            "_SORT_ORDER_",
            "_STATUS_",
            "_SEO_KEYWORD_",
            "_DISCOUNT_",
            "_SPECIAL_",
            "_OPTIONS_",
            "_FILTERS_",
            "_ATTRIBUTES_",
            "_STORE_ID_",
            "_URL_"
        ]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(product_array_category)
    logging.info('after processing the file %s is placed in %s' % ((shop + '/' + type_category + '.csv'), Config.OUTPUT_PATH))