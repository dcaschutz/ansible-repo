#!/usr/bin/env python

import ansible.errors as errors
from ansible.plugins.lookup import LookupBase

import json
from netaddr import *
from pprint import pformat

class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):

        if not len(terms) == 2:
          raise Exception(
            "usage: lookup('net_contains', [ outer blocks ], [ inner ])"
          )
        
        outer_list = terms[0]
        inner_list = terms[1]
        if not isinstance(outer_list, list):
            outer_list = IPSet([ outer_list ])
        else:
            outer_list = IPSet(outer_list)
        if isinstance(inner_list, list):
            inner_list = IPSet(inner_list)
        else:
            inner_list = IPSet([ inner_list ])

        contains = True
        for i in inner_list:
            if not i in outer_list:
                contains = False
        return contains
