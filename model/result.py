from model.base import Base
from model.job import Job

class Result(Base):
    def __init__(self, client, result_id):
        super().__init__(client)
        self.id = result_id

    @property
    def jobs(self):
        arguments = {'count': 2000, 'result_set_id': self.id}
        raw_results = self.client.execute_request(rest_resource='jobs', get_arguments=arguments)
        return [Job.from_json(self.client, raw_result) for raw_result in raw_results]

    def get_jobs_for(self, job_type, job_number=None, job_platform=None):
        return [job for job in self.jobs if job.match(job_type, job_number, job_platform)]

    @staticmethod
    def from_json(client, json):
        return Result(client, json['id'])
