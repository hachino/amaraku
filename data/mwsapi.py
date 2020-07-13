import base64
import datetime
import hashlib
import hmac
import requests
import six
import urllib.parse
from bs4 import BeautifulSoup
import numpy as np
import xml.etree.ElementTree as et
import xml.dom.minidom as md


#-----リクエスト時の定数-----
AMAZON_CREDENTIAL = {
    'SELLER_ID': 'A2RC3A0BA0OA3R',
    'ACCESS_KEY_ID': 'AKIAIO4K6MR5WUGQYAWQ',
    'ACCESS_SECRET': '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',
    'MarketplaceId': 'A1VC38T7YXB528',
    }
DOMAIN = 'mws.amazonservices.jp'
ENDPOINT = '/Products/2011-10-01'
#-----

#-----API叩く際の複雑な変換-----
def amareq(DATA):
    query_list = list()
    for k, v in sorted(DATA.items()):
        query_list.append('{}={}'.format(k, urllib.parse.quote(v, safe='')))
    query_string = "&".join(query_list)

    canonical = "{}\n{}\n{}\n{}".format(
        'POST', DOMAIN, ENDPOINT, query_string
    )

    h = hmac.new(
        six.b(AMAZON_CREDENTIAL['ACCESS_SECRET']),
        six.b(canonical), hashlib.sha256)

    signature = urllib.parse.quote(base64.b64encode(h.digest()), safe='')

    url = 'https://{}{}?{}&Signature={}'.format(
        DOMAIN, ENDPOINT, query_string, signature)

    response = requests.post(url)
    soup = BeautifulSoup(response.content.decode(), "html.parser")
    return(soup)
#-----

#-----JANコードから ASIN,カテゴリ,カテゴリランキングを取得-----
def asin_search(JAN):
    
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    data = {
        'AWSAccessKeyId': AMAZON_CREDENTIAL['ACCESS_KEY_ID'],
        'Action': 'GetMatchingProductForId',
        'SellerId': AMAZON_CREDENTIAL['SELLER_ID'],
        'SignatureMethod': 'HmacSHA256',
        'MarketplaceId': AMAZON_CREDENTIAL['MarketplaceId'],
        'SignatureVersion': '2',
        'Timestamp': timestamp,
        'Version': '2011-10-01',
        'IdType': 'JAN',
        'IdList.Id.1': JAN
    }

    soup = amareq(data)

    items_moto = soup.find_all("ns2:title")
    asins_moto = soup.find_all("asin")
    categorys = soup.find_all("salesrank")
    items = []
    asins = []

    for asin  in asins_moto:
        asins.append(asin.text)
   
    return asins
#-----

#-----ASINから 値段・価格を取得-----
def product_search(ASINS,RAKU_PRICE):

    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    data = {
        'AWSAccessKeyId': AMAZON_CREDENTIAL['ACCESS_KEY_ID'],
        'Action': 'GetCompetitivePricingForASIN',
        'SellerId': AMAZON_CREDENTIAL['SELLER_ID'],
        'SignatureMethod': 'HmacSHA256',
        'MarketplaceId': AMAZON_CREDENTIAL['MarketplaceId'],
        'SignatureVersion': '2',
        'Timestamp': timestamp,
        'Version': '2011-10-01',
        'ItemCondition': 'NEW',
        'ExcludeMe': 'true',
    }


    key = []
    value = []
    prices_list = []


    for i, asin in enumerate(ASINS):
        key.append("ASINList.ASIN." + (str(i+1)))
        value.append(asin)

    asin_dict = dict(zip(key,value))
    data.update(asin_dict)


    soup = amareq(data)
    # print(soup)

    prices = soup.find_all("competitivepricing")
    

    for price in prices:
        price = price.find_all("listingprice")
        if len(price) == 0:
            prices_list.append(0)
        for p in price:
            prices_list.append(float(p.contents[1].text))
    
    value = getNearestValue(prices_list, RAKU_PRICE)

    price = value[1]
    index = value[0]

    sellers = soup.find_all("numberofofferlistings")
    categorys = soup.find_all("salesrankings")

    try:
        asin = ASINS[index]
    except:
        asin = ""

    try:
        category = categorys[index].find("productcategoryid").text
    except:
        category = ""

    try:
        rank =  categorys[index].find("rank").text
    except:
        rank = ""

    try:
        seller = sellers[index].contents[0].text
    except:
        seller = ""

    return asin, price, seller, category, rank
#-----

#-----ASIN・価格から手数料を取得-----
def fee_search(ASIN, PRICE):

    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    data = {
        'AWSAccessKeyId': AMAZON_CREDENTIAL['ACCESS_KEY_ID'],
        'Action': 'GetMyFeesEstimate',
        'SellerId': AMAZON_CREDENTIAL['SELLER_ID'],
        'SignatureMethod': 'HmacSHA256',
        'SignatureVersion': '2',
        'Timestamp': timestamp,
        'Version': '2011-10-01',
        'FeesEstimateRequestList.FeesEstimateRequest.1.MarketplaceId': AMAZON_CREDENTIAL['MarketplaceId'],
        'FeesEstimateRequestList.FeesEstimateRequest.1.IdType': 'ASIN',
        'FeesEstimateRequestList.FeesEstimateRequest.1.IdValue': ASIN,
        'FeesEstimateRequestList.FeesEstimateRequest.1.IsAmazonFulfilled': 'true',
        'FeesEstimateRequestList.FeesEstimateRequest.1.Identifier': 'request1',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.ListingPrice.Amount': PRICE,
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.ListingPrice.CurrencyCode':'JPY',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.Shipping.Amount':'0.00',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.Shipping.CurrencyCode':'JPY',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.Points.PointsNumber':'0',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.Points.PointsMonetaryValue.Amoun':'0',
        'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.Points.PointsMonetaryValue.CurrencyCode': 'JPY'
    }

    soup = amareq(data)
    # print(soup)

    prices = soup.find_all("totalfeesestimate")

    try:
        fee = prices[0].contents[1].text
    except:
        fee = ""

    return fee
#-----

def getNearestValue(list, num):

    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx,list[idx]


# if __name__ == '__main__':

#     asins = asin_search("4971710282351")
#     print(asins)
    
#     data2 = product_search(asins,2596)
#     print(data2)
 
#     data3 = fee_search(data2[0], str(data2[1]))
#     print(data3)