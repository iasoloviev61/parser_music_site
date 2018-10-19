import requests, csv, os
from config import Config
import logging


def run_schedule(shop, category, action, type_action):


    params = (
        ('cron_key', Config.SHEDULERS[shop][category][action][type_action]),
    )
    logging.info('Start cron_id %s action %s' % (Config.SHEDULERS[shop][category][action][type_action], action))
    requests.get(Config.CSV_PRO_URL, params=params)


def import_csv(shop, category, action):
    input_file = action + '_' + category + '_' + shop + '.csv'
    raw = open(Config.RAW_PATH + shop + Config.SCHED_EXPORT_PATH + input_file, encoding='utf8')
    data = raw.readlines()
    json_data = []
    json_arr = []

    for item in data:
        newitem = item.split(";")
        json_data.append(newitem)

    for item_json in json_data[1:]:
        json_arr.append({ '_ID_': item_json[0], '_MAIN_CATEGORY_': item_json[1], '_NAME_': item_json[2], '_LOCATION_': item_json[3], '_IMAGE_': item_json[4] })
    logging.info('After import json %s elements' % (len(json_arr)))
    return json_arr

def export_csv(shop, category, action, data):
    output_file = action + '_' + category + '_' + shop + '.csv'
    with open(Config.RAW_PATH + shop + Config.SCHED_IMPORT_PATH + output_file, "w", newline="", encoding='utf8') as file:
        columns =[
            "_ID_",
            "_MAIN_CATEGORY_",
            "_NAME_",
            "_LOCATION_",
            "_IMAGE_",
        ]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)


def del_img(data):
    logging.info('Will be delete a %s images from file-system' % (len(data)))
    for item_img in data:
        path = item_img['_IMAGE_'].replace('http://evterpashop.com/image/', '')
        # os.remove(Config.IMG_PATH + path)
    logging.info('Delete a %s images done' % (len(data)))


def filter_by_shop(shop, data):
    newadata = []
    for item in data:
        if item['_LOCATION_'] == Config.SHOP_TRANSLATE[shop]:
            newadata.append(item)
    logging.info('After running the filter %s items left' % (len(newadata)))
    return newadata

def replace_model(shop):
    raw = open(Config.RAW_PATH + shop + Config.SCHED_EXPORT_PATH + Config.NAME_MODEL_FILE, encoding='utf8')
    data = raw.readlines()
    json_data = []
    json_arr = []

    for item in data:
        newitem = item.split(";")
        json_data.append(newitem)

    for item_json in json_data[1:]:
        json_arr.append({ '_ID_': item_json[0], '_NAME_': item_json[1], '_MODEL_': item_json[2] })
    logging.info('After import json %s elements' % (len(json_arr)))
    for item_model in json_arr:
        item_model['_MODEL_'] = item_model['_ID_']

    with open(Config.RAW_PATH + shop + Config.SCHED_IMPORT_PATH  + Config.NAME_MODEL_FILE, "w", newline="", encoding='utf8') as file:
        columns =[
            "_ID_",
            "_NAME_",
            "_MODEL_"
        ]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(json_arr)
        logging.info('replace model done')

# run_schedule('dinaton', 'gitar', 'del', 'export')
# result = import_csv('dinaton', 'gitar', 'del')
# final = filter_by_shop('dinaton', result)
# export_csv('dinaton', 'gitar', 'removeing', final)
# run_schedule('dinaton', 'gitar', 'del', 'import')