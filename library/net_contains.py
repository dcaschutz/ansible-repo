#!/usr/bin/env python

# DEPRECATED:
# This has been implemented as a lookup_plugin.
#
# However, this is instructive for general module creation.
# usage:
# net_contains: outer='1.2.3.0/24', inner='1.2.3.5'
# => { "contains" => "True" }


# WANT_JSON

try:
  import json
  from netaddr import *
except ImportError, e:
    print "failed=True msg='failed to import python module: %s'" % e
    sys.exit(1)


def main():
    changed = False
    message = ''

    module = AnsibleModule(
        argument_spec = dict(
            # specify possible arguments that can be passed to your module
            # 
            #
            # you can specify possible choices
            # state     = dict(default='present', choices=['present', 'absent']),
            # 
            # required arguments
            # name      = dict(required=True),
            outer = dict(required=True),
            inner = dict(required=True)
            # 
            # argument type coercion
            # count     = dict(default=1, type='int'), 
        )
    )

    outer = module.params['outer']
    inner = module.params['inner']
    if not isinstance(outer, list):
      outer = IPSet([ outer ])
    else:
      outer = IPSet(outer)
    if isinstance(inner, list):
      inner = IPSet(inner)
    else:
      inner = IPSet([ inner ])

    contains = True
    for i in inner:
      if not i in outer:
        contains = False
    

    # fill this with info that you want added to the ansible environment
    # http://docs.ansible.com/developing_modules.html#module-provided-facts
    facts = dict()

    facts['contains'] = contains

    # if success ...
    module.exit_json(changed=changed, msg=message, ansible_facts=facts)
    # ... otherwise, if failure
    # module.fail_json(msg="explain why the module failed here")


# import module snippets
from ansible.module_utils.basic import *

main()
