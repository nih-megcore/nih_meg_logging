#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:10:55 2023

@author: jstout
"""
import logging
import os 



def initialize(bids_root):
    '''
    Set up QA project folder and create logging file

    Parameters
    ----------
    bids_root : path
        
    Returns
    -------
    history_log : list of historical log entries

    '''
    deriv_root = op.join(bids_root, 'derivatives') 
    if not op.exists(op.join(deriv_root, PROJECT)):
        os.mkdir(op.join(deriv_root, PROJECT))
    
    # Set up logging
    logfile = op.join(deriv_root, PROJECT, 'enigma_QA_logfile.txt')
    return_log=False
    if op.exists(logfile):
        with open(logfile) as f:
            history_log = f.readlines()
        #Strip newlines        
        history_log=[i[:-1] for i in history_log if i[-1:]=='\n']
        return_log=True
    logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info("REVIEW_START")
    if return_log==True:
        return history_log
    else:
        return None


# =============================================================================
# 
# =============================================================================
def get_last_review(history_log):
    '''Extract the start and stop of the last review
    Return the log lines from the last review'''
    rev_start_idx=0
    rev_end_idx=0
    for idx, line in enumerate(history_log):
        cond=line.split('INFO:')[-1]
        if cond=='REVIEW_START':
            rev_start_idx=idx
        elif cond=='REVIEW_FINISH':
            rev_end_idx=idx
    last_review=history_log[rev_start_idx+1:rev_end_idx]
    return last_review
        
def get_subject_status(logline_input):
    tmp=logline_input.split(':')
    datetimeval=':'.join(tmp[0:3])
    subject, status = None, None #Preinitialize
    if 'SUBJECT' in tmp:
        sub_idx = tmp.index('SUBJECT')
        subject = tmp[sub_idx+1]
    if 'STATUS' in tmp:
        stat_idx = tmp.index('STATUS')
        status = tmp[stat_idx+1]
    return subject, status

def build_status_dict(review_log):
    '''Loop over lines in review log and extract a dictionary of 
    subject status.'''
    subject_status_dict={}
    for line in review_log:
        subject,status = get_subject_status(line)
        if subject==None:
            continue
        subject_status_dict[subject]=status
    return subject_status_dict