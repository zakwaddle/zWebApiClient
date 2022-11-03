## zWebApiClient
- - - 

zWebApi is a wrapper around the "requests" python module
which tries to provide an easy interface for interacting with 
web apis. It is intended to be subclassed, but can also be used
on its own.

```python
from zWebApiClient import WebApiClient, WebApiAuth

auth = WebApiAuth('superAwesomeApiAuthString-234ou27t87')
example_api = WebApiClient('www.example.com/api/', auth)

request = example_api.get('users', 235, 'contacts')
print(request.response.json())


```
or 

```python
from zWebApiClient import WebApiClient, WebApiAuth

auth = WebApiAuth('superAwesomeApiAuthString-234ou27t87')
example_api = WebApiClient('www.example.com/api/', auth)

def fetch_user_contacts(user_id):
    request = example_api.get('users', user_id, 'contacts')
    if request.status_code == 200:
        return request.response.json()

print(fetch_user_contacts(357))

```

while an example of subclassing might look like this:

```python
from zWebApiClient import WebApiClient, WebApiAuth


class HubSpotAuth(WebApiAuth):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update({'accept': 'application/json'})
        return request


class HubSpotApiClient(WebApiClient):

    def __init__(self, api_key):
        super().__init__("https://api.hubapi.com/", HubSpotAuth(api_key))

    def pre_flight(self, req):
        auth = {"hapikey": self.auth.api_key}
        if req.params.get("params") is not None:
            req.params['params'].update(auth)
        else:
            req.params['params'] = auth
        return req

    def get_marketing_forms(self):
        return self.get("marketing", "v3", "forms")

    def get_contact(self, contact_id, version=1, **kwargs):
        if version == 1:
            return self.get('contacts', 'v1', 'contact', 'vid', contact_id, 'profile', params=kwargs)

        if version == 3:
            return self.get('crm', 'v3', 'objects', 'contacts', contact_id, params=kwargs)


    def get_contact_list(self, list_id):
        return self.get('contacts', 'v1', 'lists', list_id)

    def get_all_forms(self):
        return self.get('forms', 'v2', 'forms')

    def get_list_contacts(self, list_id):
        return self.get('contacts', 'v1', 'lists', list_id, 'contacts', 'all')

```

The zWebAuth class will by default add:

            'Authorization': f'Bearer {self.token}'

to header of each request. Each api is different, however. 
For more complicated authorizations, the WebAuth class 
can be subclassed and the " __ call __()" method overwritten. 

*Don't forget to return the request when doing this!*

example:

```python
from zWebApiClient import WebApiAuth, WebApiClient

class HubSpotAuth(WebApiAuth):

    def __init__(self, api_key):
        super().__init__(api_key)
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update({'accept': 'application/json'})
        return request


class HubSpotApiClient(WebApiClient):

    def __init__(self, api_key):
        super().__init__("https://api.hubapi.com/", HubSpotAuth(api_key))

    def pre_flight(self, req):
        auth = {"hapikey": self.auth.api_key}
        if req.params.get("params") is not None:
            req.params['params'].update(auth)
        else:
            req.params['params'] = auth
        return req


```

in this example, authorization must be provided as a url search param, and 'application/json' must be added to each header

In this case, adding the authorization info has been moved to the "pre_flight" step, being careful not to
overwrite any previously provided params, 
and the "__ call __()" method has been overwritten.   