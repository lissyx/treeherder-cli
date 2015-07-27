from model.base import Base
from model.result import Result

class Revision(Base):
    def __init__(self, client, sha1):
        super().__init__(client)
        self.sha1 = sha1

    @property
    def results(self):
        arguments = {'count': 10, 'full': True, 'revision': self.sha1}
        raw_results = self.client.execute_request(rest_resource='resultset', get_arguments=arguments)
        return [Result.from_json(self.client, raw_result) for raw_result in raw_results]
