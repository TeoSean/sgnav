import requests
from bs4 import BeautifulSoup
import pickle, json
from tqdm import tqdm

def scrape(link):
    session = requests.session()
    mp = session.get(link)

    soup = BeautifulSoup(mp.content, 'html.parser')
    as_ = soup.find_all('a')
    lynks = []
    for a in as_:
        if a['href'].startswith('https://moovitapp.com/index/en-gb/public_transportation-line'):
            lynks.append(a['href'])

    routes = {}


    for i in tqdm(range(len(lynks)), desc = 'Scraping...'):
        link = lynks[i]
        try:
            np = session.get(link)
            soup = BeautifulSoup(np.content, 'html.parser')
            route = []
            for i in soup.find_all('h3'):
                route.append(i.text)

            op = route[0]
            
            
            route = route[1:-1]
            route
            head = soup.find('h2', class_='content-header qna-header')
            head = head.text
            head=head.split(' ')[0]

            routes[head] = route
        except:
            continue
    return routes


routes = scrape('https://moovitapp.com/index/en-gb/public_transportation-lines-Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1-1678-775180')
routes.update(scrape('https://moovitapp.com/index/en-gb/public_transportation-lines-Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1-1678-775181'))
routes.update(scrape('https://moovitapp.com/index/en-gb/public_transportation-lines-Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1-1678-873544'))
routes.update(scrape('https://moovitapp.com/index/en-gb/public_transportation-lines-Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1-1678-904138'))

with open('routedata.json', 'wb') as file:
    file.write(json.dumps(routes, indent=4))


print(routes)