from .status_codes import *


class ApplicationError(Exception):
    """
    A custom exception class which will contain the message and the status code
    and will be used whenever an operation failed and the response is not 200 or something similar
    It is depended on the dictionary with the status codes at status_codes.py

    Raises:
        KeyError if the status_list[0] does not correspond to a STATUS_CODES or VARIABLE_RESULTS key
    """
    def __init__(self, status_list=None, status_code=None, message=None, **kwargs):
        # build_response_dictionary requires a 2d array list
        self._response_body = {}

        # check if the second element is in status_codes.RESOURCE_NAMES
        if len(status_list)>=2:
            if status_list[1] in RESOURCE_NAMES:
                self._response_body['resource_name'] = status_list[1]
            # else check if the second element is the variable
            elif status_list[0] in VARIABLE_RESULTS:
                self._response_body['resource'] = status_list[1]

        # extra parameters will be used for the response body
        for key,value in kwargs.items():
            self._response_body[key] = value

        # custom status code or message
        if status_code or message:
            self.status_code = status_code
            self.message = message
            return

        status_dict = build_response_dictionary([status_list], is_description=False)

        if status_list[0] in STATUS_CODES.keys():
            self.status_code = STATUS_CODES[status_list[0]]['code']
        else:
            self.status_code = VARIABLE_RESULTS[status_list[0]]['code']

        self.message = status_dict[self.status_code]

    def get_response_body(self):
        '''
        Returns:
            the response body of the request in json format
        '''
        self._response_body['message'] = self.message
        return self._response_body
