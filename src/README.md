# loes-scoring-dataset

This project basically contains code to anonymize a Loes scoring data set.

The main method is 

    anonymize_dataset(
        bids_root_in,
        bids_root_out,
        daysback="auto",
        subject_mapping="auto",
        datatypes=None,
        random_state=None,
        verbose=None,
    )
