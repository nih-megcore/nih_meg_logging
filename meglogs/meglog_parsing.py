#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 20:08:04 2023

@author: jstout
"""
import copy
import pandas as pd
from meglogs.DEFAULTS import LOG_STYLE, GLOBAL_KEYS, LOG_DELIM

null_dframe = pd.DataFrame(columns=LOG_STYLE.split(LOG_DELIM))

def parse_logtext(logtxt):
    dframe = copy.deepcopy(null_dframe)
    for logline in logtxt:
        tmp_ = logline.split(LOG_DELIM)
        if len(tmp_) > len(dframe.columns):
            raise ValueError(f'''Log parsing did not complete correctly
                             the values exceed the expected length -- 
                             possibly extra "{LOG_DELIM}" in string''')
        elif len(tmp_) < len(dframe.columns):
            is_global = [ i for i in tmp_ if i in GLOBAL_KEYS ] 
            if len(is_global)>0:
                dframe.loc[len(dframe), ['DATETIME','LOGLEVEL', 'PROJECT','MEGSSAGETAG']] = tmp_
        else:
            #Standard Message Parse
            dframe.loc[len(dframe)]=tmp_
    return dframe
        
        

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


    