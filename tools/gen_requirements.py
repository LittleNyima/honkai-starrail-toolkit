import os
from typing import Iterable


def get_pipreqs_output():
    proc = os.popen('pipreqs . --print')
    output = proc.read()
    return output


def parse_pipreqs_output(reqs: str):

    def filter_version(single_req: str):
        return single_req.split('==')[0]

    req_list = reqs.strip().split('\n')
    return map(filter_version, req_list)


def merge_into_requirements(parsed_reqs: Iterable[str]):
    with open('requirements.txt') as fin:
        reqs = fin.read().strip().split('\n')
    reqs_set = set(reqs) | set(parsed_reqs)
    sorted_reqs = sorted(reqs_set)
    print('\n'.join(sorted_reqs))
    with open('requirements.txt', 'w') as fout:
        fout.write('\n'.join(sorted_reqs))


if __name__ == '__main__':
    reqs = get_pipreqs_output()
    parsed_reqs = parse_pipreqs_output(reqs)
    merge_into_requirements(parsed_reqs)
