import re

def _clean_url(url):
    if '?' not in url:
        return url+'?'
    url_root = url.split('?')
    filter_split = url_root[1].split('&')
    rempve_page = [i for i in filter_split if 'page=' not in i]
    filters = '&'.join(rempve_page)
    return url_root[0]+'?'+ filters



def page_clean_url(url):
    if '?' not in url:
        return url+'?'
    clean_url = re.sub('&?page=[0-9]+','',url)
    return clean_url


def sort_clean_url(url):
    clean_url = re.sub("&?sort_by=[a-zA-Z]+",'', url)
    return clean_url


'''
    price  -> one value
    color  -> [val1, val2, ...]
    size   -> [val1, val2, ...]
    gender -> [val1, val2, ...]
'''

PRICE = {'0':[0,99999], '1':[0,100], '2':[100,200], '3':[200,300], '4':[300,400], '5':[400,500]}
COLORS = ['All_Color', 'Black', 'White', 'Red', 'Blue', 'Green']
SIZES = ['All_Size', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
GENDER = ['All_Gender', 'Male', 'Female', 'Baby']

def get_back_filter_params(kwargs):
    price = kwargs.get('price', '')
    price = PRICE.get(price, [])

    colors = []
    for i in COLORS:
        value = kwargs.get(i, '')
        if i == 'All_Color' and value:
            break
        if value:
            colors.append(i)
    
    sizes = []
    for i in SIZES:
        value = kwargs.get(i, '')
        if i == 'All_Size' and value:
            break
        if value:
            sizes.append(i)
    
    gender = []
    for i in GENDER:
        value = kwargs.get(i, '')
        if i == 'All_Gender' and value:
            break
        if value:
            gender.append(i)

    return price, colors, sizes, gender




def get_front_filter_params(kwargs):
    price = kwargs.get('price', '0')

    colors = dict()
    for i in COLORS:
        value = kwargs.get(i, '')
        if value:
            colors[i] = 'checked'
        else :
            colors[i] = value

    sizes = dict()
    for i in SIZES:
        value = kwargs.get(i, '')
        if value:
            sizes[i] = 'checked'
        else :
            sizes[i] = value
    
    gender = dict()
    for i in GENDER:
        value = kwargs.get(i, '')
        if value:
            gender[i] = 'checked'
        else :
            gender[i] = value

    return price, colors, sizes, gender




def filter_clean_url(url):
    clean_url = re.sub("&?price=[0-9]+",'', url)
    clean_url = re.sub("&?color-[0-6]=[a-zA-Z]+",'', clean_url)
    clean_url = re.sub("&?size-[0-7]=[a-zA-Z]+",'', clean_url)
    clean_url = re.sub("&?gender-[0-4]=[a-zA-Z]+",'', clean_url)
    return clean_url

def recreate_url(url, page):
    part1 = url.split("&page_url")
    part2 = page.split('?')
    new_url = part1[0]
    if len(part2) > 1:
        new_url +='&'+filter_clean_url(part2[1])
    return new_url



def get_search(url):
    params = url.split('?')
    if len(params) == 1:
        return dict()

    # getting all params
    params = re.findall(r'([^=&]+)=([^=&]+)', params[1])
    
    # assigning keys with values
    result = dict()
    for key, val in params:
        result.setdefault(key, val)
    
    return result