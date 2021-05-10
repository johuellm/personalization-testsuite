"""
Fill the DB with initial Data some exemplary entries
"""
import sqlite3
from random import randint, uniform
import csv
from datetime import datetime
import pandas as pd
import os
import sys

"""Establish DB connection"""
conn = sqlite3.connect('database.db')
c = conn.cursor()


def get_type(path):
    """
    Extract one of the following types from the templates:
    -e_commerce
    -search_engine
    -news_page
    :param path: path from a template
    :return: type of the given template
    """
    if path.find("e_commerce") != -1:
        template_type = 'e_commerce'
    elif path.find('search_engine') != -1:
        template_type = 'search_engine'
    elif path.find('news_page') != -1:
        template_type = 'news_page'
    else:
        template_type = None
    return template_type


"""Fill the website table with templates"""
templates = [{
    'target_group': randint(0, 10),
    'template_path': template_path,
    'type': get_type(template_path)
} for template_path in os.listdir(sys.path[1]+"\\templates")]

c.executemany("""INSERT INTO website (
                target_group, type, template_path
                ) VALUES (
                :target_group, :type, :template_path
                )""", templates)


"""
Fill the E-Commerce Website Table with data from
https://www.kaggle.com/datafiniti/electronic-products-prices
which is included in the file /data/DatafinitiElectronicsProductsPricingData.csv 
"""
with open("DatafinitiElectronicsProductsPricingData.csv", encoding="utf8") as file:
    data = csv.DictReader(file)
    data_dict = [{'name': product['name'],
                  'price': product['prices.amountMax'],
                  'condition': product['prices.condition'],
                  'currency': product['prices.currency'],
                  'merchant': product['prices.merchant'],
                  'sourceURL': product['prices.sourceURLs'],
                  'brand': product['brand'],
                  'categories': product['categories'],
                  'imgURLs': product['imageURLs'],
                  'target_group': randint(0, 10)
                  } for product in data]

c.executemany("""INSERT INTO product (
            product_name, product_price, product_condition, product_currency, product_merchant,
            product_sourceURL, product_brand, product_categories, product_imgURL ,target_group)
            VALUES (
            :name, :price, :condition, :currency, :merchant, :sourceURL, 
            :brand, :categories, :imgURLs, :target_group
            )""", data_dict)


"""exemplary user entry"""
users = [{'avg_p': uniform(45.0, 300.0),
          'avg_rp': uniform(0.0, 5.0),
          'n_rp': randint(0, 15),
          'avg_rn': uniform(0.0, 5.0),
          'n_rn': randint(0, 15),
          'avg_aa': uniform(0.0, 25),
          'avg_al': randint(120, 1000),
          'tg': randint(0, 10)} for _ in range(10)]

c.executemany("""INSERT INTO user (
            avg_price, avg_rating_product, n_rating_product, avg_rating_news,
            n_rating_news, avg_article_age, avg_article_length, target_group
            ) VALUES (
             :avg_p, :avg_rp, :n_rp, :avg_rn,
             :n_rn, :avg_aa, :avg_al, :tg
             )""", users)


"""exemplary session entry"""
sessions = [{'website_id': randint(1, 3),
             'user_id': randint(1, 10),
             'language': 'DE',
             'device': 'PC',
             'location': 'DE',
             'timestamp': datetime.now(),
             'browser_fp': randint(0, 10000000),
             'ip_address': randint(1000000000, 9999999999)
             } for _ in range(15)]

c.executemany("""INSERT INTO session (
            website_id, user_id, language, device, location,
            timestamp, browser_fp, ip_address
            ) VALUES (
            :website_id, :user_id, :language, :device, :location,
            :timestamp, :browser_fp, :ip_address
            ) """, sessions)


"""
Fill the articles table with content from the all the news dataset from Kaggle
kaggle.com/snapcrack/all-the-news?select=articles3.csv
Only using the articles3.csv
"""

with open("articles3.csv", encoding="utf8") as file:
    articles = pd.read_csv(file)
    articles_to_db = [{'article_title': row['title'],
                       'newspaper': row['publication'],
                       'author': row['author'],
                       'date': row['date'],
                       'url': row['url'],
                       'content': row['content'],
                       'target_group': randint(0, 10)
                       }for i, row in articles.iterrows()]

c.executemany("""INSERT INTO article (
            article_title, newspaper, author, date, url, content, target_group
            ) VALUES (
            :article_title, :newspaper, :author, :date, :url, :content, :target_group
            )""", articles_to_db)


conn.commit()
conn.close()

if __name__ == "__main__":
    print(get_type("base.html"))