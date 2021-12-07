import json

def making_url(parament,url,right_board,left_board,added,replaced_pass,what_replaced,data):
    param = data.get(parament).split(',')
    if param == ['']:
        return url
    else:
        param.pop(-1)
        param = sorted(list(set(param)))
        text = ''
        for item in param:
            item = item.replace(what_replaced,replaced_pass)
            text = text + added + item
        url=url.split(right_board)
        url=[y for x in url for y in x.split(left_board)]
        url = url[0]+left_board+text+right_board+url[-1]
        return text,url

def changing_url():
    with open('user_data.json') as file:
        data = json.load(file)

    if data.get('chosen_category')=='ноутбуки':
        url = 'https://www.citilink.ru/catalog/noutbuki/?f=discount.any%2Crating.any%2C2589_3&pf=discount.any%2Crating.any'
        price_min = data.get('chosen_min_price')
        price_max = data.get('chosen_max_price')
        url=url+'%2C2589_3&price_min='+price_min+'&price_max='+price_max

        manu = making_url(parament='chosen_manufacture',url=url,added='%2C',right_board='%2C2589_3&pf=discount.any%2Crating.any',left_board='f=discount.any%2Crating.any',replaced_pass='',what_replaced='?',data=data)
        if manu[0]=='h':
            left_board = 'f=discount.any%2Crating.any'
            url = url
            proc = making_url(parament='chosen_processor', url=url, added='%2C277_3',
                              right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                              replaced_pass='d1', what_replaced=' ', data=data)
        else:
            proc = making_url(parament='chosen_processor', url=manu[1], added='%2C277_3',
                              right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=manu[0],
                              replaced_pass='d1', what_replaced=' ', data=data)

        if proc[0]=='h':
            if manu[0]=='h':
                left_board = 'f=discount.any%2Crating.any'
                right_board = '%2C2589_3&pf=discount.any%2Crating.any'
                url = url
                resol = making_url(parament='chosen_resolution',url=url,added='%2C2788_3',right_board=right_board,
                                   left_board=left_board,replaced_pass='kh',what_replaced='х',data=data)
            else:
                right_board = '%2C2589_3&pf=discount.any%2Crating.any'
                url=manu[1]
                resol = making_url(parament='chosen_resolution', url=url, added='%2C2788_3', right_board=right_board,
                                   left_board=manu[0], replaced_pass='kh', what_replaced='х', data=data)
        else:
            if manu[0]=='h':
                left_board = 'f=discount.any%2Crating.any'
                url = proc[1]
                resol = making_url(parament='chosen_resolution', url=url, added='%2C2788_3', right_board=proc[0],
                                   left_board=left_board, replaced_pass='kh', what_replaced='х', data=data)
            else:
                resol = making_url(parament='chosen_resolution', url=proc[1], added='%2C2788_3', right_board=proc[0],
                                   left_board=manu[0], replaced_pass='kh', what_replaced='х', data=data)

        if resol[0]=='h':
            if proc[0]=='h':
                if manu[0]=='h':
                    left_board = 'f=discount.any%2Crating.any'
                    right_board = '%2C2589_3&pf=discount.any%2Crating.any'
                    url = url
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                       right_board=right_board,
                                       left_board=left_board, replaced_pass='', what_replaced='?', data=data)
                else:
                    right_board = '%2C2589_3&pf=discount.any%2Crating.any'
                    left_board =manu[0]
                    url = manu[1]
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                      right_board=right_board,
                                      left_board=left_board, replaced_pass='', what_replaced='?', data=data)
            if proc[0]!='h':
                if manu[0]=='h':
                    left_board = 'f=discount.any%2Crating.any'
                    right_board = proc[0]
                    url = proc[1]
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                      right_board=right_board,
                                      left_board=left_board, replaced_pass='', what_replaced='?', data=data)
                if manu[0]!='h':
                    left_board = manu[0]
                    right_board = proc[0]
                    url = proc[1]
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                      right_board=right_board,
                                      left_board=left_board, replaced_pass='', what_replaced='?', data=data)
        else:
            if proc[0]=='h':
                if manu[0]=='h':
                    url = resol[1]
                    right_board = resol[0]
                    left_board = 'f=discount.any%2Crating.any'
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                      right_board=right_board,
                                      left_board=left_board, replaced_pass='', what_replaced='?', data=data)
                else:
                    matr = making_url(parament='chosen_matrix', url=resol[1], added='%2C14630_3', right_board=resol[0],
                                      left_board=manu[0], replaced_pass='', what_replaced='?', data=data)
            else:
                if manu[0]=='h':
                    url = resol[1]
                    right_board = resol[0]
                    left_board = 'f=discount.any%2Crating.any'
                    matr = making_url(parament='chosen_matrix', url=url, added='%2C14630_3',
                                      right_board=right_board,
                                      left_board=left_board, replaced_pass='', what_replaced='?', data=data)
                else:
                    matr = making_url(parament='chosen_matrix', url=resol[1], added='%2C14630_3', right_board=resol[0],
                                      left_board=manu[0], replaced_pass='', what_replaced='?', data=data)

        if proc[0]=='h':
            if resol[0]=='h':
                if matr[0]=='h':
                    if manu[0]=='h':
                        left_board = 'f=discount.any%2Crating.any'
                        ssd = making_url(parament='chosen_ssd_size', url=url, added='%2C18332_3',
                                         right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                         replaced_pass='d1', what_replaced=' ', data=data)
                        print(ssd)
                    else:
                        left_board = manu[0]
                        ssd = making_url(parament='chosen_ssd_size', url=manu[1], added='%2C18332_3',
                                         right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                         replaced_pass='d1', what_replaced=' ', data=data)
                else:
                    left_board = matr[0]
                    ssd = making_url(parament='chosen_ssd_size', url=matr[1], added='%2C18332_3',
                                     right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                     replaced_pass='d1', what_replaced=' ', data=data)
            else:
                left_board = resol[0]
                if matr[0]=='h':
                    ssd = making_url(parament='chosen_ssd_size', url=resol[1], added='%2C18332_3',
                                     right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                     replaced_pass='d1', what_replaced=' ', data=data)
                else:
                    ssd = making_url(parament='chosen_ssd_size', url=matr[1], added='%2C18332_3',
                                     right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                     replaced_pass='d1', what_replaced=' ', data=data)
        else:
            left_board = proc[0]
            if matr[0]=='h':
                if resol[0]=='h':
                    ssd = making_url(parament='chosen_ssd_size', url=proc[1], added='%2C18332_3',
                                     right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                     replaced_pass='d1', what_replaced=' ', data=data)
                else:
                    ssd = making_url(parament='chosen_ssd_size', url=resol[1], added='%2C18332_3',
                                     right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                     replaced_pass='d1', what_replaced=' ', data=data)
            else:
                ssd = making_url(parament='chosen_ssd_size', url=matr[1], added='%2C18332_3',
                                 right_board='%2C2589_3&pf=discount.any%2Crating.any', left_board=left_board,
                                 replaced_pass='d1', what_replaced=' ', data=data)

        RAM = data.get('chosen_RAM_size').split(',')
        if RAM == ['']:
            if ssd[0]!='h':
                url_final = ssd[1]
            else:
                if matr[0] != 'h':
                    url_final = matr[1]
                else:
                    if resol[0] != 'h':
                        url_final = resol[1]
                    else:
                        if proc[0] != 'h':
                            url_final = proc[1]
                        else:
                            if manu[0] != 'h':
                                url_final = manu[1]
        else:
            RAM.pop(-1)
            param = sorted(list(set(RAM)))
            text = ''
            for item in param:
                if item == '4 gb':
                    item = '%2C2579_3'
                if item == '8 gb':
                    item = '%2C2581_3'
                if item == '16 gb':
                    item = '%2C4811_3'
                if item == '32 gb':
                    item = '%2C4812_3'
                text = text + item
                if ssd[0] != 'h':
                    link = ssd[1]
                    variable = ssd[0]
                else:
                    if matr[0] != 'h':
                        link = matr[1]
                        variable = matr[0]
                    else:
                        if resol[0] != 'h':
                            link = resol[1]
                            variable = resol[0]
                        else:
                            if proc[0] != 'h':
                                link = proc[1]
                                variable = proc[0]
                            else:
                                if manu[0] != 'h':
                                    link = manu[1]
                                    variable = manu[0]
                url = link.split('%2C2589_3&pf=discount.any%2Crating.any')
                if url == link:
                    url = link.split('%2C2589_3&price')
                url_final = url[0] + text + '%2C2589_3&price' + url[-1]
        with open('url.txt', 'w') as file:
            file.write(url_final)

def main():
    changing_url()

if __name__=='__main__':
    main()
