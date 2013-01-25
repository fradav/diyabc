# -*- coding: utf-8 -*-

## @package python_interface.utils.diyabcUtils
# @author Julien Veyssier
#
#     - readRefTableSize : extract the record number of a DIYABC binary reference
#       table 
#     - readNbRecordsOfScenario : extract the record number which concern a
#       specific scenario

import array
import os, os.path

def readRefTableSize(reftablefile):
    """ @rtype: int
    @return: the record number in binary reftable header
    """
    if os.path.exists(reftablefile):
        binint = array.array('i')
        f = open(reftablefile,'rb')
        binint.read(f,1)
        f.close()
        rtSize = binint[0]
        return rtSize
    else:
        return None

def readNbRecordsOfScenario(reftablefile,numSc):
    """ @rtype: int
    @return: record number of a given scenario
    in binary reftable header
    """
    if os.path.exists(reftablefile):
        binint = array.array('i')
        f = open(reftablefile,'rb')
        binint.read(f,numSc+2)
        f.close()
        nbRec = binint[-1]
        return nbRec
    else:
        return None

