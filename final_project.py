# functie care cauta un url de Google Maps prin codul html al paginii web, in interiorul tagurilor <a>
def search_maps_1(url):
    import urllib.request
    import re
    import bs4

    header = { 'User-Agent':'Safari Mozilla Chrome Firefox' }  # header pentru folosirea unui User-Agent
    req = urllib.request.Request(url, data=None, headers=header)

    try:
        with urllib.request.urlopen(req) as page:

            page_output = page.read( )
            parse = bs4.BeautifulSoup(page_output, 'html.parser')

            initial_maps = None

            for link in parse.find_all('a'):
                lk = link.get('href')
                pattern = r"^https://.*maps.*"

                if re.match(pattern, lk):
                    initial_maps = lk
                    break

            return initial_maps

    except:
        return None


# functie care cauta un url de Google Maps prin codul html al paginii web, in interiorul iframe-urilor
def search_maps_2(url):
    import urllib.request
    import re
    import bs4

    header = { 'User-Agent':'Safari Mozilla Chrome Firefox' }
    req = urllib.request.Request(url, data=None, headers=header)

    try:
        with urllib.request.urlopen(req) as page:
            page_output = page.read( )

            parse = bs4.BeautifulSoup(page_output, 'html.parser')

            initial_maps = None

            for link in parse.find_all('iframe'):
                lk = link.get('src')
                pattern = r"^https://.*maps.*"

                if re.match(pattern, lk):
                    initial_maps = lk
                    break

            return initial_maps

    except:
        return None


# functie pentru cautarea adresei in interiorul unei adrese web primite ca parametru prin url
def find_address(website_name):
    import urllib.request
    import re
    import bs4
    import requests

    # am creat url-ul in functie se numele domeniului si am trimis o cerere catre acesta
    url = 'https://' + website_name
    header = { 'User-Agent':'Safari Mozilla Chrome Firefox' }
    req = urllib.request.Request(url, data=None, headers=header)

    page = urllib.request.urlopen(req)

    # am extras codul html al paginii
    page_output = page.read( )

    parse = bs4.BeautifulSoup(page_output, 'html.parser')

    ok = 0
    initial_maps = None

    # am verificat daca url-ul Google Maps se afla in prima pagina a site-ului
    if search_maps_1(url) is not None:
        initial_maps = search_maps_1(url)
        ok = 1

    else:
        if search_maps_2(url) is not None:
            initial_maps = search_maps_2(url)
            ok = 2

    # in caz contrar, am cautat prin toate tag-urile <a> si iframe-urile din pagina respectiva
    # url-uri care trimit catre alte pagini din site
    if ok == 0:
        for link in parse.find_all('a'):
            lk = link.get('href')
            pattern = url + r'\S+'

            if re.match(pattern, lk):
                if search_maps_1(lk) is not None:
                    initial_maps = search_maps_1(lk)
                    ok = 1
                    break

                else:
                    if search_maps_2(lk) is not None:
                        initial_maps = search_maps_2(lk)
                        ok = 2
                        break

        for link in parse.find_all('iframe'):
            lk = link.get('src')
            pattern = url + r'\S+'

            if re.match(pattern, lk):
                if search_maps_1(lk) is not None:
                    initial_maps = search_maps_1(lk)
                    ok = 1
                    break

                else:
                    if search_maps_2(lk) is not None:
                        initial_maps = search_maps_2(lk)
                        ok = 2
                        break

    # pentru url-ul de Google Maps, am facut o cerere pentru a obtine forma totala a sa
    # in cadrul careia se afla coordonatele locatiei, pe care le-am extras
    if ok == 2:

        req2 = urllib.request.Request(initial_maps, data=None, headers=header)

        page2 = urllib.request.urlopen(req2)

        page2_output = page2.read( ).decode('utf-8')

        pattern2 = r'0x[a-fA-F0-9]+:0x[a-fA-F0-9]+'

        matches = re.findall(pattern2, page2_output)

        for match in matches:
            coords = match

        substring = ":"
        coords = coords.split(substring)

        coord1 = coords[0]
        coord2 = coords[1]

    else:
        if ok == 1:
            response = requests.head(initial_maps, allow_redirects=True)
            final_maps = response.url

            substring1 = "!1s"
            substring2 = "!8m"
            substring3 = ":"

            final_maps = final_maps.split(substring1)
            final_maps = final_maps[1]

            final_maps = final_maps.split(substring2)
            final_maps = final_maps[0]

            final_maps = final_maps.split(substring3)

            coord1 = final_maps[0]
            coord2 = final_maps[1]

    # am generat o cheie API si am folosit-o impreuna cu textul extras
    # pentru a accesa codul html al paginii
    if ok != 0:
        url_maps = "https://maps.googleapis.com/maps/api/place/details/json?cid="
        url_maps = url_maps + coord2
        url_maps = url_maps + "&&key=AIzaSyCf7Ppnep-6KRtE9kvG-zMRvU4be5fFWRs"

        req_maps = urllib.request.Request(url_maps, data=None, headers=header)
        maps_page = urllib.request.urlopen(req_maps)

        maps_page = maps_page.read( ).decode('utf-8')

        maps_parse = bs4.BeautifulSoup(maps_page, "html.parser")

        text_content = maps_parse.get_text( )

        # de la linnia "formatted_address" am extras datele adresei
        pattern = r'"formatted_address"\s*:\s*"([^"]+)"'

        matches = re.findall(pattern, text_content)

        # am prelucrat datele
        address = matches[0].split(",")

        s1 = address[0]
        city = address[1]
        s2 = address[2]
        country = address[3]

        s1 = s1.split(" ")
        street_number = s1[0]

        count = 0
        street = ""
        for elem in s1:
            count = count + 1;

            if count > 1:
                street = street + elem + " "

        s2 = s2.split(" ")
        region = s2[1]
        postal_code = s2[2]

        city = city.split(" ")
        city = city[1]

        country = country.split(" ")
        country = country[1]

        # am afisat adresa gasita
        print(country, region, city, postal_code, street, street_number, sep=",")
        return 1

    # in cazul in care nu a fost gasita o adresa, am afisat un mesaj
    else:
        print("Address not found for " + website_name)
        return 0


# functie care verifica daca o exista o adresa web cu denumirea citita
def check(website_name):
    import requests
    header = { 'User-Agent':'Safari Mozilla Chrome Firefox' }
    response = requests.get('https://www.' + website_name, headers=header)
    if response.status_code == 200:
        return 1
    else:
        return 0


# am deschis fisierul .snappy.parquet
from fastparquet import ParquetFile

parquet_file_path = 'list%20of%20company%20websites.snappy.parquet'

import pyarrow.parquet as pq
import pandas as pd

# am extras datele din fisier intr-un tabel
table = pd.read_parquet(parquet_file_path)

# pentru fiecare adresa web, am afisat adresa, daca aceasta exista, sau un mesaj in caz contrar
for i in table.index:
    website = table['domain'][i]
    print(website)

    if check(website) == 1:
        find_address(website)
    else:
        print(website + " does not exist")
