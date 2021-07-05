import base64


class AnalysisFunctions:
    """
    Class for Analysis Functions that are used in the test scripts
    (used in demo_test1 and demo_test2)
    """

    @staticmethod
    def source_hashcomparison(sources):
        """
        creation of A List of Hash values for each HTML Sourcecode
        and calculate the percentage of matching hash values
        :param sources: Array with the html code of a website stored as one big string
        :return: the ratio of combinations where the hash values are identical to all combinations of hashvalues
        """
        hashvalues = []
        """calculate Hashvalues"""
        for source in sources:
            hashvalues.append(hash(source))

        """count matching hashvalues"""
        count = 0
        for value in hashvalues:
            for i in range(0, len(hashvalues)):
                if value == hashvalues[i]:
                    count += 1

        """calculate percentage of matching hashvalues"""
        count -= len(hashvalues)
        similarityratio = count / ((len(hashvalues)**2)-len(hashvalues))
        return similarityratio

    @staticmethod
    def image_hashcomparison(imagepaths):
        """

        :return:the ratio of combinations where the hash values are identical to all combinations of hashvalues
        """

        """calculate hashvalues"""
        hashvalues = []
        for i in range(0, len(imagepaths)):
            with open(imagepaths[i], "rb") as image:
                image_encoding = base64.b64encode(image.read())
                value = hash(image_encoding)
            hashvalues.append(value)

        """Calculate a similarityratio of how many hashvalues are similar"""
        count = 0
        for value in hashvalues:
            for i in range(0, len(hashvalues)):
                if value == hashvalues[i]:
                    count += 1

        """calculate percentage of matching hashvalues"""
        count -= len(hashvalues)
        similarityratio = count / ((len(hashvalues) ** 2) - len(hashvalues))
        return similarityratio