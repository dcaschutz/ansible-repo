#!/usr/bin/env python

import ansible.errors as errors
from ansible.plugins.lookup import LookupBase

import json
from netaddr import *
from pprint import pformat

class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    # Given:
    #   a netblock
    #   a subnet size
    #   existing subnets in netblock
    # return the next available subnet of size
    # lookup('find_free_net', '10.0.0.0/16', 24, [ '10.0.0.0/24' ]) =>
    # '10.0.1.0/24'
    def run(self, terms, inject=None, **kwargs):

        if not len(terms) == 3:
          raise Exception(
            "usage: lookup('find_free_net', 'netblock', subnet_size, existing_subnet_list )"
          )
        
        outer_block = IPNetwork(terms[0])
        size = terms[1]
        existing = IPSet(terms[2])

        from pprint import pformat
        if size < outer_block.prefixlen:
          raise Exception(
            "Requested subnet is larger than passed block " + outer_block
          )

        ip_block_addr = outer_block.first
        assigned = None
        while(ip_block_addr < outer_block.last and not assigned):
          test_cidr = IPNetwork((ip_block_addr, size))
          found = False
          if test_cidr in existing:
            found = True
          else:
            for e in existing.iter_cidrs():
              if e in IPSet([ test_cidr ]):
                found = True
          if not found:
            assigned = test_cidr
            break
          ip_block_addr += 2 ** (32 - size)

        if not assigned:
          raise Exception("Unable to assign a block of size " + size + " from " + outer_block)
        return assigned
