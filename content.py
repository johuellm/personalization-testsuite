"""
Class for specifying which content is used for the instance of  a
webpage and loading it from the Database
Todo:-location
Todo:-header parameter and footer in base.html?
"""
from data import Data
from flask import make_response, render_template
from random import choice, randint, shuffle, gauss, sample
from datetime import datetime, timedelta
from warnings import warn
from ip2geotools.databases.noncommercial import DbIpCity
from ip2geotools import errors


class PageContent:

    @staticmethod
    def extract_parameters(parameter):
        """
        Method for extraction parameters out of the url
        :param parameter: Parameters concatenated as a string
        :return: The parameters as a dictionary
        """
        if parameter is None:
            return {}
        else:
            try:
                parameter_dictionary = {}
                combinations = parameter.split("&")
                for combination in combinations:
                    key, value = combination.split("=")
                    parameter_dictionary[key] = value
                return parameter_dictionary
            except Exception as e:
                raise Exception(f"Parameter Extraction Failed: it should have the"
                                f" structure 'key=value&key=value&...' ({e})")

    @staticmethod
    def choose_templates(param_dict, target_group, wtype, default):
        """
        Function to provide the right combination of base,type-specific template
        and number of columns, based on the parameters
        :param param_dict: dict with all given parameters
        :param target_group: target group of the current user
        :param default: default parameter to use if the parameter is not specified in the param_dict
        :param wtype: type of the website (e-commerce, news-page or search-engine)
        """

        # Try getting the relevant parameters
        # Parameter for the number of columns used in template
        if "cols" in param_dict:
            cols = param_dict["cols"]
        else:
            cols = default

        # setting the cols value
        if cols == "s":
            cols = 2
        elif cols == "d":
            cols = randint(1, 5)
        elif cols == "p":
            if target_group % 2 == 0:
                cols = 2
            else:
                cols = 4
        else:
            try:
                cols = int(cols)
            except Exception as e:
                raise Exception(f"cols value needs to be s,d,p or and integer value! ({e})")

        # general parameter for the structure of the webpage
        if "struct" in param_dict:
            struct = param_dict["struct"]
        else:
            struct = default

        # differentiation based on website type
        if wtype == "e-commerce":
            if struct == "p":
                # personalized combination
                # chose base template
                ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
                if ntg * 0.25 < target_group < ntg * 0.75:
                    ecomm_base = "base_footer_general.html"
                else:
                    ecomm_base = "base_footer_products.html"
                # chose e-commerce template
                if target_group % 2 == 0:
                    ecomm_template = "e_commerce_card_group.html"
                else:
                    ecomm_template = "e_commerce_card_group_horizontal.html"
                return ecomm_base, ecomm_template, cols

            elif struct == "d":
                # dynamic case with random combinations
                templates = ["e_commerce_card_group.html", "e_commerce_card_group_horizontal.html"]
                base_templates = ["base_footer_products.html", "base_footer_general.html", "base.html"]
                return choice(base_templates), choice(templates), cols

            elif struct == "s":
                # static case is the default case
                return "base_footer_products.html", "e_commerce_card_group.html", cols
            else:
                raise Exception("Invalid Struct parameter: Should be 'p','d' or 's'")

        elif wtype == "search-engine":
            pass
        elif wtype == "news-page":
            pass
        else:
            raise Exception("invalid wtype in choose_templates")

    @staticmethod
    def choose_color_theme(param_dict, target_group, default):
        """
        Function to choose the color theme based on
        :param param_dict: the dictionary with all given parameters
        :param default: default parameter to use if the parameter is not specified in the param_dict
        :param target_group: target group of the current user
        :return: a tuple with the background color theme and the text color
        """
        if "color" in param_dict:
            color_parameter = param_dict["color"]
        else:
            color_parameter = default

        if color_parameter == "dark":
            return "dark", "white"
        elif color_parameter == "light":
            return "light", "black"
        elif color_parameter == "time":
            if 5 < int(datetime.now().strftime("%H")) < 22:
                return "light", "black"
            else:
                return "dark", "white"
        elif color_parameter == "p":
            ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
            if target_group <= ntg * 0.5:
                return "dark", "white"
            else:
                return "light", "black"
        elif color_parameter == "d":
            return choice([("dark", "white"), ("light", "black")])
        elif color_parameter == "s":
            return "dark", "white"
        else:
            raise Exception("invalid color parameter: should be 'dark', 'white', 'time', 'p', 'd' or 's'")

    @staticmethod
    def choose_header(param_dict, target_group, wtype, default):
        """
        Function to choose if and what to display in the header
        :param param_dict: Dict with all given parameters
        :param target_group: Target Group of the current user
        :param wtype: the wanted website type
        :param default: default parameter to use if the parameter is not specified in the param_dict
        :return:    1. True/False depending on if the header should be displayed or not
                    2. a url where the header should reference to
                    3. the text that will be displayed in the header
        """

        if "header" in param_dict:
            header_parameter = param_dict["header"]
        else:
            header_parameter = default

        if wtype == "e-commerce":
            if header_parameter == "f":
                return False, None, None

            elif header_parameter == "s":
                product = Data().get_products(0, 1)[0]
                return True, product[6], "Sale: " + product[1]

            elif header_parameter == "d":
                tg = randint(0, 10)
                product = Data().get_products(tg, 50)[randint(0, 49)]
                header = choice([True, False])
                return header, product[6], "Sale: " + product[1]

            elif header_parameter == "p":
                ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
                product = Data().get_products(round((target_group/ntg)*10), 1)[0]
                return True, product[6], "Sale: " + product[1]
            else:
                return True, None, header_parameter.replace("-", " ")
        elif wtype == "search-engine":
            pass
        elif wtype == "news-page":
            pass
        else:
            raise Exception("invalid wtype in choose_header()")

    @staticmethod
    def concrete_user(param_dict, user):
        """
        Function to set the user manually if specified in the url parameters
        If not the user is the session user
        :param param_dict: the dictionary with all given parameter key/value pairs
        :param user: the user, which was identified by user recognition and saved in the session storage
        :return: the user for which personalization takes place
        """
        if "user" in param_dict:
            if Data().exists_user(int(param_dict["user"])) == 1:
                user = str(param_dict["user"])
            else:
                warn(f'User {param_dict["user"]} does not exists. Using user {user} instead')

        if "tg" in param_dict:
            target_group = int(param_dict["tg"])
            ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
            if ntg < target_group:
                raise Exception("Target Group is too big")
        else:
            target_group = Data().get_target_group(int(user))

        return user, int(target_group)

    @staticmethod
    def get_content(param_dict, target_group, batchsize, wtype, default):
        """
        Method to get the content from the DB
        :param param_dict: dict with all given parameters
        :param target_group: target group of the current user
        :param batchsize: number of elements in one row (= number of columns (cols))
        :param wtype: type of the website (e-commerce, news-page or search-engine)
        :param default: default parameter to use if the parameter is not specified in the param_dict
        :return: a set of products
        """

        # get the parameter
        if "content" in param_dict:
            content_param = param_dict["content"]
        else:
            content_param = default

        # get data based on website type
        if wtype == "e-commerce":
            if content_param == "p":
                ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
                products = Data().get_products(round((target_group/ntg)*10), 8 * batchsize)
            elif content_param == "d":
                products = Data().get_products(randint(0, 10), 8 * batchsize)
                shuffle(products)
            elif content_param == "s":
                products = Data().get_products(0, 8 * batchsize)
            elif content_param == "o":
                products = Data().get_products(0, 8 * batchsize)
            else:
                raise Exception(f"Invalid content parameter: should be 's', 'p', 'd' or 'o'")
            return products

        elif wtype == "search-engine":
            pass
        elif wtype == "news-page":
            pass
        else:
            raise Exception("wrong website type (wtype) in the method get_content()")

    @staticmethod
    def modify_entity_attributes(products, param_dict, target_group, wtype, default):
        """
        Method to modify the attributes of the given entities( products for ecommerce for example)
        :param products: the given set of products loaded from the db
        :param param_dict: dict with all given parameters
        :param target_group: target group of the current user
        :param wtype: type of the website (e-commerce, news-page or search-engine)
        :param default: default parameter to use if the parameter is not specified in the param_dict
        :return: an array with dictionaries with product information
        """
        if "price" in param_dict:
            price_param = param_dict["price"]
        else:
            price_param = default

        if "tags" in param_dict:
            tags_param = param_dict["tags"]
        else:
            tags_param = default

        if wtype == "e-commerce":
            if price_param == "p":
                ntg = 10 if "ntg" not in param_dict else int(param_dict["ntg"])
                if target_group <= ntg * 0.25:
                    price_multiplier = 0.75
                elif 2 < target_group <= ntg * 0.5:
                    price_multiplier = 0.95
                elif 5 < target_group <= ntg * 0.75:
                    price_multiplier = 1.05
                elif target_group > ntg * 0.75:
                    price_multiplier = 1.25
            elif price_param == "d":
                price_multiplier = gauss(1, 0.2)
            elif price_param == "s":
                price_multiplier = 1
            else:
                raise Exception("Invalid price parameter in modify_entity_attributes()")

            if tags_param == "p":
                tag_extraction = lambda tags: [tag + " | " for tag in tags[:4]]\
                    if target_group <= ntg * 0.5 else [tag + " | " for tag in tags[-4:]]
            elif tags_param == "d":
                tag_extraction = lambda tags: [tag + " | " for tag in sample(tags, 4)]
            elif tags_param == "s":
                tag_extraction = lambda tags: [tag + " | " for tag in tags[0:4]]
            else:
                raise Exception("Invalid Tags Parameter in modify_entity_attributes()")

            products_array = []
            for product in products:
                product_dict = {"title": product[1],
                                "img_url": product[-2].split(",")[0],
                                "img_alt_url": product[-2].split(",")[-1],
                                "retailer": product[5],
                                "retailer_url": product[6],
                                "price": str(round(product[2] * price_multiplier, 2)) + " " + product[4],
                                "tags": "".join(tag_extraction(product[8].split(",")))
                                }
                products_array.append(product_dict)
            return products_array

        elif wtype == "search-engine":
            pass
        elif wtype == "news-page":
            pass
        else:
            raise Exception("wrong website type (wtype) in the method modify_entity_attributes")

    @staticmethod
    def choose_location(param_dict, ip, default):
        """
        function to get the location and decide on displaying it based on the given parameters
        :param param_dict: Dictionary with all given parameters
        :param ip: the ip address of the current user
        :param default: default value for the location
        :return: location based on parameters (default = "International")
        """

        if "location" in param_dict:
            location_parameter = param_dict["location"]
        else:
            location_parameter = default

        try:
            ip_location = DbIpCity.get(ip, api_key='free').country
        except errors.InvalidRequestError:
            ip_location = "International"
        except KeyError:
            ip_location = "International"

        if location_parameter == "p":
            location = ip_location
        elif location_parameter == "d":
            location = choice([ip_location, "International"])
        elif location_parameter == "s":
            location = "international"
        else:
            location = location_parameter
        return location

    @staticmethod
    def get_default(param_dict):
        """
        Method to set the default value to s,d or p
        :param param_dict: Dictionary with all given parameters
        :return: s,d,p depending on the input (no input = s (default))
        """
        if "default" in param_dict:
            return param_dict["default"]
        else:
            return "s"

    def generate_content(self, parameter, request, user, wtype):
        """
        Method to generate the response object which includes everything shown to the user
        :param parameter: the parameters as a string (extracted from url)
        :param request: object that contains view arguments (e.g cookies, paths, ...)
        :param user: the current user (user_id)
        :param wtype: the type of the website that should be displayed (e-commerce/search-engine/news-page)
        :return: a response object with all necessary information to display the webpage based on the parameters
        """
        # Get individual parameters, default and the user
        param_dict = self.extract_parameters(parameter)
        default = self.get_default(param_dict)
        user, target_group = self.concrete_user(param_dict, user)

        # Decide on structure/display
        base, template, batchsize = self.choose_templates(param_dict, target_group, wtype, default)
        header, header_url, header_object = self.choose_header(param_dict, target_group, wtype, default)
        bg_color, text_color = self.choose_color_theme(param_dict, target_group, default)
        location = self.choose_location(param_dict, request.remote_addr, default)

        # decide on content
        # products = Data().get_products(target_group, batchsize*8)
        products = self.get_content(param_dict, target_group, batchsize, wtype, default)
        products = self.modify_entity_attributes(products, param_dict, target_group, wtype, default)

        # save the users session
        Data().create_session_entry(request, user, template)

        # generate the response based on the chosen content and structure elements
        response = make_response(render_template(template, products=products, base=base,
                                                 batchsize=batchsize, bg_color=bg_color,
                                                 text_color=text_color, header=header,
                                                 header_url=header_url, header_object=header_object,
                                                 location=location))
        response.set_cookie("user", user, expires=datetime.now() + timedelta(minutes=90))
        return response


if __name__ == "__main__":
    page = PageContent()
