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
  import pprint
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
            vpc_facts = dict(required=True),
            vpc_tags = dict(required=True)
            # 
            # argument type coercion
            # count     = dict(default=1, type='int'), 
        )
    )

    vpc_facts = eval(module.params['vpc_facts'])
    vpc_tags = eval(module.params['vpc_tags'])
    #from pprint import pformat;# raise Exception(pformat(vpc_facts))
    f = open('/tmp/crap','w')

    matching_vpcs = []
    existing_vpc_tags = None

    for vpc in vpc_facts['vpcs']:
      if not 'tags' in vpc:
        continue
      existing_vpc_tags = vpc['tags']
      matched = True
      for tag_name, tag_value in vpc_tags.items():
        if not tag_name in existing_vpc_tags or existing_vpc_tags[tag_name] != tag_value:
          matched = False
      if matched:
        matching_vpcs.append(vpc)

    if len(matching_vpcs) > 1:
      raise Exception(
        "Found " + len(matching_vpcs) + " VPCs! Check AWS for multiple VPCs with tags: " + pprint.pformat(vpc_tags)
      )

    # if success ...
    module.exit_json(changed=changed, msg=message, vpcs=matching_vpcs)
    # ... otherwise, if failure
    # module.fail_json(msg="explain why the module failed here")


# import module snippets
from ansible.module_utils.basic import *

main()
