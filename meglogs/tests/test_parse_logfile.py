#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 20:06:47 2023

@author: jstout
"""

# import pytest
from meglogs.meglog_parsing import parse_logtext

logtxt=['2023-03-24 16:41:41,614::INFO::REVIEW_START\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub03::STATUS::GOOD\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub02::STATUS::Unchecked\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub04::STATUS::BAD\n',
        '2023-03-24 16:41:45,940::INFO::SUBJECT::sub-Sub01::STATUS::GOOD\n',
        '2023-03-24 16:41:46,526::INFO::REVIEW_FINISH\n']


def test_parse_logfile():
    tmp_ = parse_logtext(logtxt)
    assert len(tmp_) == len(logtxt)-2
