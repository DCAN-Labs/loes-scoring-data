#!/usr/bin/python

import os
import random
from itertools import permutations
import random
from datetime import datetime, timedelta


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

    return sessions

def randomized_id(ids):
    plain_text_to_anonymous = dict()
    for subject in ids.keys():
        random_subject = 'sub-'
        for i in range(4):
            rand_digit = chr(ord('0') + random.randint(0, 9))
            random_subject = random_subject + rand_digit
        for i in range(4):
            rand_letter = chr(ord('A') + random.randint(0, 25))
            random_subject = random_subject + rand_letter
        plain_text_to_anonymous[subject] = random_subject
        sessions = ids[subject]
        first_time = datetime(int(sessions[0][4:8]), int(sessions[0][8:10]), int(sessions[0][10:12]))
        encoded_sessions = [0]
        for session in sessions[1:]:
            later_time = datetime(int(session[4:8]), int(session[8:10]), int(session[10:12]))
            difference = later_time - first_time
            later_encoded_time = first_time + timedelta(days=difference.days)
            print(later_encoded_time)



if __name__ == '__main__':
    ids = get_ids("/users/9/reine097/data/loes-scoring-data/Loes_score/")
    print(ids)
    new_ids = randomized_id(ids)
    print(new_ids)
