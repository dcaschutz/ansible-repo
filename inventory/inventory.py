#!/usr/bin/env python

import argparse
import os
from yaml import load


parser = argparse.ArgumentParser()
parser.add_argument('--env', help='SSDC environment')
parser.add_argument('--list', action='store_true', help='list inventory')
parser.add_argument('--host')
args = parser.parse_args()

dir = os.path.dirname(os.path.abspath(__file__))

def yamload(file):
  return load(open(file))

# python almost has a built in method for dealing with dict merges.
def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not b:
      return a
    if not a:
      return b
    if not isinstance(b, dict):
        return b
    for k, v in b.iteritems():
        if k in a and isinstance(a[k], dict):
            a[k] = dict_merge(b[k], v)
        else:
            a[k] = v
    return a


default = yamload(dir + '/../infrastructure/default.yaml')

env = args.env or os.environ['SWEETSPOT_ENVIRONMENT']
if not env:
  raise Exception("SWEETSPOT_ENVIRONMENT environment variable must be set")


env_specific = yamload(
  dir + '/../../infrastructure/environments/' + env + '.yaml'
)

merged = dict_merge(default, env_specific)

#import pprint
#pprint.pprint(merged)

if not merged['AWS_PROFILE']:
  raise Exception(
    "No AWS_PROFILE set in either defaults or {0}.yaml".format(args.env)
  )

os.environ['AWS_PROFILE'] = merged['AWS_PROFILE']

ec2_args = [ 'ec2.py' ]
if args.list:
  ec2_args.append('--list')

if args.host:
  ec2_args.append('--host')
  ec2_args.append(args.host)

os.execv(dir + '/ec2.py', ec2_args)
