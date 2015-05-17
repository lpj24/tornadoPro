#-*- coding:utf8 -*-
from sphinxapi import *


def get_sphinxClient():
    client = None
    if not client:
        client = SphinxClient()
        client.SetServer('localhost',9312)
        client.SetMatchMode(SPH_MATCH_ANY)
    return client
