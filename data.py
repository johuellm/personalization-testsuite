import sqlite3
from datetime import datetime
from ip2geotools.databases.noncommercial import DbIpCity
from user_agents import parse
from random import randint


class Data:
    """
    Class which provides functionality for all needed DB access
    """

    def __init__(self, db_path="data/database.db"):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def get_target_group(self, user):
        """
        Function to get the Target group of a given user
        :param user: id of a user
        :return: target group of this user
        """
        with self.conn:
            self.c.execute("SELECT target_group FROM user WHERE user_id =={}".format(user))
            return self.c.fetchone()[0]

    def exists_user(self, user):
        """
        Method to check if a user exists in the database
        :param user: a user id
        :return: 1, if he exists, 0 otherwise
        """
        with self.conn:
            self.c.execute("SELECT EXISTS(SELECT 1 FROM user WHERE user_id =={})".format(user))
            return self.c.fetchone()[0]

    def get_website_id(self, template):
        """
        Get the website ID for a given template
        :param: template of a website
        :return: the corresponding website id
        """
        with self.conn:
            self.c.execute("Select website_id From website Where template_path == '{}'".format(template))
            return self.c.fetchone()

    def new_user(self):
        """
        Function to create a new user entry
        :return: the user_id of the just created user
        """
        with self.conn:
            self.c.execute("""INSERT INTO user (
                    avg_price, avg_rating_product, n_rating_product, avg_rating_news,
                    n_rating_news, avg_article_age, avg_article_length, target_group
                    ) VALUES (
                     Null, Null, Null, Null,
                     Null, Null, Null, {}
                     )""".format(randint(0,10)))
            self.c.execute("Select user_id From user Order By user_id DESC")
            print("new_user")
            return self.c.fetchone()[0]

    def get_user(self, value, column):
        """
        Function to get the user based on an feature from a session
        Used in User_Recognition to get Users based on IP or Browser Fingerprint
        :param value: Feature of a user that could be observed
        :param column: Column of where the feature would be in the table
        :return: The User which could be identified
        """
        with self.conn:
            self.c.execute("Select user_id From session Where {} == '{}'".format(column, value))
            return_value = self.c.fetchone()
            return return_value[0] if return_value is not None else return_value

    def get_table(self, table):
        """
        Function to view all Entries of a given Table
        :param table: table which shall be accesed
        :return: All Elements of the given Table
        """
        with self.conn:
            self.c.execute("Select * From {}".format(table))
            return self.c.fetchall()

    def inspect_table(self, table, number_of_rows=10):
        """
        Function to view the first <number_or_rows> entries of the given table
        Usage only for development or db-changes/enhancements, no usage for the Webpages
        :param table: Table which shall be inspected
        :param number_of_rows: Number of entries which shall be viewed
        :return: Array with a given number of entries of the given table
        """
        with self.conn:
            self.c.execute("Select * From {}".format(table))
            return self.c.fetchmany(number_of_rows)

    def get_template(self, template_type):
        """
        Function to extract a template from The DB based on the wanted type and the
        target_group of the current user
        :param template_type: wanted website type
        :return: a template of the given type for a user of the given target group
        """
        with self.conn:
            self.c.execute("SELECT * FROM website WHERE type == '{}'".format(template_type))
            return self.c.fetchone()

    def get_articles(self, target_group, number_of_articles):
        """
        Function to load articles for a user
        :param target_group: target group of the user
        :param number_of_articles: number of wanted articles
        :return: Array with the wanted number of articles for the specified target group
        """
        with self.conn:
            self.c.execute("SELECT * FROM article WHERE target_group == {}".format(target_group))
            return self.c.fetchmany(number_of_articles)

    def get_products(self, target_group, number_of_products):
        """
        Function to load articles for a user
        :param target_group: target group of the user
        :param number_of_products: number of wanted products
        :return: Array with the wanted number of products for the specified target group
        """
        with self.conn:
            self.c.execute("SELECT * FROM product WHERE target_group == {}".format(target_group))
            return self.c.fetchmany(number_of_products)

    def get_search_results(self, target_group, number_of_results):
        """
        Function to load search results for a user
        :param target_group: target group of the user
        :param number_of_results: number of wanted search results
        :return: Array with the wanted number of results for the specified target group
        """
        with self.conn:
            self.c.execute("SELECT * FROM searchresults WHERE target_group == {}".format(target_group))
            return self.c.fetchmany(number_of_results)

    def insert_session(self, website_id, user_id, language=None, device=None, location=None,
                       browser_fp=None, ip_address=None):
        """
        Function to create a session entry in the
        :param website_id: id of the shown website (template)
        :param user_id:  id of the user
        :param language: language the users browser uses
        :param device: users device
        :param location: users location
        :param browser_fp: users Browser Fingerprint
        :param ip_address: users IP-Address
        :return: None, as only a DB entry gets executed
        """

        session_data = {
                'website_id': website_id,
                'user_id': user_id,
                'language': language,
                'device': device,
                'location': location,
                'timestamp': datetime.now(),
                'browser_fp': browser_fp,
                'ip_address': ip_address
             }

        with self.conn:
            self.c.execute("""INSERT INTO session (
                website_id, user_id, language, device, location, timestamp, browser_fp, ip_address
            ) VALUES (
                :website_id, :user_id, :language, :device, :location, :timestamp, :browser_fp, :ip_address
            )""", session_data)

    def create_session_entry(self, request, user, template):
        """
        Method for to assemble all necessary information to create a
        session entry in the Database. The entry function is called in this
        function.
        :param request: object that contains the view arguments (e.g user-agent or IP)
        :param user: the current user
        :param template: the name of the template that is used in this session
        :return: None
        """
        print("Creating Session Entry")
        ua = request.headers.get('User-Agent')
        ip = request.remote_addr
        language = request.accept_languages[0][0]
        fingerprint = hash(ua + ip + language)
        """TODO: flask may be able to parse the user agent as well """
        device = parse(ua).device.family
        try:
            location = DbIpCity.get(ip, api_key='free').country
        except KeyError:
            location = None
        except:
            location = None
        website_id = self.get_website_id(template)[0]
        self.insert_session(
            website_id=website_id, user_id=user, language=None, device=device, location=location,
            browser_fp=fingerprint, ip_address=ip
        )


if __name__ == "__main__":
    Data().insert_session(2, 3)
    #print(Data().new_user())
    print(Data().inspect_table('user', number_of_rows=15))
    print(Data().get_target_group(11))
