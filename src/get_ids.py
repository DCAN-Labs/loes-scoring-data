#!/usr/bin/python

import os
import random
from itertools import permutations


def get_ids(folder):
    os.chdir(folder)
    sessions = dict()
    for root, dirs, files in os.walk('.'):
        path = root.split(os.sep)
        if len(path) < 3:
            continue
        subject = path[1]
        session = path[2]
        if subject not in sessions:
            sessions[subject] = []
        sessions[subject].append(session)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            print(len(path) * '---', file)

    return sessions

def randomized_id(ids):
    random.seed(23)
    subject_count = len(ids)
    for i in permutations(range(subject_count)):
        list_copy = range(len(ids(i)))
        ids[i] = list_copy
    return list_copy


if __name__ == '__main__':
    ids = get_ids("/users/9/reine097/data/loes-scoring-data/Loes_score/")
    print(ids)
    new_ids = randomized_id(ids)
    print(new_ids)
