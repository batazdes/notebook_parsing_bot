import lxml.html
import requests

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

def citilink_parser_base(url):
    html_citilink = requests.Session()
    response = html_citilink.get(
        url=url,
        headers=headers)

    with open('citilink.html', 'w') as file:
        file.write(response.text)

    tree = lxml.html.document_fromstring(response.text)
    names_model = tree.xpath("//*[@class='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist']/div[@class='ProductCardHorizontal__header-block']/a/text()")
    links = tree.xpath("//*[@class='product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist']/div[@class='ProductCardHorizontal__image-block']/a/@href")
    links_image = tree.xpath("//*[@class='ProductCardHorizontal__image-block']/a/picture[@class='ProductCardHorizontal__picture js--ProductCardInListing__picture']/source/@srcset")

    prices_not_for_using = tree.xpath("//*[@class='ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price ']/text()")
    prices = []
    for price in prices_not_for_using:
        price = price.replace('\n','').replace(' ','')
        prices.append(price)

    final_objects = []
    for i in range(0,len(names_model)):
        final_objects.append(
            {
                'name_model': names_model[i].replace('/',''),
                'link': 'https://www.citilink.ru' + links[i],
                'price': prices[i]
            }
        )

        response_image = requests.get(links_image[i])
        with open(f'C:\\Users\\79663\\PycharmProjects\\notebook_parsing_bot\\Notebooks_photo\\{names_model[i].replace("/","")}.jpg', 'wb') as f:
            f.write(response_image.content)
    return final_objects

def main():
   citilink_parser_base(url='https://www.citilink.ru/catalog/noutbuki/')

if __name__=="__main__":
    main()

