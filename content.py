"""
Class for specifying which content is used for the instance of  a
webpage and loading it from the Database

"""
from data import Data
from flask import make_response, render_template
from random import choice, randint


class PageContent:

    @staticmethod
    def extract_parameters(parameter):
        """
        Method for extraction parameters out of the url
        :param parameter: Parameters concatenated as a string
        :return: The parameters as a dictionary
        """
        try:
            parameter_dictionary = {}
            combinations = parameter.split("&")
            for combination in combinations:
                key, value = combination.split("=")
                parameter_dictionary[key] = value
            return parameter_dictionary
        except Exception as e:
            # print(e)
            return {}

    @staticmethod
    def choose_batchsize():
        return 4

    @staticmethod
    def choose_templates(param_dict, target_group, wtype):
        """
        Function to provide the right combination of base,type-specific template
        and number of columns, based on the parameters
        :param param_dict: dict with all given parameters
        :param target_group: target group of the current user
        :param wtype: type of the website (e-commerce, news-page or search-engine)
        """

        # Try getting the relevant parameters
        try:
            cols = int(param_dict["cols"])
            print(f"cols: {cols}")
        except Exception as e:
            cols = 4
        try:
            struct = param_dict["struct"]
        except Exception as e:
            struct = None

        # differentiation based on type
        if wtype == "e-commerce":
            if struct == "p":
                # personalized combination
                # chose base template
                if 2 < target_group < 7:
                    ecomm_base = "base_footer_general.html"
                else:
                    ecomm_base = "base_footer_products.html"
                # chose e-commerce template
                if target_group % 2 == 0:
                    ecomm_template = "e_commerce_card_group.html"
                else:
                    ecomm_template = "e_commerce_card_group_horizontal.html"
                    cols = 2
                return ecomm_base, ecomm_template, cols

            elif struct == "d":
                # dynamic case with random combinations
                templates = ["e_commerce_card_group.html", "e_commerce_card_group_horizontal.html"]
                base_templates = ["base_footer_products.html", "base_footer_general.html", "base.html"]
                return choice(base_templates), choice(templates), cols
            else:
                # static case is the default case
                return "base_footer_products.html", "e_commerce_card_group.html", cols

        elif wtype == "search-engine":
            pass
        elif wtype == "news-page":
            pass
        else:
            return "base_footer_general.html", "home.html", 0

    @staticmethod
    def choose_color_theme(param_dict, target_group):
        """
        Function to choose the color theme based on
        :param param_dict: the dictionary with all given parameters
        :param target_group: target group of the current user
        """
        try:
            color_parameter = param_dict["color"]
        except Exception as e:
            return "dark", "white"

        if color_parameter == "dark":
            return "dark", "white"
        elif color_parameter == "light":
            return "light", "black"
        elif color_parameter == "time":
            pass
        elif color_parameter == "p":
            if target_group <= 4:
                return "dark", "white"
            else:
                return "light", "black"
        elif color_parameter == "d":
            return choice([("dark", "white"), ("light", "black")])
        else:
            return "dark", "white"

    @staticmethod
    def choose_header():
        tg = randint(0, 10)
        product = Data().get_products(tg, 50)[randint(0, 49)]
        url = product[6]
        title = product[1]
        header = choice([True, False])
        return header, url, title

    @staticmethod
    def concrete_user(param_dict, session_user):
        """
        Function to set the user manually if specified in the url parameters
        If not the user is the session user
        :param param_dict: the dictionary with all given parameter key/value pairs
        :param session_user: the user, which was identified by user recognition and saved in the session storage
        :return: the user for which personalization takes place
        """
        try:
            if Data().exists_user(int(param_dict["user"])) == 1:
                user = str(param_dict["user"])
            else:
                user = session_user
        except KeyError:
            user = session_user
        except AttributeError:
            user = session_user
        return user

    def generate_e_commerce_content(self, parameter, request, user):
        """
        Method to generate the response object which includes everything shown to the user
        :param parameter: the parameters as a string (extracted from url)
        :param request: object that contains view arguments (e.g cookies, paths, ...)
        :param user: the current user (user_id)
        """
        # Get individual parameters and the user
        param_dict = self.extract_parameters(parameter)
        user = int(self.concrete_user(param_dict, user))
        target_group = Data().get_target_group(user)

        # Decide on structure/display
        base, template, batchsize = self.choose_templates(param_dict, target_group, "e-commerce")
        header, header_url, header_object = self.choose_header()
        bg_color, text_color = self.choose_color_theme(param_dict, target_group)
        print(f"batchsize: {batchsize}")

        # decide on content
        products = Data().get_products(2, batchsize*8)

        # save the users session
        Data().create_session_entry(request, user, template)

        # generate the response based on the chosen content and structure elements
        response = make_response(render_template(template, products=products, base=base,
                                                 batchsize=batchsize, bg_color=bg_color,
                                                 text_color=text_color, header=header,
                                                 header_url=header_url, header_object=header_object))
        return response  # user


if __name__ == "__main__":
    page = PageContent()
