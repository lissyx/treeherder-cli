#!/usr/bin/env python3

import argparse
import itertools
from model.treeherder_client import TreeherderClient
from model.revision import Revision

def _flatten_list(a_list):
    return list(itertools.chain.from_iterable(a_list))

def parse_args():
    command_choices = ('retrigger', 'cancel', 'log')

    command_parser = argparse.ArgumentParser(description='Treeherder client')
    command_parser.add_argument('command', type=str, choices=command_choices, help='a command to execute')
    command_parser.add_argument('--revision', required=True,  type=str, help='')
    command_parser.add_argument('--job-type', required=True, type=str, help='')
    command_parser.add_argument('--csrf-token', required=True, type=str, help='')
    command_parser.add_argument('--session-id', required=True, type=str, help='')
    command_parser.add_argument('--job-number', type=int, help='')
    command_parser.add_argument('--job-platform', type=str, help='')
    command_parser.add_argument('--repo', type=str, default='gaia', help='')
    command_parser.add_argument('--repeat', type=int, default=1, help='')

    return command_parser.parse_args()

def main(cli_args):
    client = TreeherderClient(cli_args.repo, cli_args.csrf_token, cli_args.session_id)
    revision = Revision(client, cli_args.revision)
    results = revision.results
    jobs = [result.get_jobs_for(cli_args.job_type, job_number=cli_args.job_number, job_platform=cli_args.job_platform) for result in results]
    jobs = _flatten_list(jobs)

    for job in jobs:
        for i in range(1, cli_args.repeat + 1):
            print('Repeat #{}'.format(i))
            job.__getattribute__(cli_args.command)()

if __name__ == '__main__':
    args = parse_args()
    main(args)
