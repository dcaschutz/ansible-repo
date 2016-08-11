class FilterModule(object):
    ''' Ansible jinja2 filters '''

    def filters(self):
        return {
          'find_missing_subnets': find_missing_subnets,
          'get_subnet_name': get_subnet_name
        }


def find_missing_subnets(existing_environment_subnets, environment_subnets, environment_name):
  # existing_environment_subnets: found.
  # environment_subnets: configured
  missing_subnets = []
  #import pprint; pprint.pprint(existing_environment_subnets); sys.exit(0)
  for env_subnet in environment_subnets:
    found = False
    for existing_sub in existing_environment_subnets:
      if(
        'tags' in existing_sub and
        'Name' in existing_sub['tags'] and
        existing_sub['tags']['Name'] == get_subnet_name(environment_name, env_subnet['name'])
      ):
        found = True
    if not found:
      missing_subnets.append(env_subnet)
  return missing_subnets
         
def get_subnet_name(environment, name):
   return "subnet-{0}-{1}".format(environment, name)
