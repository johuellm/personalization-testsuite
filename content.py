"""
Class for specifying which content is used for the instance of  a
webpage and loading it from the Database

"""


class PageContent:

    def __init__(self, parameters):
        self.param_string = parameters

    def extract_parameters(self):
        pass

    def choose_template(self):
        pass


if __name__ == "__main__":
    page = PageContent()
