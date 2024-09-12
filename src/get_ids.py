#!/usr/bin/python

import os

sessions = dict()
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("data/Loes_score"):
    path = root.split(os.sep)
    if len(path) < 4:
        continue
    subject = path[2]
    session = path[3]
    if subject not in sessions:
        sessions[subject] = []
    sessions[subject].append(session)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)
