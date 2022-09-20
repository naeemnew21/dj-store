import re

def clean_url(url):
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
    clean_url = page_clean_url(url)
    clean_url = re.sub("&?sort_by=[a-zA-Z]+",'',clean_url)
    return clean_url

