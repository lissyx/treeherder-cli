from model.base import Base

class Job(Base):
    def __init__(self, client, job_id, type_symbol, group_symbol, build_platform):
        super().__init__(client)
        self.id = job_id
        self.type_symbol = type_symbol
        self.group_symbol = group_symbol
        self.build_platform = build_platform

    def cancel(self):
        self._execute_action(action='cancel')

    def retrigger(self):
        self._execute_action(action='retrigger')

    def log(self):
        print(self._get_joblog())

    def _execute_action(self, action):
        rest_resource = 'jobs/{}/{}'.format(self.id, action)
        self.client.execute_request(http_verb='post', rest_resource=rest_resource)
        print('Job {} {} ({}) {}ed'.format(self.group_symbol, self.type_symbol, self.id, action))

    def _get_joblog(self):
        import requests
        url = '{}/api/project/{}/job-log-url/?job_id={}'.format(self.client.TREEHERDER_BASE_URL, self.client.repo, self.id)
        r = requests.get(url)
        return requests.get(r.json()[0]["url"]).text

    @staticmethod
    def from_json(client, json):
        return Job(client, json['id'], json['job_type_symbol'], json['job_group_symbol'], json['build_platform'])

    def match(self, job_type, number=None, platform=None):
        return self.group_symbol == job_type \
               and (number is None or self._match_job_number(job_type, number)) \
               and (platform is None or self.build_platform == platform)

    def _match_job_number(self, job_type, number):
        possible_formats = ('{}{}'.format(job_type, number), str(number))   # Example Gij1 or 1
        return self.type_symbol in possible_formats
