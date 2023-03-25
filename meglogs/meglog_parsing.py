#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 20:08:04 2023

@author: jstout
"""

import pandas as pd

CODE_PARSE = 'DATETIME::LOGLEVEL::PROJECT::SUBJECT::MESSAGTAG::VALUE'
parse_delim = '::'
dframe = pd.DataFrame(columns=CODE_PARSE.split(parse_delim))

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


logtxt=['2023-03-24 16:41:41,614::INFO::REVIEW_START\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub03::STATUS::GOOD\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub02::STATUS::Unchecked\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub04::STATUS::BAD\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub01::STATUS::GOOD\n',
        '2023-03-24 16:41:46,526::INFO::REVIEW_FINISH\n']