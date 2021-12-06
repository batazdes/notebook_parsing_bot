import lxml.html
from notebook_parser_without_pages import citilink_parser_base
import requests
import json

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

def citilink_parser():
    html_citilink = requests.Session()
    response = html_citilink.get(
        url=open('url.txt').read(),
        headers=headers)

    if response.status_code!=200:
        with open('result_data_citilink.json', 'w') as file:
            nothing = []
            json.dump(nothing, file, ensure_ascii=False, indent=1)

    if response.status_code==200:
        tree = lxml.html.document_fromstring(response.text)

        last_page = tree.xpath("//*[@class='PaginationWidget__page js--PaginationWidget__page PaginationWidget__page_last PaginationWidget__page-link']/@data-page")
        last_next_page = tree.xpath("//*[@class='PaginationWidget__page js--PaginationWidget__page PaginationWidget__page_next PaginationWidget__page-link']/@data-page")

        if last_page!=[]:
            for i in range(1,int(last_page[-1])+1):
                url = open('url.txt').read()+f'&p={i}'
                final_objects = citilink_parser_base(url=url)
                with open('result_data_citilink.json','r') as file:
                    data = json.load(file)
                final_data = data+final_objects
                with open('result_data_citilink.json','w') as file:
                    json.dump(final_data, file, ensure_ascii=False, indent=1)
        else:
            if last_next_page!=[]:
                for i in range(1, int(last_next_page[-1]) + 1):
                    url = open('url.txt').read() + f'&p={i}'
                    final_objects = citilink_parser_base(url=url)
                    with open('result_data_citilink.json', 'r') as file:
                        data = json.load(file)
                    final_data = data + final_objects
                    with open('result_data_citilink.json', 'w') as file:
                        json.dump(final_data, file, ensure_ascii=False, indent=1)
                    print(f'Работа со страницой {i} завершена')
            else:
                url = open('url.txt').read()
                final_objects = citilink_parser_base(url=url)
                with open('result_data_citilink.json', 'w') as file:
                    json.dump(final_objects, file, ensure_ascii=False, indent=1)

    with open('url.txt','w')as file:
        file.write('')
def main():
    citilink_parser()

if __name__=='__main__':
    main()