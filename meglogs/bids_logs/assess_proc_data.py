#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 10:54:02 2023

@author: jstout
"""

import mne_bids
from mne_bids import BIDSPath, find_matching_paths
import os, os.path as op
import copy

PROJECT = 'ENIGMA_MEG'
# /data/EnigmaMeg/BIDS/NIH_hvmeg_20220131
## Defaults
# bids_root = '/fast/OPEN/NIH_stringaris'
# deriv_root = op.join(bids_root, 'derivatives', PROJECT)
# subjects_dir = op.join(bids_root, 'derivatives', 'freesurfer', 'subjects')


# bids_paths = find_matching_paths(deriv_root, tasks=task_id, extensions='.fif')
# bids_paths += find_matching_paths(deriv_root, tasks=task_id, extensions='.hdf5')


def is_present(data_list):
    for dataset in data_list:
        if op.exists(dataset):
            print(f'{dataset} present')
        else:
            print(f'{dataset} missing')
    
# def dict_fromVarlist(varlist):
#     outdict = {}
#     for varval in varlist:
#         varname = [ i for i, j in locals().items() if j == varval][1]
#         outdict[varname]=varval
#     return outdict
        

# =============================================================================
# Freesurfer Files
# =============================================================================

def get_fs_filedict(subject, bids_root):
    subjects_dir = op.join(bids_root, 'derivatives', 'freesurfer', 'subjects')
    
    fs_dict = {}
    # FS default files
    fs_dict['001mgz'] = f'sub-{subject}/mri/orig/001.mgz'
    fs_dict['T1mgz'] = f'sub-{subject}/mri/T1.mgz'
    fs_dict['lh_pial'] = f'sub-{subject}/surf/lh.pial'
    fs_dict['rh_pial'] = f'sub-{subject}/surf/rh.pial'
    fs_dict['lh_dkaparc'] = f'sub-{subject}/label/lh.aparc.DKTatlas.annot'
    fs_dict['rh_dkaparc'] = f'sub-{subject}/label/rh.aparc.DKTatlas.annot'
    
    # FS - post process files
    fs_dict['in_skull'] = f'sub-{subject}/bem/inner_skull.surf'
    fs_dict['head'] = f'sub-{subject}/bem/sub-{subject}-head.fif'
    fs_dict['head_dense'] = f'sub-{subject}/bem/sub-{subject}-head-dense.fif'
    
    # Morph maps for sub-aparc
    fs_dict['morph'] = f'morph-maps/fsaverage-sub-{subject}-morph.fif'
    
    # Prepend subjects_dir
    for key, value in fs_dict.items():
        fs_dict[key] = op.join(subjects_dir,value)
        if not op.exists(fs_dict[key]):
            fs_dict[key]=False
    return fs_dict

# =============================================================================
# ENIGMA BIDS Outputs 
# =============================================================================

#!!!FIX - this may find more than 1 file -- need to rectify 
def check_expected(bids_paths, expected_suffixlist, check_dict):
    '''
    Do set operations to determine the missing files from the bids paths
    The function updates the input dictionary with the expected_suffixlist
    as keys.  The values are set to the path or to False if not found

    Parameters
    ----------
    bids_paths : mne_bids.BIDSPath
        DESCRIPTION.
    expected_suffixlist : list
        List of expected suffixes from the bids paths.
    check_dict : dict
        Dictionary to update with missing/present values.

    Returns
    -------
    check_dict : dict
        Updated input dictionary with paths or False for entries.

    '''
    found_dict = {i.suffix:i for i in bids_paths}
    for key in expected_suffixlist: 
        if key in found_dict.keys():
            check_dict[key] = str(found_dict[key].fpath)
        else:
            check_dict[key] = False  
    return check_dict

def get_enigma_outputs(subject, bids_root):
    '''
    Return enigma expected outputs.    

    Parameters
    ----------
    subject : str
        BIDS subject ID without sub-
    bids_root : path
        Top level bids path

    Returns
    -------
    Dictionary with enigma outputs

    '''
    deriv_root = op.join(bids_root, 'derivatives', PROJECT)
    
    enigma_dict = {}
    subj_paths = find_matching_paths(deriv_root,
                                     subjects=subject, 
                                     extensions='.fif')
    expected_fifs = set(['bem', 'src', 'cov', 'epo', 'fwd', 'meg', 'trans'])
    enigma_dict = check_expected(subj_paths, expected_fifs, enigma_dict)
        
    ## Add in hd5 files for beamformer
    hdf5_paths = find_matching_paths(deriv_root,
                                     subjects=subject, 
                                     extensions='.h5')
    expected_f5s = set(['lcmv'])
    enigma_dict = check_expected(hdf5_paths, expected_f5s, enigma_dict)

#!!!FIX    
    # ## CSV outputs   <<<<<<<<  FIX Either make csv BIDS compatible or manual search
    # expected_csvs = set(['Band_rel_power', 'label_spectra'])
    # csvs_paths = find_matching_paths(deriv_root,
    #                                  subjects=subject, 
    #                                  extensions='.csv')    
    return enigma_dict

    
def status_expected_files(subject, bids_root):
    fs_dict = get_fs_filedict(subject, bids_root)
    en_dict = get_enigma_outputs(subject, bids_root)
    
    final = copy.deepcopy(fs_dict)
    final.update( en_dict )
    return final

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-subject')
    parser.add_argument('-bids_root')
    args = parser.parse_args()
    
    subject = args.subject
    bids_root = args.bids_root
    
    final = status_expected_files(subject, bids_root)
    print(final)



    
