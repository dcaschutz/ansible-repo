class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            'missing_item_names' : missing_item_names
        }

#      set_fact: missing_item_names="{{ existing_items|missing_item_names(names) }}"
# assumes items will have names in tags, aws style.
# [ { 'foo': 'bar', 'tags': { 'Name': 'object name', ... }, ... }, ... ]
def missing_item_names(existing_items, desired_names):
  existing_names = [s['tags']['Name'] for s in existing_items if 'tags' in s.keys() and 'Name' in s['tags'].keys()]
  return [name for name in desired_names if name not in existing_names]
