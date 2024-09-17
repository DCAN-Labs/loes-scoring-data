#!/usr/bin/python

import os
import random
import random
from datetime import datetime, timedelta
import pickle
import shutil
from pathlib import Path
import shutil
import pandas as pd
import math


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


def anonymize_dataset(bids_root_in, bids_root_out):
    participants_df = pd.read_csv(os.path.join(bids_root_in, 'participants.tsv'))
    participant_ids = participants_df["participant_id"].tolist()
    places = int(math.ceil(math.log10(len(participant_ids))))
    participants_df = participants_df.reset_index()  # make sure indexes pair with number of rows
    next_ordinal = 0
    new_ids = []
    for _, _ in participants_df.iterrows():
        next_id = 'sub-' + str(next_ordinal).rjust(places, '0')
        while next_id in participant_ids:
            next_ordinal += 1
            next_id = 'sub-' + str(next_ordinal).rjust(places, '0')
        new_ids.append(next_id)
        participant_ids.append(next_id)
    se = pd.Series(new_ids)
    participants_df['anonymized_participant_id'] = se.values
    participants_df.to_csv(os.path.join(bids_root_out, 'participants.tsv'), index=False, index_label=False)

    return participants_df


def randomized_id(ids, copy_dir):
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
        first_time = datetime(1971, 1, 1, 0, 0, 0)
        first_ses = 'ses-' + str(datetime(1971, 1, 1, 0, 0, 0))
        encoded_sessions = [0]
        for session in sessions[1:]:
            later_time = datetime(int(session[4:8]), int(session[8:10]), int(session[10:12]))
            difference = later_time - first_time
            later_encoded_time = first_time + timedelta(days=difference.days)
            later_encoded_time_ses = 'ses-' + str(later_encoded_time)
            encoded_sessions.append(later_encoded_time_ses)

    return plain_text_to_anonymous



if __name__ == '__main__':
    from_directory = '/users/9/reine097/data/loes-scoring-data/Loes_score/'
    ids = get_ids(from_directory)
    to_directory = "/users/9/reine097/data/loes-scoring-data/Loes_score_anonymized"
    dirpath = Path(to_directory)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    shutil.copytree(from_directory, to_directory)
    encoding = anonymize_dataset(from_directory, to_directory)
