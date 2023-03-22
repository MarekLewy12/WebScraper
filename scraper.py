import string
from bs4 import BeautifulSoup
import requests
import os

links_list = []

punctuations = [x for x in string.punctuation]
number_of_pages = int(input("How many pages"))
type_of_article = input("Type of article")
url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'

for page in range(1, number_of_pages + 1):
    new_url = url + f'&page={page}'
    request = requests.get(new_url)
    parse = BeautifulSoup(request.content, 'html.parser')
    article_type = parse.find_all('span', {'class': 'c-meta__type'},
                                  text=f'{type_of_article}')
    for x in article_type:
        links = x.find_parent('article').find('a').get('href')
        links_list.append(links)

    if not links_list:
        os.mkdir(f'Page_{page}') if not os.path.isdir(f'Page_{page}') else None

    else:
        for link in links_list:
            new_url = 'https://www.nature.com' + link
            new_request = requests.get(new_url)
            new_parse = BeautifulSoup(new_request.content, 'html.parser')

            titles = new_parse.find('h1',
                                    {'class': "c-article-magazine-title"}).text.strip()
            
            article_titles = [a for a in titles if a not in punctuations]
            file_names = ("".join(article_titles)).replace(' ', '_') + '.txt'
            
            content = new_parse.find('p', {"class": "article__teaser"}).text.strip()
            os.mkdir(f'Page_{page}') if not os.path.isdir(f'Page_{page}') else None
            
            file = open(f'Page_{page}\{file_names}', 'w', encoding='utf-8')
            file.write(content)
            file.close()
