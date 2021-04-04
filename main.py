import requests
from bs4 import BeautifulSoup
import time
import fake_useragent

user_agent = fake_useragent.UserAgent(verify_ssl=False).random
start_time = time.time()
input_url = str(input("Введите адрес сайта в формате http://адрес/ : "))
url_check = input_url.split('://')[1]
if url_check[-1] == '/':
    url_check = url_check[:-1]
if input_url[-1] == '/':
    input_url = input_url[:-1]
HEADERS = {
    'user-agent': user_agent,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}


class Request(object):
    def __init__(self, url, head):
        self.url = url
        self.headers = head

    def response(self):
        site_response = requests.get(url=self.url, headers=self.headers, allow_redirects=False).text
        soup = BeautifulSoup(site_response, 'lxml')
        return soup


class MapFirstStep(Request):
    def site_links(self):
        soup = self.response()
        links = soup.find_all('a')
        link_list = []
        try:
            for lin in links:
                link_list.append(lin.get('href'))
        except Exception as ex:
            print(ex)
        return link_list


class ListWork(object):
    def __init__(self, list_for_unique):
        self.unique = list_for_unique

    def unique_list(self):
        unique_list = []
        for i in self.unique:
            if i not in unique_list:
                unique_list.append(i)
        return unique_list


class FinnalyList(object):
    def __init__(self, url, unique_list):
        self.url = url
        self.unique = unique_list

    def finnaly_cleared_list(self):
        clear_list = []
        clear_list_only_map = []
        for j in self.unique:
            if j is None:
                continue
            if 'https://' in j or 'http://' in j:
                if j[-1] == '/':
                    j = j[0:-1]
                if j.split('://')[1] == input_url.split('://')[1]:
                    continue
                else:
                    clear_list.append(j)
            elif len(j) > 3 and '/' in j:
                clear_list.append(self.url + j)
            else:
                continue
        for k in clear_list:
            if str(self.url) in k:
                clear_list_only_map.append(k)
        return clear_list_only_map

links = []
print(input_url)


def finnaly_list_response(url, header):
    first_links_list = MapFirstStep(url=url, head=header).site_links()
    unique_l = ListWork(first_links_list).unique_list()
    finnaly_first_list = FinnalyList(url, unique_l).finnaly_cleared_list()
    return finnaly_first_list


finnaly_first_list = finnaly_list_response(url=input_url, header=HEADERS)


if finnaly_first_list:
    for first_link in finnaly_first_list:
        if first_link.split('://') == url_check:
            pass
        else:
            print('\t*' + first_link)
            links.append(first_link)
            try:
                if requests.get(url=first_link, headers=HEADERS, allow_redirects=False).status_code == 200:
                    finnaly_second_list = finnaly_list_response(first_link, header={
                        'user-agent': fake_useragent.UserAgent(verify_ssl=False).random,
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
                    for second_link in finnaly_second_list:
                        print('\t\t-' + second_link)
                        links.append(second_link)
                else:
                    continue
            except Exception:
                pass


print(f'Время обработки сайта составило {time.time()-start_time}')
print(f'Количество найденный ссылок = {len(links)}')
for link in links:
    with open(f"links.txt", 'a') as links_write:
        links_write.write(f"{link}\n")
print(f'Все ссылки сохраненны в файле "links.txt"')