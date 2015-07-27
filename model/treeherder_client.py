import requests

class TreeherderClient:

    TREEHERDER_BASE_URL = 'https://treeherder.mozilla.org'

    def __init__(self, repo, csrf_token, session_id):
        self.repo = repo
        self.csrf_token = csrf_token
        self.session_id = session_id

    def execute_request(self, http_verb='get', rest_resource='', get_arguments=None):
        get_query = self._craft_get_query(get_arguments)

        url = '{}/api/project/{}/{}/{}'.format(self.TREEHERDER_BASE_URL, self.repo, rest_resource, get_query)
        headers = {'Referer': self.TREEHERDER_BASE_URL, 'X-CSRFToken': self.csrf_token}
        cookies = {'sessionid': self.session_id, 'csrftoken': self.csrf_token}

        http_method = getattr(requests, http_verb)
        response = http_method(url, headers=headers, cookies=cookies)
        response.raise_for_status()

        # Treeherder returns objects like {"meta": {}, results: {}}. Meta is not needed.
        return response.json().get('results')

    def _craft_get_query(self, get_arguments=None):
        get_query = None
        if get_arguments is not None:
            get_arguments = ['{}={}'.format(key, value) for key, value in get_arguments.items()]
            get_query = '&'.join(get_arguments)

        return '?{}'.format(get_query) if get_query else ''
