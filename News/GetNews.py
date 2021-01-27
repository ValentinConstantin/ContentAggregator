import requests
from bs4 import BeautifulSoup
from django.db import models

SITES = {
    "sport": ["https://www.digi24.ro/sport/", "https://www.sport.ro/liga-1"],
    "economie": ["https://www.digi24.ro/stiri/economie/digi-economic", "https://www.profit.ro/stiri/economie/"],
    "politica": [],
    "externe": [],

}

def get_economy_news(category, sites, news_model: models) -> list:
    links = []
    for site in sites[category]:
        r = requests.get(site)
        soup = BeautifulSoup(r.content, 'html5lib')
        if "digi24" in site:
            for a in soup.find_all('a', href=True):
                if (
                    "/stiri/" in a['href']
                    and len(a['href']) > 40
                    and "https://" not in a['href']
                ):
                    url = "https://www.digi24.ro" + a["href"]
                    if (
                            not news_model.objects.filter(url=url).exists()
                            and url not in links
                    ):
                        if len(links) == 3:
                            break
                        links.append(url)
        if "profit.ro" in site:
            for a in soup.find_all('a', href=True):
                if (
                        "/stiri/" in a['href']
                        and len(a['href']) > 40
                        and "https://" not in a['href']
                        and "http://" not in a['href']
                ):
                    url ='https://www.profit.ro' + a['href']
                    if (
                            not news_model.objects.filter(url=url).exists()
                            and url not in links
                    ):
                        if len(links) == 6:
                            break
                        links.append(url)
    return links



def get_sport_news(category, sites, news_model: models) -> list:
    links = []
    for site in sites[category]:
        if category == "sport":
            if "digi24" in site:
                r = requests.get(site)
                soup = BeautifulSoup(r.content, 'html5lib')
                for a in soup.find_all('a', href=True):
                    if "sport" in a["href"] and len(a["href"].split("/")) >= 5 and "https" not in a["href"]:
                        url = "https://www.digi24.ro" + a["href"]
                        if (
                                not news_model.objects.filter(url=url).exists()
                                and url not in links
                        ):
                            if len(links) == 3:
                                break
                            links.append(url)
            elif "sport.ro" in site:
                r = requests.get(site)
                soup = BeautifulSoup(r.content, 'html5lib')
                for a in soup.find_all('a', href=True):
                    if site in a['href'] and len(a["href"].split("/")) >= 5:
                        url = a['href']
                        if (
                                not news_model.objects.filter(url=url).exists()
                                and not url in links
                        ):
                            if len(links) == 6:
                                break
                            links.append(url)

            # elif "gsp" in site:
            #     r = requests.get(site)
            #     soup = BeautifulSoup(r.content, 'html5lib')
            #     for a in soup.find_all('a', href=True):
            #         if "/fotbal/liga-1/" in a["href"]:
            #             url = "https://www.gsp.ro" + a["href"]
            #             if (
            #                     not news_model.objects.filter(url=url).exists()
            #                     and url not in links
            #             ):
            #                 if len(links) == 6:
            #                     break
            #                 links.append(url)
    return links


def get_content_from_links(category, sites, news_model: models):
    site_data = []
    if category == "sport":
        links = get_sport_news(category, sites, news_model)
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            if "digi24" in link:
                Avatar = soup.findAll("figure", {"class": "article-thumb"})
                DATA = {"Avatar": "",
                        "Title": soup.find('title').string,
                        "Content": "",
                        "Category": link.split("/")[4].capitalize(),
                        "URL": link}

                for row in Avatar:
                    DATA["Avatar"] = row.img['src']
                    break

                for index, x in enumerate(soup.find_all("p"), start=1):
                    if index < len(soup.find_all("p")):
                        DATA['Content'] += x.get_text() + "\n"

                response = requests.get(DATA["Avatar"])
                with open("News/static/img/" + DATA["Avatar"][-20:] + ".png", "wb") as file:
                    file.write(response.content)
                site_data.append(DATA)
            elif "sport.ro" in link:
                print(link)
                DATA = {"Avatar":"",
                        "Title": soup.find('title').string,
                        "Content": "",
                        "Category": "Sport",
                        "URL": link}
                try:
                    DATA["Avatar"] = soup.find('div', {"class": "relative big-image"}).img['data-src']
                except Exception:
                    DATA["Avatar"] = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"

                content_p = soup.find('div', {'class': 'article-content'})
                p_rows = content_p.find_all('p')

                index_p = 0
                for x in p_rows:
                    if index_p == len(p_rows) - 2:
                        break
                    DATA['Content'] += x.get_text()
                    index_p += 1

                response = requests.get(DATA["Avatar"])
                with open("News/static/img/" + DATA["Avatar"][-20:] + ".png", "wb") as file:
                    file.write(response.content)
                site_data.append(DATA)
            # elif "gsp" in link:
            #     DATA = {"Avatar": "",
            #             "Title": soup.find('title').string,
            #             "Content": "",
            #             "Category": 'Sport',
            #             "URL": link
            #             }
            #
            #     # ! Get avatar
            #     for img in soup.findAll('img'):
            #         if (
            #                 img is not None
            #                 and img.get('src')
            #                 and "https://cacheimg.gsp.ro" in img['src']
            #         ):
            #             DATA['Avatar'] = img.get('src')
            #             break
            #         else:
            #             DATA['Avatar'] = 'no_img'
            #     # ! Get content
            #     divs = soup.findAll('div', attrs={"class": "article-body"})
            #     for x in divs:
            #         DATA['Content'] = x.find('p').text
            #         break
            #
            #     response = requests.get(DATA["Avatar"])
            #     with open("News/static/img/" + DATA["Avatar"][-20:] + ".png", "wb") as file:
            #         file.write(response.content)
            #     site_data.append(DATA)
    if category == "economie":
        links = get_economy_news(category, sites, news_model)
        for link in links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html5lib')
            if "digi24" in link:
                Avatar = soup.findAll("figure", {"class": "article-thumb"})
                DATA = {"Avatar": "",
                        "Title": soup.find('title').string,
                        "Content": "",
                        "Category": "Economie",
                        "URL": link}

                for row in Avatar:
                    DATA["Avatar"] = row.img['src']
                    break

                for index, x in enumerate(soup.find_all("p"), start=1):
                    if index < len(soup.find_all("p")):
                        DATA['Content'] += x.get_text() + "\n"

                response = requests.get(DATA["Avatar"])
                with open("News/static/img/" + DATA["Avatar"][-20:] + ".png", "wb") as file:
                    file.write(response.content)
                site_data.append(DATA)
            elif "profit.ro" in link:
                DATA = {"Avatar": "https:" + soup.find('div', {"class": "art-img"}).img['src'],
                        "Title": soup.find('div', {"class": "article"}).h1.text,
                        "Content": "",
                        "Category": "Sport",
                        "URL": link}

                content_p = soup.find('div', {'class': 'article-content'})
                p_rows = content_p.find_all('p')

                index_p = 0
                for x in p_rows:
                    if index_p == len(p_rows) - 2:
                        break
                    DATA['Content'] += x.get_text()
                    index_p += 1
                response = requests.get(DATA["Avatar"])
                with open("News/static/img/" + DATA["Avatar"][-16:-13] + ".png", "wb") as file:
                    file.write(response.content)
                    DATA["Avatar"]= DATA["Avatar"][-16:-13]
                site_data.append(DATA)
    return site_data
