import json
import requests

class News:
    def __init__(self):
        url = 'http://newsapi.org/v2/top-headlines?country=us&apiKey=cb274b2472d549ddac751a33113363f5'
        response = requests.get(url)
        self.articles = response.json()['articles']

    def get_polished_articles(self):
        '''
        OUTPUT: Return list of dictionaries that contain
        Keys:
            author: author
            title: title
            content: content of the news article
        '''
        polished_articles = []

        for article in self.articles:
            author = article['author']
            title = article['title']
            content = article['content']
            if content is not None:
                content = content.split('…')[0]+'... '
                if '\n' in content:
                    content = (' '.join(content.split('\n'))).replace('\r','')
            polished_article = {'author':author,
             'title':title,
             'content':content,
            }

            polished_articles.append(polished_article)

        return polished_articles

# Created By: Yu Chen + Younghoon Kim (AKA Brian Kim)