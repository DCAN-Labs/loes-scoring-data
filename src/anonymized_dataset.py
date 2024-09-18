#!/usr/bin/python

import os
import shutil
from pathlib import Path
import shutil
import pandas as pd
import math


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_ids(folder):
    os.chdir(folder)
    sessions = dict()
    for root, _, _ in os.walk('.'):
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


def rename_subject_folders(participants_mapping_df, bids_root_out):
    immediate_subdirectories = get_immediate_subdirectories(bids_root_out)
    for immediate_subdirectory in immediate_subdirectories:
        anonymized_participant_id = participants_mapping_df.loc[participants_mapping_df['participant_id'] == immediate_subdirectory, 'anonymized_participant_id'].iloc[0]
        os.rename(os.path.join(bids_root_out, immediate_subdirectory),
            os.path.join(bids_root_out, anonymized_participant_id))


if __name__ == '__main__':
    from_directory = '/users/9/reine097/data/loes-scoring-data/Loes_score/'
    ids = get_ids(from_directory)
    to_directory = "/users/9/reine097/data/loes-scoring-data/Loes_score_anonymized"
    dirpath = Path(to_directory)
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    shutil.copytree(from_directory, to_directory)
    encoding = anonymize_dataset(from_directory, to_directory)
    rename_subject_folders(encoding, to_directory)
