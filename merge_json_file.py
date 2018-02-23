import json
import sys

import os

from utils import json_in_dir


def merge(json_file_dir):
    merged_file = os.path.join(json_file_dir, 'merged.json')
    json_files = json_in_dir(json_file_dir)

    merged = []
    for file in json_files:
        with open(file) as j:
            merged.append(json.load(j))

    with open(merged_file, mode='w', encoding='utf-8') as file:
        json.dump(merged, file)


if __name__ == '__main__':
    merge(sys.argv[1])
    print('Merged into {}'.format('merged.json'))
