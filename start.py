# /usr/bin/env python
import sys, argparse
from run_get_jobs import collect_jsons
from converter import convert_product_to_csv
from csv_pro_requests import *
import logging

def run_app(shop, category, spider):
    # Пункт 1.
    # Блок парсера товаров
    #
    logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename="./log/" + spider + category + ".log", level=logging.INFO)
    logger=logging.getLogger(__name__)

    logging.info("Program started")
    logging.info('First phase start')
    main_file = collect_jsons(spider)
    logging.info("First phase done!")


    # Пункт 2.
    # Блок удаления товаров перед импортом
    #

    # Запустить экспорт товаров из магазина
    # в файл './raw/shop/имя_магазина/shedulers/export/имя_действия--категория--магазин.csv'
    logging.info('Second phase start')
    run_schedule(shop, category, 'del', 'export')
    # конвертируем полученный файл в список
    result = import_csv(shop, category, 'del')
    # выбрасываем из списка всё, что не относится к текущему указанному магазину - параметр shop
    final = filter_by_shop(shop, result)
    # Удаляем картинки из файловой системы
    # del_img(final)
    # формируем файл для импорта в opencart, конвертируем список в формат csv
    export_csv(shop, category, 'del', final)
    # Запускаем задание импорта, в данном случае удаление товаров
    run_schedule(shop, category, 'del', 'import')
    logging.info('Second phase done')

    # Пункт 3.
    # Конвертация полученной информации из парсера(п.1) в csv файл для импорта + загрузка изображений
    # файл будет находиться в ./output/shop/имя_магазина/имя_категории.csv
    convert_product_to_csv(main_file, category, spider)

    # Пункт 4.
    # Испорт итогового файла в opencart
    #
    run_schedule(shop, category, 'add', 'import')

    # Пункт 5.
    # Экспорт всех товаров, обработка - проставление моля модель равное полю ID
    # Импорт итогового файла в магазин
    run_schedule(shop, 'all', 'update', 'export')
    replace_model(shop)
    run_schedule(shop, 'all', 'update', 'import')

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--opencartshop')
    parser.add_argument('-c', '--category')
    parser.add_argument('-s', '--spider')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    # print (namespace)

    if namespace.opencartshop:
        # print(len(collect_jsons(namespace.name)))
        # json_data = collect_jsons(namespace.name)
        # convert_product_to_csv(json_data, namespace.category, namespace.name)
        run_app(namespace.opencartshop, namespace.category, namespace.spider)
    else:
        print("Please, input name spider!")