import sqlite3
from datetime import datetime


class Data:
    """
    Class which provides functionality for all needed DB access
    """

    def __init__(self, db_path="data/database.db"):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

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

    def get_template(self, template_type, target_group):
        """
        Function to extract a template from The DB based on the wanted type and the
        target_group of the current user
        :param template_type: wanted website type
        :param target_group:  wanted target group
        :return: a template of the given type for a user of the given target group
        TODO: -add target Group
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


if __name__ == "__main__":
    Data().insert_session(2, 3)
    print(Data().inspect_table('session', number_of_rows=20))
    print(Data().get_products(target_group=10, number_of_products=20))
