from xml.sax.xmlreader import InputSource
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import telegram_send
ua = UserAgent()
headers = {'User-Agent': ua.random}
#Вводим ссылку
url = input('ВВеди ссылку на товар с сайта Zara.com: ')
response = requests.get(url, headers=headers)
BS = BeautifulSoup(response.content, 'lxml')

#вычленяем артикул товара из ссылки
article= (url[url.find("&v2")-9:url.find("&v2")])
str_start= 'product-detail-size-selector-product-detail-product-size-selector-article-'.replace("article", article)
 #вводим значение размера. Берется порядковый номер из таблици размеров на странице товара
size= input('Введите порядковый номер размера, начиная с 0 (например, размер S идет первым по порядку- это 0, М-1, L-2 и т.д.): ')
str_end= 'item-size'.replace("size", size)

item_id= BS.find( id= str_start + str_end)
data= item_id.get("data-qa-action")

while data!= "size-in-stock":
    print('Товара нет в наличии')
    time.sleep(1800) #делает запрос раз в 30 мин
else:
    telegram_send.send(messages= ['Товар есть в наличии', url])