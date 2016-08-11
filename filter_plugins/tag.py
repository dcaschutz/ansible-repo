class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            'tag_filter' : tag_filter
        }

# [ { 'tags': { 'Name': 'other value'} },{ 'tags': { 'Name': 'some tag value' } } ] | tag_filter('Name','some tag value')
# => [ { 'tags': { 'Name': 'some tag value' } ]
def tag_filter(input_hashes, tag_name, tag_value):
  return [h for h in input_hashes if 'tags' in h.keys() and tag_name in h['tags'] and h['tags'][tag_name] in tag_values]

# [ { 'tags': { 'Name': 'other value'} },{ 'tags': { 'Name': 'some tag value' } } ] | tag_filter('Name','some tag value')
# => [ { 'tags': { 'Name': 'other value' } ]
def tag_reject(input_hashes, tag_name, tag_values):
  return [h for h in input_hashes if 'tags' not in h.keys() or tag_name not in h['tags'] or h['tags'][tag_name] not in tag_values]
