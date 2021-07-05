"""
Class for User Recognition
"""
from data import Data
from random import randint
from content import PageContent


class UserRecognition:

    @staticmethod
    def recognize(request, parameter):
        """
        Function to recognize the user, if he could not already be recognized by the session
        :param request: object that contains view arguments (e.g cookies, paths, ...)
        :return: the identified user (user_id) or the id of a newly created user, if
                 the user could not be identified
        """
        print("User Recognition activated")
        # Get User Attributes and make fingerprint and response
        # For more FP_attr:  https://tedboy.github.io/flask/generated/generated/flask.Request.html
        ua = request.headers.get('User-Agent')
        ip = request.remote_addr
        language = request.accept_languages[0][0]
        cookie = request.cookies.get('user')
        fingerprint = hash(ua + ip + language)

        # Case 1: User has a cookie referencing a user in DB
        print("case 1")
        if cookie:
            return int(cookie)

        # Case 2: Users Browser Fingerprint matches a fingerprint in the DB
        print("case 2")
        fp_user = Data().get_user(fingerprint, "browser_fp")
        print(f"Browser Fingerprint Elements: {ua + ip + language}")
        if fp_user is not None:
            return fp_user

        # Case 3: User can be recognized by his IP
        use_ip = False
        if use_ip:
            print("case 3")
            ip_user = Data().get_user(ip, "ip_address")
            if ip_user is not None:
                return ip_user

        # Case 4: New User
        print("case 4")
        param_dict = PageContent().extract_parameters(parameter)
        if 'ntg' in param_dict:
            target_group = randint(0, param_dict['ntg'])
        else:
            target_group = randint(0, 10)
        new_user = Data().new_user(target_group)
        return new_user
