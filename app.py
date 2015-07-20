#!/usr/bin/env python3

import requests
import argparse
import subprocess

TREEHERDER_BASE_URL = 'https://treeherder.mozilla.org'

def _get_results_id(repo, revision):
    r = requests.get('{}/api/project/{}/resultset/?count=10&full=true&revision={}'.format(TREEHERDER_BASE_URL, repo,
                                                                                          revision))
    return r.json()['results'][0]['id']


def _find_job_ids(results_id, job_type, job_number=None):
    r = requests.get('{}/api/project/gaia/jobs/?count=2000&result_set_id={}'.format(TREEHERDER_BASE_URL, results_id))
    results = r.json()['results']
    return [result['id'] for result in results
            if result['job_group_symbol'] == job_type
            and (job_number is None or result['job_type_symbol'] == (job_type + str(job_number)))]


def _retrigger_jobs(repo, job_ids, repeat=1):
    for i in range(0, repeat):
        for job_id in job_ids:
            print('\n', i, job_id)
            _execute_curl_request('retrigger', repo, job_id)


def _cancel_jobs(repo, job_ids, *args):
    for job_id in job_ids:
        print('\n', job_id)
        _execute_curl_request('cancel', repo, job_id)


def _execute_curl_request(command, repo, job_id):
    # subprocess.call(["curl",
    #                  "-XPOST",
    #                  "{}/api/project/{}/jobs/{}/{}/".format(TREEHERDER_BASE_URL, repo, job_id, command),
    #                  "-H",
    #                  "Cookie: ",    # TODO: Currently, you have to change the cookie by the one you have,
    #                                 # let's get this data from the command line
    #                  "-H",
    #                  "Referer: {}".format(TREEHERDER_BASE_URL),
    #                  "-H",
    #                  "X-CSRFToken: "])  # TODO: Currently, you have to change the cookie by the one you have,
    #                                     # let's get this data from the command line
    print(command, repo, job_id)


if __name__ == '__main__':
    command_choices = {'retrigger': _retrigger_jobs, 'cancel': _cancel_jobs}

    command_parser = argparse.ArgumentParser(description='Treeherder rerunner')
    command_parser.add_argument('command', type=str, choices=command_choices.keys(),
                                help='a command to execute')
    command_parser.add_argument('--revision', required=True,  type=str, help='')
    command_parser.add_argument('--job-type', required=True, type=str, help='')
    command_parser.add_argument('--job-number', type=int, help='')
    command_parser.add_argument('--repo', type=str, default='gaia', help='')
    command_parser.add_argument('--repeat', type=int, default=1, help='')

    args = command_parser.parse_args()
    results_id = _get_results_id(args.repo, args.revision)
    job_ids = _find_job_ids(results_id, args.job_type, args.job_number)

    command_choices[args.command](args.repo, job_ids, args.repeat)
