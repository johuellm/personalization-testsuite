"""
script to create all necessary database tables
"""
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

"""Create the Sessions Table"""
c.execute("""CREATE TABLE session (
            session_id INTEGER PRIMARY KEY ASC,
            website_id integer NOT NULL,
            user_id integer NOT NULL,
            language text,
            device text,
            location text,
            timestamp text,
            browser_fp text,
            ip_address text,
            FOREIGN KEY (user_id) REFERENCES user (user_id),
            FOREIGN KEY (website_id) REFERENCES website (website_id)
            )""")


"""
Create the User Table
n ~ number
avg ~ average
"""
c.execute(""" CREATE TABLE user (
            user_id integer PRIMARY KEY,
            avg_price real,
            avg_rating_product real,
            n_rating_product integer,
            avg_rating_news real,
            n_rating_news integer,
            avg_article_age real,
            avg_article_length real,
            target_group integer
            )""")


"""
Create Table website
"""
c.execute("""CREATE TABLE website (
            website_id integer PRIMARY KEY ASC,
            target_group integer,
            type text,
            template_path text
            )""")


"""
Create the E-Commerce data Table
"""
c.execute("""CREATE TABLE product (
            product_id integer PRIMARY KEY ASC ,
            product_name text,
            product_price real,
            product_condition text,
            product_currency text,
            product_merchant text,
            product_sourceURL text, 
            product_brand text,
            product_categories text,
            product_imgURL text,
            target_group integer
            )""")

"""
Create the Search Engine data Table
"""
c.execute("""CREATE TABLE searchresult (
            result_id integer PRIMARY KEY ASC,
            title text,
            url text,
            date text,
            preview text
            )""")

"""
Create the News data Table
"""
c.execute("""CREATE TABLE article (
            article_id integer PRIMARY KEY ASC,
            article_title text,
            newspaper text,
            author text,
            date text,
            url text,
            content text,
            target_group           
            )""")

"""
FURTHER POSSIBLE TABLES
"""
"""Create the Header Table"""
"""Create the Footer Table"""
"""Create the Site-bar Table"""
"""Create the Pop-up Table"""
"""Create the TAG-Relation Table"""


conn.commit()
conn.close()
