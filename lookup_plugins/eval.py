#!/usr/bin/env python

# lookup( 'example', 'foo', 'bar' )
import ansible.errors as errors
from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        # terms = input, eval_string
        if len(terms) != 2:
          raise Exception("Usage: lookup('eval', input, eval_String)")
        input = terms[0]
        eval_string = terms[1]
        return eval(terms[1])
