import requests
from bs4 import BeautifulSoup


def get_news(n = None):
    domain = 'https://news.ycombinator.com/'
    path = 'newest' 
    counter = 0

    while n is None or (counter < n):
        url = domain + path
        r = requests.get(url)

        page = BeautifulSoup(r.text, "html.parser")
        articles = _extract_articles(page)

        for a in articles:
            yield a
            counter += 1
            if n and counter == n:
                break

        
        more = page.find('a', attrs={'class':'morelink'})
        if not more:
            break

        path = more.attrs['href']


def _extract_articles(page):
    table = page.findAll('table', attrs={'class':'itemlist'})

    if len(table) != 1:        
        return []

    rows =  table[0].findAll('tr')
    result = []

    for i, r in enumerate(rows): #берет значения и ключи где занчение это ряд таблицы
        link = r.find('a', attrs={'class':'storylink'})
        if not link:
            continue
        # tr with link and the next one (scores, author and comments)
        d = _get_article_data(link, rows[i+1])#если н нашел ссылку и берет ссылку и след ряд
        if d:
            result.append(d)

    return result

def _get_article_data(link, row):
    d = {}
    d['url'] = link.attrs['href']
    d['title'] = link.text

    points = row.find('span', attrs={'class':'score'})
    author = row.find('a', attrs={'class':'hnuser'})
    comments = row.findAll('a')

    d['author'] = author.text if author else None
    d['points'] = int(points.text.split()[0]) if points else None

    if comments:
        if comments[-1].text.endswith('comments'):
            d['comments'] = int(comments[-1].text.split()[0]) 
        else: 
            d['comments'] = 0
    else:
        d['comments'] = None

    return d


