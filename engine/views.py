from engine.utils import SSNUtils
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging
from stdnum.us import ssn
import requests
import re

MASK_NAMES = settings.MASK_NAMES
SSN_REGEX = r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$'
WORDS_REGEX = r'([A-Za-z-]|[\\u5D0-\\u05EA])+'

SSN_ASTERISKS = '***-**-****'

PATH_TO_SERVER = {
    r'.+': 'https://postman-echo.com'
}

@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):

    def __is_valid_ssn(self, num):
        if ssn.is_valid(num):
            if SSNUtils.is_dummy_ssn(num):
                return False
            formated_ssn = ssn.format(num)
            area_number = int(formated_ssn[:3])
            group_number = int(formated_ssn[4:6])
            return SSNUtils.check_area_and_group(area_number, group_number)
        return False

    def __replace_confident(self, match):
        match = match.group()
        if re.match(SSN_REGEX, match):
            if self.__is_valid_ssn(match):
                logging.debug(f'found valid ssn')
                return SSN_ASTERISKS
        if match.lower() in MASK_NAMES:
            logging.debug(f'found masked name')
            return len(match) * '*'
        return match

    def __get_server_url(self, path):
        for path_patern, serverbackend_url in PATH_TO_SERVER.items():
            if re.match(path_patern, path):
                return serverbackend_url

    def dispatch(self, request, *args, **kwargs):
        http_method = getattr(requests, request.method.lower())
        path = request.path
        server_url = self.__get_server_url(path)

        logging.debug(f'redirecting to {server_url}{path}')
        requests_response = http_method(f'{server_url}{path}', data=request.body, headers=request.headers)
        # can be done with multiprocessing if long content devided to several chunks
        content = re.sub(WORDS_REGEX, self.__replace_confident, requests_response.content.decode("utf-8"))
        return HttpResponse(
                content=content,
                status=requests_response.status_code,
                content_type=requests_response.headers['Content-Type'])


