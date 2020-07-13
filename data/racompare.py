import rakuama

cosme = {
    'asin_list' : "/Users/akira_mac/python_work/amaraku/data/cosme/asin_list_cosme.text",
    'item_csv_path' : "/Users/akira_mac/python_work/amaraku/data/cosme/cosme.csv",
    'today_data_path' : "/Users/akira_mac/python_work/amaraku/data/cosme/today_data_cosme.text",
    'genreid' : "100939",
}

pet = {
    'asin_list' : "/Users/akira_mac/python_work/amaraku/data/pet/asin_list_pet.text",
    'item_csv_path' : "/Users/akira_mac/python_work/amaraku/data/pet/pet.csv",
    'today_data_path' : "/Users/akira_mac/python_work/amaraku/data/pet/today_data_pet.text",
    'genreid' : "101213",
}

kaden = {
    'asin_list' : "/Users/akira_mac/python_work/amaraku/data/kaden/asin_list_kaden.text",
    'item_csv_path' : "/Users/akira_mac/python_work/amaraku/data/kaden/kaden.csv",
    'today_data_path' : "/Users/akira_mac/python_work/amaraku/data/kaden/today_data_kaden.text",
    'genreid' : "100026",
}

rakuama.asin_list_maker(cosme['asin_list'],cosme['genreid'])
rakuama.price_compare(cosme['asin_list'],cosme['item_csv_path'],cosme['today_data_path'],cosme['genreid'])

rakuama.asin_list_maker(pet['asin_list'],pet['genreid'])
rakuama.price_compare(pet['asin_list'],pet['item_csv_path'],pet['today_data_path'],pet['genreid'])

rakuama.asin_list_maker(kaden['asin_list'],kaden['genreid'])
rakuama.price_compare(kaden['asin_list'],kaden['item_csv_path'],kaden['today_data_path'],kaden['genreid'])
