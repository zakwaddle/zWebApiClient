import requests
from requests.auth import AuthBase


class WebApiAuth(AuthBase):
    """
    a very loose wrapper around the requests.auth.AuthBase class.
    this class defaults to adding: {'Authorization': f'Bearer {self.token}'}
    to the request header of each request

    both __init__() and __call__() may be overwritten to
    accommodate more complex authorization processes
    """

    def __init__(self, token) -> None:
        self.token = token

    def __call__(self, request):
        request.headers.update({
            'Authorization': f'Bearer {self.token}',
        })
        return request
    
    def __repr__(self):
        return f"{__class__.__name__}"

class WebRequest:
    """
    WebRequest is a class to contain both a request to a resource, and it's associated response
    All methods of the WebRequest class will currently return "None" and will only
    populate an already existing attribute
    todo: implement a method for dealing with paginated responses
    """
    url = None
    method = None
    response: requests.Response = None
    params: dict = None
    complete = False
    status_code = None

    def __init__(self, method, url, params: dict = None) -> None:
        self.method = method
        self.url = url
        self.params = params

    def send(self) -> None:
        """
        execute the request and populate 'self.response'
        with the results (an object of the requests.Response class)
        :return: None
        """
        self.response = requests.request(self.method, self.url, **self.params)
        self.complete = True
        self.status_code = self.response.status_code

    def __repr__(self):
        return f'WebRequest({self.method}, {self.url}, {self.params})'


class WebApiClient:
    """
    WebApiClient is intended as a base class for building classes to interact with a REST API.
    It provides most of the boilerplate I found myself writing with nearly all 'api client' classes
    It also provides convenient class methods with can be overwritten to perform pre- and post-processing
    on a request
    """

    @classmethod
    def observer(cls, *args, **kwargs) -> None:
        """
        not actually sure that this method is necessary
        it was conceived as a place for logging or other output and/or debugging features.
        however it was removed from the 'self.__execute' sequence, kinda making it pointless.
        :param args: any
        :param kwargs: any
        :return: None
        """
        pass

    @classmethod
    def pre_flight(cls, req: WebRequest) -> WebRequest:
        """
        called before executing the request.
        overwrite this method to perform
        any preprocessing or logging of the request.
        BE SURE TO RETURN THE REQUEST!

        :param req: WebRequest
        :return: WebRequest
        """
        return req

    @classmethod
    def post_flight(cls, req: WebRequest):
        """
        called after executing the request.
        overwrite this method to perform
        any post-processing, validation, logging, or transformations of the request results.
        whatever is returned from this method will be the returned value of the called request method
        be sure to return from this method if overwriting
        :param req:
        :return:
        """
        return req

    def __init__(self, base_url, auth: WebApiAuth):
        self.auth = auth
        self.base_url = base_url

    def __make_url(self, *route_bits):
        """
        smash the route parts together with '/' and add the resulting resource path to the base_url
        return the resulting string

        :param route_bits:
        :return: request url
        """
        route = '/'.join([str(bit) for bit in route_bits])
        if route.startswith(self.base_url):
            return route
        return self.base_url + route

    def __create_request(self, method, *route_bits, **kwargs):
        url = self.__make_url(*route_bits)
        params = {'auth': self.auth, **kwargs}
        return WebRequest(method, url, params)

    def __execute(self, req: WebRequest):
        req = self.pre_flight(req)
        req.send()
        req = self.post_flight(req)
        return req

    def get(self, *route_bits, **kwargs):
        req = self.__create_request('GET', *route_bits, **kwargs)
        return self.__execute(req)

    def post(self, *route_bits, **kwargs):
        req = self.__create_request('POST', *route_bits, **kwargs)
        return self.__execute(req)

    def put(self, *route_bits, **kwargs):
        req = self.__create_request('PUT', *route_bits, **kwargs)
        return self.__execute(req)

    def patch(self, *route_bits, **kwargs):
        req = self.__create_request('PATCH', *route_bits, **kwargs)
        return self.__execute(req)

    def delete(self, *route_bits, **kwargs):
        req = self.__create_request('DELETE', *route_bits, **kwargs)
        return self.__execute(req)
