 #!/usr/bin/env python3
import urllib.request 
from bs4 import BeautifulSoup
import re
import csv

DOMAIN = "http://posuda-mix.ru"
CATEGORY_URL = "https://www.klenmarket.ru/shop/inventory/kitchen-equipment/pans-cauldrons-saji/aluminum-pans/"




url_from_rak = 'http://rakporcelain.com/productdetails.php?catid=51'

url_of_posuda_mix= 'http://posuda-mix.ru/shop/farfor/RAK/Bez_dekora/group_824/?on_page=100'

def parse(html):
	soup = BeautifulSoup(html)



	soup2 = BeautifulSoup(get_html(url_from_rak))


	dict = {}
	dict2 = {}
	dict3 = {}
	dict4 = {}

	for div_item in soup2.find_all('div', class_="product_sub_items"):
		name_item = " ".join(div_item.find('div', class_="product_sub_items_name").get_text().replace('/','').split())

		article = div_item.find('div', class_="product_sub_items_name").get_text().split()[0]

		article_with_dig = article
		#print(article)



		article = ''.join([i for i in article if not i.isdigit()])

		image = div_item.find('img')['src'].replace('small', 'big')
		article_from_img= image.split('_').pop().replace('.png','')

		print(len(article_from_img))

		article_from_img = ''.join([i for i in article_from_img[0:14] if not i.isdigit()])+article_from_img[14:16]

		article_from_img_without_dig = ''.join([i for i in article_from_img if not i.isdigit()])

		dict.setdefault(article,image)
		dict2.setdefault(article_with_dig,image)
		dict3.setdefault(article_from_img, image)
		dict4.setdefault( article_from_img_without_dig,image)
	print(dict3)



	#name_category = '1883 > '+ soup.find('div', class_="product-list-intro").find('h1').get_text()
	#print(name_category)

	count_of_items = 0
	change_photo= 0 
	for n in range(0,1):
		items = []


		categ = ' '.join(soup.find('div',class_="main-text").find('h1').get_text().split())
		print(categ)
		for item_div in soup.find_all('td',class_="b-item-name"):





			count_of_items = count_of_items + 1
			href_item = item_div.find('a')['href']

			name_of_item = item_div.find('a').get_text().split()

			name_of_item = ' '.join(name_of_item)
			print(name_of_item)

			print(href_item)

			address_of_item = DOMAIN+ href_item

			soup2 = BeautifulSoup(get_html(address_of_item))



			
			image_item = ''
			if(name_of_item =="Емкость глубокая квадратная BURD25" ):
				pass
				
			else :	
				if(name_of_item !="Сливочн" ):
					image_item = DOMAIN+soup2.find('div', class_="image_cell_inn").find('a')['href']


				image_bool = False
				


				print(image_item)

				description_div = soup2.find('div', class_="description_row")

				div =description_div.find_all('div', class_="description_cell")

				if(div[0].find('strong').get_text()!=None):
					article_item = div[0].find('strong').get_text()
				print(article_item)

				if(div[1].find('a').get_text() != None):
					proizvoditel = div[1].find('a').get_text()
				print(proizvoditel)
				try:

					obem = div[2].get_text()
				except IndexError:
					obem = ""
				print(obem)

				price = soup2.find('div', class_="b-item-price").find('span').get_text().replace(',','.')
				print(price)

				
				atricle_without_dig = ''.join([i for i in article_item if not i.isdigit()])

				if (dict2.get(article_item) == None):
					if (dict.get(atricle_without_dig)!= None):
						image_item = dict.get(atricle_without_dig)
						change_photo = change_photo +1
						image_bool = True

				if(dict3.get(article_item) != None):
					image_item = dict3.get(article_item)
					change_photo = change_photo +1
					image_bool = True


				if(dict2.get(article_item)!= None):
					image_item = dict2.get(article_item)

					change_photo = change_photo +1
					image_bool = True

			#if (image_bool is False and dict4.get(atricle_without_dig)!= None ):
			#	image_item = dict4.get(atricle_without_dig)



			


				#.replase('href="/shop/producers/rak-porcelain/"','href="/product-category/posuda/rak-porcelain-oae/"')
			#print(description_div)

			#image_item = item_div.find('div', class_="cat-goods__item-preview").find('a').find('img')['src']#Картинка товара

			#name_of_item = soup2.find('h1', class_="product-title").get_text()#Имя товара

			#article_item = item_div.find('span', class_="text-warning").get_text()#Артикль

			#price_item = item_div.find('span', class_="price__current-value").get_text()#Цена товара

			#table = soup2.find('div', class_="col-12 col-md-8").find('table')#Описание товара


			#href_price = soup2.find('a', class_="btn btn-dark w-100 my-3")['href']

			#soup3 = BeautifulSoup(get_html(href_price))
			#price_item = soup3.find('span', class_="price_value").get_text()
			name_category = 'Фарфоровая посуда > RAK Porcelain (ОАЭ) > Без декора >  ' + categ
			items.append({
				
				'name': name_of_item,
				'img_src': image_item,
				'price': price,
				'proizvoditel': proizvoditel,
				'article': article_item,
				'obem':  obem,
				#'article' : article_item,
				'category': name_category,
				'def_url': address_of_item,
			})
	csvfilename = name_category+".csv"
	with open (csvfilename, 'w') as csvfile:
		writer =  csv.writer(csvfile)
		writer.writerow(("Имя", "Изображения", 'Цена','Производитель' , 'Артикул','Короткое описание', "Категории","Исходный адрес"))
		for item in items:
			writer.writerow(
				(item['name'],item['img_src'],item['price'], item['proizvoditel'],item['article'],item['obem'],item['category'],item['def_url'])
				) 

	print('COunt all items:', count_of_items)

	print('COunt of all items where changed add of IMG:', change_photo)

def get_html(url):
 	resposnse = urllib.request.urlopen(url)
 	return resposnse.read()

def main():


	parse(get_html(url_of_posuda_mix))

	#soupmain = BeautifulSoup(get_html('https://www.klenmarket.ru/shop/inventory/kitchen-equipment/pans-cauldrons-saji/'))

	'''for categ in soupmain.find_all('a', class_="shop-eq-list__cats-item"):
		print(categ['href'])
		parse(get_html(DOMAIN + categ['href']))'''
	
		
if __name__ == '__main__':
	main()