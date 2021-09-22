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
        :param parameter: URl parameter hat were included in the request url
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

        # extracting Paramters
        mapping = {
            't': True,
            'f': False
        }
        param_dict = PageContent().extract_parameters(parameter)
        rec_by_cookie = mapping[param_dict['cookie']] if 'cookie' in param_dict else True
        rec_by_fingerprint = mapping[param_dict['bfp']] if 'bfp' in param_dict else False
        rec_by_ip = mapping[param_dict['ip']] if 'ip' in param_dict else False
        if 'newuser' in param_dict:
            rec_by_cookie = False
            rec_by_fingerprint = False
            rec_by_ip = False

        print(f"recognition mode: {rec_by_cookie, rec_by_fingerprint, rec_by_ip}")

        # Case 1: User has a cookie referencing a user in DB
        if rec_by_cookie and cookie:
            print("User Recognized by Cookie")
            return int(cookie)

        # Case 2: Users Browser Fingerprint matches a fingerprint in the DB
        fp_user = Data().get_user(fingerprint, "browser_fp")
        if rec_by_fingerprint and fp_user is not None:
            print(f"Browser Fingerprint Elements: {ua + ip + language}")
            print("User Recognized by Browser Fingerprint")
            return fp_user

        # Case 3: User can be recognized by his IP
        if rec_by_ip:
            ip_user = Data().get_user(ip, "ip_address")
            if ip_user is not None:
                print("User Recognized by IP")
                return ip_user

        # Case 4: New User
        if 'ntg' in param_dict:
            target_group = randint(0, param_dict['ntg'])
            print("Specified User")
        else:
            target_group = randint(0, 10)
        new_user = Data().new_user(target_group)
        print("New User")
        return new_user
